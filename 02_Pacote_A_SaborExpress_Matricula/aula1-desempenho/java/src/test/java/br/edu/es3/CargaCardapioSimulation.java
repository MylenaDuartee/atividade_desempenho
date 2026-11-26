package br.edu.es3;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.ScenarioBuilder;
import io.gatling.javaapi.core.Simulation;
import io.gatling.javaapi.http.HttpProtocolBuilder;

import java.time.Duration;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Exemplo da Aula 1 - Teste de CARGA com Gatling (Java DSL).
 *
 * Cenário: clientes da lanchonete consultam o cardápio, "pensam" de 1 a 3 s
 * e fazem um pedido. Mantemos 50 usuários simultâneos por 1 minuto.
 *
 * Critérios de aceitação (viram "assertions" e reprovam a execução):
 *   - 95% das requisições em até 500 ms (p95 < 500 ms)
 *   - menos de 1% de erros
 */
public class CargaCardapioSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
            .baseUrl("http://localhost:5000")
            .acceptHeader("application/json")
            .contentTypeHeader("application/json");

    ScenarioBuilder clientes = scenario("Clientes da lanchonete")
            .exec(http("GET /api/cardapio")
                    .get("/api/cardapio")
                    .check(status().is(200))
                    .check(jsonPath("$[0].nome").exists()))
            .pause(1, 3) // tempo de "pensar", em segundos
            .exec(session -> session.set("item", ThreadLocalRandom.current().nextInt(1, 7)))
            .exec(http("POST /api/pedidos")
                    .post("/api/pedidos")
                    .body(StringBody("{\"cliente\":\"gatling\",\"itens\":[{\"id\":#{item},\"qtd\":1}]}"))
                    .check(status().is(201)));

    {
        setUp(
            clientes.injectClosed(
                // rampa: de 0 a 50 usuários simultâneos em 10 s
                rampConcurrentUsers(0).to(50).during(Duration.ofSeconds(10)),
                // patamar: mantém 50 usuários simultâneos por 50 s
                constantConcurrentUsers(50).during(Duration.ofSeconds(50))
            )
        )
        .protocols(httpProtocol)
        .assertions(
            global().responseTime().percentile(95.0).lt(500),
            global().failedRequests().percent().lt(1.0)
        );
    }
}
