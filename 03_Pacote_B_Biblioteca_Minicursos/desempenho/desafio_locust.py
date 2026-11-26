"""Novo desafio: complete as tarefas e as verificações conforme o roteiro.
Mistura exigida: 70% de listagem e 30% de detalhe em expectativa.
O peso define probabilidade, não uma proporção exata por execução.
"""
from locust import HttpUser, between, task

class Visitante(HttpUser):
    wait_time = between(0.2, 0.6)

    @task(7)
    def listar_cursos(self):
        with self.client.get("/api/cursos", name="listar_cursos",
                             catch_response=True, timeout=5) as r:
            if r.status_code != 200:
                r.failure(f"HTTP {r.status_code}")
                return
            try:
                d = r.json()
                nomes = [c["nome"] for c in d["itens"]]
                if d["total"] != 3:
                    r.failure(f"total esperado 3, veio {d['total']}")
                elif "Python" not in nomes:
                    r.failure("curso Python ausente")
            except (ValueError, KeyError, TypeError):
                r.failure("Resposta inválida")

    @task(3)
    def detalhe_curso(self):
        with self.client.get("/api/cursos/1", name="detalhe_curso",
                             catch_response=True, timeout=5) as r:
            if r.status_code != 200:
                r.failure(f"HTTP {r.status_code}")
                return
            try:
                d = r.json()
                if d["id"] != 1 or d["nome"] != "Python" or d["vagas"] != 2:
                    r.failure(f"conteúdo inesperado: {d}")
            except (ValueError, KeyError, TypeError):
                r.failure("Resposta inválida")