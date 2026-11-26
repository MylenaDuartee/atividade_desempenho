"""
DESAFIO A - Trabalho 1: abertura da matrícula 2026.2 (Locust / Python)

Complete este arquivo conforme o Guia do Aluno (seção Trabalho 1 > Desafio A).

Sistema: python ../../../app/app.py   (http://localhost:5000)
Zerar antes de cada execução:  POST http://localhost:5000/api/admin/reset

Executar (exemplo):
    $env:TIPO_TESTE="carga"; locust -f locustfile_matricula.py --host http://localhost:5000 --headless --csv ../resultados/carga --html ../resultados/carga.html
    (Linux/macOS: TIPO_TESTE=carga locust -f ...)

Dicas:
  - Cada usuário virtual deve ser um aluno diferente (20260001 ... 20260200).
  - 409 e 422 são regras de negócio: marque com resp.success() e conte à parte.
  - Verifique que nenhuma disciplina fica com vagas negativas.
  - Use o exemplo resolvido (../../solucao-professor/python/locustfile.py) como modelo de
    LoadTestShape e de verificação de SLA, mas NÃO copie: o cenário é outro.
"""
import os

from locust import HttpUser, LoadTestShape, between, task, events
from itertools import count
import random

from collections import deque
import time
import requests
from requests.exceptions import Timeout

contador = count(1)
DISCIPLINAS = {
    "SEG-19h": ["ES3", "RED"],
    "TER-19h": ["BD2"],
    "QUA-19h": ["PW2"],
    "QUI-19h": ["IHC"],
    "SEX-19h": ["EMP"],
    "QUA-21h": ["MOB"]
}

