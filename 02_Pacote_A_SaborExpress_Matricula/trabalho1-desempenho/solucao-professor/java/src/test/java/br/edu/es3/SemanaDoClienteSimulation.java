package br.edu.es3;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.ClosedInjectionStep;
import io.gatling.javaapi.core.PopulationBuilder;
import io.gatling.javaapi.core.ScenarioBuilder;
import io.gatling.javaapi.core.Simulation;
import io.gatling.javaapi.http.HttpProtocolBuilder;

import java.time.Duration;
import java.util.List;

/**
 * Trabalho Prático 1 - SITUAÇÃO RESOLVIDA PELO PROFESSOR (versão Java/Gatling)
 * "Semana do Cliente" da lanchonete Sabor Express.
 *
 * Escolha o tipo de teste com -Dtipo=carga | estresse | pico | resistencia
 *   mvn gatling:test -Dtipo=carga
 *   mvn gatling:test -Dtipo=estresse
 *
 * Antes de cada execução: curl -X POST http://localhost:5000/api/admin/reset
 */
public class SemanaDoClienteSimulation extends Simulation {

    static final String TIPO = System.getProperty("tipo", "carga");

    HttpProtocolBuilder httpProtocol = http
            .baseUrl("http://localhost:5000")
            .acceptHeader("application/json")
            .contentTypeHeader("application/json");

    /** 90% dos usuários: consultam o cardápio, pedem e acompanham o pedido. */
    ScenarioBuilder clientes = scenario("Cliente do app")
            .exec(http("GET /api/cardapio").get("/api/cardapio").check(status().is(200)))
            .pause(1, 3)
            .exec(http("POST /api/pedidos").post("/api/pedidos")
                    .body(StringBody("{\"cliente\":\"gatling\",\"itens\":[{\"id\":1,\"qtd\":2},{\"id\":5,\"qtd\":1}]}"))
                    .check(status().is(201))
                    .check(jsonPath("$.id").saveAs("pedidoId")))   // guarda o id para usar depois
            .pause(1, 3)
            .exec(http("GET /api/pedidos/[id]").get("/api/pedidos/#{pedidoId}")
                    .check(status().is(200))
                    .check(jsonPath("$.status").is("recebido")));

    /** 10% dos usuários: o gerente olhando o relatório de vendas. */
    ScenarioBuilder gerentes = scenario("Gerente")
            .exec(http("GET /api/relatorio/vendas").get("/api/relatorio/vendas").check(status().is(200)))
            .pause(2, 5);

    /** Curva de usuários simultâneos para um "total" de usuários. */
    static List<ClosedInjectionStep> perfil(double fracao) {
        int u = (int) Math.max(1, Math.round(fracao * 50));
        switch (TIPO) {
            case "estresse":
                // degraus de +25 usuários (total) a cada 30 s, até 250
                int passo = (int) Math.max(1, Math.round(fracao * 25));
                return List.of(incrementConcurrentUsers(passo).times(10)
                        .eachLevelLasting(Duration.ofSeconds(30))
                        .startingFrom(passo));
            case "pico":
                int base = (int) Math.max(1, Math.round(fracao * 10));
                int topo = (int) Math.max(1, Math.round(fracao * 150));
                return List.of(
                        constantConcurrentUsers(base).during(Duration.ofSeconds(30)),
                        rampConcurrentUsers(base).to(topo).during(Duration.ofSeconds(1)),
                        constantConcurrentUsers(topo).during(Duration.ofSeconds(30)),
                        rampConcurrentUsers(topo).to(base).during(Duration.ofSeconds(3)),
                        constantConcurrentUsers(base).during(Duration.ofSeconds(30)));
            case "resistencia":
                int r = (int) Math.max(1, Math.round(fracao * 40));
                return List.of(constantConcurrentUsers(r).during(Duration.ofMinutes(15)));
            default: // carga
                return List.of(
                        rampConcurrentUsers(0).to(u).during(Duration.ofSeconds(10)),
                        constantConcurrentUsers(u).during(Duration.ofMinutes(2)));
        }
    }

    {
        PopulationBuilder popClientes = clientes.injectClosed(perfil(0.9));
        PopulationBuilder popGerentes = gerentes.injectClosed(perfil(0.1));

        setUp(popClientes, popGerentes)
                .protocols(httpProtocol)
                .assertions(
                        // SLA: p95 < 500 ms e menos de 1% de erros
                        global().responseTime().percentile(95.0).lt(500),
                        global().failedRequests().percent().lt(1.0),
                        // o relatório tem um SLA próprio, mais tolerante
                        details("GET /api/relatorio/vendas").responseTime().percentile(95.0).lt(2000)
                );
    }
}
