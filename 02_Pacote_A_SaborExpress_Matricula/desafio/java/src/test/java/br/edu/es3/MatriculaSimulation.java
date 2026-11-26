package br.edu.es3;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.ScenarioBuilder;
import io.gatling.javaapi.core.Simulation;
import io.gatling.javaapi.http.HttpProtocolBuilder;

import java.time.Duration;

/**
 * DESAFIO A - Trabalho 1: abertura da matrícula 2026.2 (Gatling / Java).
 * Complete conforme o Guia do Aluno (Trabalho 1 > Desafio A).
 *
 * Executar: mvn gatling:test -Dtipo=carga   (ou pico, estresse)
 * Antes de cada execução: POST http://localhost:5000/api/admin/reset
 *
 * Dicas: use um feeder para dar um aluno diferente a cada usuário virtual;
 * aceite 409/422 como resultado de regra de negócio (status().in(201, 409, 422));
 * crie assertions para o p95 geral e para o p95 do comprovante.
 * Modelo: ../../solucao-professor/java/.../SemanaDoClienteSimulation.java
 */
public class MatriculaSimulation extends Simulation {

    static final String TIPO = System.getProperty("tipo", "carga");

    HttpProtocolBuilder httpProtocol = http
            .baseUrl("http://localhost:5000")
            .acceptHeader("application/json")
            .contentTypeHeader("application/json");

    ScenarioBuilder alunos = scenario("Aluno na abertura da matrícula")
            .exec(http("GET /api/disciplinas").get("/api/disciplinas").check(status().is(200)));
            // TODO: POST /api/matriculas e GET /api/matriculas/#{id}/comprovante

    {
        // TODO: escolher o perfil conforme TIPO e adicionar as assertions do SLA
        setUp(alunos.injectClosed(constantConcurrentUsers(1).during(Duration.ofSeconds(10))))
                .protocols(httpProtocol);
    }
}