class Aluno(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.matricula = f"2026{next(contador):04d}"
        self.id_matricula = None

    @task
    # TODO: GET /api/disciplinas, validar status e conteúdo (vagas >= 0)
    def consultar_oferta(self):
        with self.client.get(
            "/api/disciplinas",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Erro ao consultar disciplinas: HTTP {response.status_code}"
                )
                return
                # response.failure(
                #     f"Erro ao consultar disciplinas: HTTP {response.status_code}"
                # )
                # return

            disciplinas = response.json()

            for disciplina in disciplinas:
                if disciplina["vagas"] < 0:
                    response.failure(
                        f"Quantidade de vagas negativa: {disciplina['codigo']}"
                    )
                    self.environment.runner.quit()
                    return

            response.success()

        self.realizar_matricula()

    # TODO: tarefa para POST /api/matriculas (tratar 201, 409, 422 e erros técnicos)
    def realizar_matricula(self):
        self.id_matricula = None

        quantidade = random.randint(1, 5)

        horarios = list(DISCIPLINAS.keys())
        horarios_escolhidos = random.sample(horarios, quantidade)

        disciplinas = [
            random.choice(DISCIPLINAS[horario])
            for horario in horarios_escolhidos
        ]

        with self.client.post(
            "/api/matriculas",
            json={
                "aluno": self.matricula,
                "disciplinas": disciplinas
            },
            catch_response=True
        ) as response:

            if response.status_code == 201:
                dados = response.json()

                if (dados.get("aluno") != self.matricula or dados.get("disciplinas") != disciplinas):
                    response.failure("Dados retornados diferentes dos enviados")
                    return

                response.success()

                self.id_matricula = dados["id"]

            elif response.status_code == 409:
                global total_409
                total_409 += 1
                response.success()

            elif response.status_code == 422:
                global total_422
                total_422 += 1
                response.success()

            else:
                response.failure(
                    f"Erro ao realizar matrícula: HTTP {response.status_code}"
                )

        if self.id_matricula is not None:
            self.baixar_comprovante()

    # TODO: tarefa para GET /api/matriculas/<id>/comprovante
    def baixar_comprovante(self):
        with self.client.get(
            f"/api/matriculas/{self.id_matricula}/comprovante",
            name="/api/matriculas/[id]/comprovante",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Erro ao consultar comprovante: HTTP {response.status_code}"
                )
                return

            dados = response.json()

            if (dados.get("aluno") != self.matricula or dados.get("id") != self.id_matricula):
                response.failure("Dados do comprovante incorretos")
                return

            response.success()


class Perfil(LoadTestShape):
    tipo = os.getenv("TIPO_TESTE", "carga")
    
    def tick(self):
        t = self.get_run_time()
        # TODO: carga (100 alunos, 2 min)
        if self.tipo == "carga":
            if self.get_current_user_count() < 100:
                return (100, 10)
            if not hasattr(self, "inicio_carga"):
                self.inicio_carga = t
            if t - self.inicio_carga < 120:
                return (100, 10)
            return None
        
        # TODO: pico (0 -> 200 em até 10 s)
        if self.tipo == "pico":
            if self.get_current_user_count() < 200:
                return (200, 40)
            if not hasattr(self, "inicio_pico"):
                self.inicio_pico = t
            if t - self.inicio_pico < 30:
                return (200, 40)
            return None
        
        # TODO: estresse (degraus até 400)
        if self.tipo == "estresse":
            degrau = (t // 30) + 1
            qtd_usuarios = 50 * degrau
            return (qtd_usuarios, 50) if qtd_usuarios <= 400 else None

        raise ValueError(f"TIPO_TESTE desconhecido: {self.tipo}")        


historico = deque() # permite, de forma mais fácil, adicionar e remover elementos das extremidades.
timeouts_consecutivos = 0

runner = None

@events.init.add_listener # esse listener faz com que a função abaixo seja executada quando o runner existir
def guardar_runner(environment, **kwargs):
    global runner 
    # runner é o objeto responsável por controlar a 
    # execução do teste: iniciar usuários, 
    # controlar a carga e encerrar a execução.
    runner = environment.runner

def monitorar_requisicoes(response = None, exception = None, **kwargs):
    global total_5xx, total_timeout
    tempo = time.monotonic()

    # contabiliza erro 5xx
    if (response is not None) and (500 <= response.status_code <= 599): 
        erro_5xx = True        
        total_5xx += 1
    else:
        erro_5xx = False

    #  contabiliza timeout
    if isinstance(exception, requests.exceptions.Timeout):
        total_timeout += 1

    # adiciona resumo da requisição no deque
    historico.append((tempo, erro_5xx))

    verificar_erros(tempo)

    verificar_timeout(exception)

# verifica percentual de erros 5xx em um janela de 30s
def verificar_erros(tempo_atual):
    while historico and tempo_atual - historico[0][0] >= 30:
        historico.popleft()

    total = len(historico)
    erros = sum(erro for horario, erro in historico)

    if total > 0:
        taxa = (erros / total) * 100

        if taxa >= 5:
            if runner is not None:
                runner.quit()


def verificar_timeout(exception):
    global timeouts_consecutivos
    if isinstance(exception, requests.exceptions.Timeout):
        timeouts_consecutivos += 1
        if timeouts_consecutivos >= 5:
            if runner is not None:
                runner.quit()
    else:
        timeouts_consecutivos = 0

events.request.add_listener(monitorar_requisicoes)

# ----- VERIFICAÇÃO DO SLA ------

SLA_P95_MS = 800
SLA_P95_COMPROVANTE_MS = 1500
SLA_ERRO_MAX = 0.01

SLA_POR_ENDPOINT_MS = {
    "/api/matriculas/[id]/comprovante": 1500
}

total_409 = 0
total_422 = 0
total_5xx = 0
total_timeout = 0


@events.quitting.add_listener
def verificar_sla(environment, **_):
    """Verifica se as métricas do teste atendem aos limites do SLA."""

    total = environment.stats.total
    reprovado = False

    if total.num_requests == 0:
        print("[SLA] REPROVADO: nenhuma requisição foi realizada.")
        environment.process_exit_code = 1
        return


    p95 = total.get_response_time_percentile(0.95)

    taxa_erro = total.fail_ratio

    print(
        f"\n[SLA] geral: p95 = {p95:.0f} ms "
        f"(limite {SLA_P95_MS}) | "
        f"erros = {taxa_erro:.2%} "
        f"(limite {SLA_ERRO_MAX:.0%})"
    )

    print(f"[SLA] Respostas HTTP 409: {total_409}")
    print(f"[SLA] Respostas HTTP 422: {total_422}")

    print(f"[SLA] Erros HTTP 5xx: {total_5xx}")
    print(f"[SLA] Timeouts: {total_timeout}")

    if p95 > SLA_P95_MS or taxa_erro >= SLA_ERRO_MAX:
        reprovado = True

    for nome, limite in SLA_POR_ENDPOINT_MS.items():
        entrada = environment.stats.entries.get((nome, "GET"))

        if entrada and entrada.num_requests:
            p95_ep = entrada.get_response_time_percentile(0.95)

            print(
                f"[SLA] {nome}: p95 = {p95_ep:.0f} ms "
                f"(limite {limite})"
            )

            if p95_ep > limite:
                reprovado = True

        if not entrada or not entrada.num_requests:
            print(f"[SLA] REPROVADO: nenhuma requisição registrada para {nome}")
            reprovado = True
            continue

    print("RESULTADO FINAL: [SLA] REPROVADO" if reprovado else "RESULTADO FINAL: [SLA] APROVADO")
    if reprovado:
        environment.process_exit_code = 1