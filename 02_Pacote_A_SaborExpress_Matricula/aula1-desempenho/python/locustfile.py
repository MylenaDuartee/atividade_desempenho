"""
Exemplo da Aula 1 - Teste de CARGA com Locust (Python)

Cenário: clientes da lanchonete "Sabor Express" consultam o cardápio
e, de vez em quando, fazem um pedido.

Pré-requisitos:
    pip install locust
    python ../../app/app.py            (em outro terminal)

Execução com interface web (http://localhost:8089):
    locust -f locustfile.py --host http://localhost:5000

Execução sem interface (ideal para registrar evidências):
    locust -f locustfile.py --host http://localhost:5000 \
           --headless -u 50 -r 5 -t 1m --csv resultados/carga --html resultados/carga.html

    -u 50 : 50 usuários simultâneos
    -r 5  : 5 novos usuários por segundo (rampa de subida)
    -t 1m : duração de 1 minuto
"""
import random

from locust import HttpUser, between, task


class ClienteLanchonete(HttpUser):
    # Tempo de "pensar" entre uma ação e outra (simula pessoa real)
    wait_time = between(1, 3)

    @task(3)  # peso 3: consultar o cardápio é 3x mais comum que pedir
    def ver_cardapio(self):
        with self.client.get("/api/cardapio", name="GET /api/cardapio",
                             catch_response=True) as resp:
            if resp.status_code != 200 or len(resp.json()) == 0:
                resp.failure("Cardápio indisponível ou vazio")

    @task(1)
    def fazer_pedido(self):
        pedido = {
            "cliente": f"cliente-{random.randint(1, 10_000)}",
            "itens": [{"id": random.randint(1, 6), "qtd": random.randint(1, 3)}],
        }
        with self.client.post("/api/pedidos", json=pedido, name="POST /api/pedidos",
                              catch_response=True) as resp:
            if resp.status_code != 201:
                resp.failure(f"Esperava 201, recebeu {resp.status_code}")
            elif resp.elapsed.total_seconds() > 0.5:
                # Critério de aceitação: pedido deve ser gravado em até 500 ms
                resp.failure("Pedido demorou mais que 500 ms")
