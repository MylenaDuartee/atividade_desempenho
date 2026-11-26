# Plano e Relatório de Testes de Desempenho

## Sistema Matrícula Acadêmica

**Equipe:** Kamila Rocha | Mylena Duarte | Vitória Barbosa
**Pacote/Projeto:** Pacote 2 - Sabor Express
**Data:** 25/11/2026

---

## 1. Plano de Teste (Preenchido antes da execução)

| Item                                  | Preenchimento                                                                                                                                                                             |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pergunta / hipótese**               | Com 100 usuários simultâneos durante 2 minutos, o sistema de matrículas atende ao p95 geral ≤ 800 ms, ao p95 do comprovante ≤ 1.500 ms e mantém erros técnicos < 1%, sem vagas negativas? |
| **Operações testadas e proporção**    | Jornada sequencial por usuário: `GET /api/disciplinas` → `POST /api/matriculas` → `GET /api/matriculas/{id}/comprovante` (condicional ao HTTP 201)                                        |
| **Verificações de conteúdo**          | Status HTTP esperado (200/201), ausência de vagas negativas, presença e correspondência de ID da matrícula, aluno, disciplinas e código do comprovante                                    |
| **Think time (pausa entre ações)**    | 0,2 a 0,6 s (planejado) / 1 a 3 s (executado na simulação)                                                                                                                                |
| **Massa de dados**                    | Um aluno exclusivo por usuário virtual via variável `ALUNOS` (200 identificadores válidos cadastrados: `20260001` a `20260200`)                                                           |
| **Perfis (usuários, ritmo, duração)** | **Carga:** 100 usuários, spawn 10/s, duração 2 min \| **Pico:** 200 usuários, spawn 40/s (~5 s) \| **Estresse:** até 400 usuários (degraus de +50 a cada 30 s)                            |
| **Repetições**                        | 3 execuções sequenciais por cenário, com restauração do ambiente entre execuções                                                                                                          |
| **Metas (SLA)**                       | p95 geral ≤ 800 ms; p95 comprovante ≤ 1.500 ms; erros técnicos < 1%; nenhuma vaga negativa                                                                                                |
| **Critério de parada**                | Erros HTTP 5xx ≥ 5% em janela de 30 s; 5 timeouts consecutivos; ou ocorrência imediata de vagas negativas                                                                                 |

### 1.1. Pergunta / Hipótese

Com 100 usuários simultâneos durante 2 minutos, o sistema de matrículas atende ao p95 geral de até 800 ms, ao p95 do comprovante de até 1.500 ms e mantém a taxa de erros técnicos abaixo de 1%, sem apresentar vagas negativas?

### 1.2. Operações testadas e proporção

Será simulada a jornada de um aluno realizando as seguintes operações:

1. **Consultar disciplinas:** `GET /api/disciplinas`
2. **Realizar matrícula:** `POST /api/matriculas`
3. **Consultar comprovante:** `GET /api/matriculas/{id}/comprovante`

Cada usuário virtual realizará uma consulta de disciplinas e uma tentativa de matrícula. Caso a matrícula seja realizada com sucesso (HTTP 201), o usuário consultará o comprovante utilizando o ID retornado pela operação de matrícula.

A consulta ao comprovante será, portanto, condicional ao sucesso da matrícula.

Essa sequência foi escolhida por representar o fluxo de utilização esperado pelo aluno.

### 1.3. Verificações de conteúdo das respostas

#### GET /api/disciplinas

- Verificar se o status HTTP é 200.
- Verificar se o corpo da resposta contém as disciplinas com código, horário e quantidade de vagas restantes.
- Verificar se a quantidade de vagas restantes nunca é negativa.

#### POST /api/matriculas

- Quando o status for 201, verificar se a resposta contém o ID da matrícula, o aluno, as disciplinas solicitadas e o código do comprovante.
- Verificar se os dados retornados correspondem aos dados enviados na requisição.
- Considerar as respostas 409 e 422 como respostas de regras de negócio, não como erros técnicos.

#### GET /api/matriculas/{id}/comprovante

- Verificar se o status HTTP é 200.
- Verificar se o ID, o aluno e o código do comprovante correspondem à matrícula realizada anteriormente.

### 1.4. Think time

Será utilizado um intervalo aleatório de 1 a 3 segundos entre as operações da jornada, simulando pequenas pausas entre as ações do aluno.

### 1.5. Massa de dados

- Serão utilizados alunos previamente cadastrados no servidor, por meio da variável `ALUNOS`.
- Cada usuário virtual utilizará uma matrícula exclusiva, sem compartilhamento entre usuários simultâneos.
- As combinações de disciplinas serão selecionadas aleatoriamente entre opções previamente definidas, respeitando os horários e as regras de matrícula.
- A distribuição das combinações deverá considerar a disponibilidade de vagas.
- Para testes com mais de 200 usuários, será necessário disponibilizar alunos suficientes no ambiente de teste.

### 1.6. Perfis de carga

#### Teste de carga

- Usuários virtuais: 100.
- Taxa de inicialização (_spawn rate_): 10 usuários por segundo.
- Duração: 2 minutos após atingir os 100 usuários.

#### Teste de pico

- Usuários virtuais: 200.
- Taxa de inicialização (_spawn rate_): 40 usuários por segundo.
- Tempo previsto para atingir os 200 usuários: aproximadamente 5 segundos.

#### Teste de estresse

- Limite máximo: 400 usuários virtuais.
- Aumento gradual da carga em degraus de 50 usuários a cada 30 segundos até atingir o limite máximo.
- Objetivo: identificar a partir de qual quantidade de usuários o sistema começa a apresentar degradação de desempenho ou falhas.
- O teste poderá ser interrompido antecipadamente conforme os critérios de parada estabelecidos.

### 1.7. Repetições

Cada cenário de teste será executado 3 vezes, sequencialmente, mantendo as mesmas configurações e condições iniciais.

Serão realizadas:

- 3 execuções do teste de carga.
- 3 execuções do teste de pico.
- 3 execuções do teste de estresse.

Entre as execuções, o ambiente deverá ser restaurado às condições iniciais, incluindo a disponibilidade de vagas e os dados necessários para o teste.

### 1.8. Metas (SLA)

As seguintes metas serão utilizadas na avaliação dos três cenários:

- **p95 geral:** menor ou igual a 800 ms.
- **p95 do comprovante:** menor ou igual a 1.500 ms.
- **Taxa de erros técnicos:** inferior a 1%.
- **Integridade das vagas:** nenhuma disciplina poderá apresentar quantidade de vagas negativa.

As respostas HTTP 409 e 422 representam regras de negócio e não serão contabilizadas como erros técnicos.

Erros HTTP 5xx e timeouts serão contabilizados como erros técnicos.

### 1.9. Critérios de parada

O teste será interrompido antecipadamente caso ocorra alguma das seguintes situações:

1. **Erros HTTP 5xx:** taxa igual ou superior a 5% das requisições em uma janela de 30 segundos.
2. **Timeouts:** ocorrência de 5 timeouts consecutivos.
3. **Integridade das vagas:** qualquer disciplina apresentar quantidade de vagas negativa. Nesse caso, a interrupção será imediata.

---

## 2. Ambiente de Teste

| Item                                 | Configuração                           |
| ------------------------------------ | -------------------------------------- |
| Computador                           | Lenovo LOQ 15IRX9                      |
| Processador                          | Intel Core i5-13450HX                  |
| Memória RAM                          | 16 GB                                  |
| Sistema operacional                  | Windows 11 25H2                        |
| Ferramenta                           | Locust                                 |
| Aplicação                            | Flask – Matrícula Acadêmica            |
| Banco de dados                       | Não utiliza; dados mantidos em memória |
| Servidor e gerador na mesma máquina? | Sim (execução local)                   |

---

## 3. Perfil de Utilização Executado (Observações da Simulação)

Na execução prática da simulação, cada usuário virtual recebeu um identificador próprio e seguiu o fluxo planejado (consulta de disciplinas, seleção de até cinco disciplinas sem conflito de horário, solicitação de matrícula e consulta condicional do comprovante).

- **Ajuste de _think time_:** O intervalo de espera entre as tarefas aplicado na execução foi de **1 a 3 segundos** (diferente do intervalo de 0,2 a 0,6 s inicialmente previsto no plano).
- **Limitação dos dados de teste:** A aplicação disponibiliza apenas 200 identificadores de alunos válidos, de `20260001` a `20260200`. Assim, cenários com mais de 200 usuários virtuais podem gerar HTTP 401 quando os identificadores ultrapassam essa faixa. Essas respostas não representam, por si só, um limite de 200 matrículas simultâneas: decorrem da quantidade de alunos cadastrados para a simulação.

---

## 4. Resultados

Os resultados abaixo correspondem às execuções realizadas até o momento. Foi gerada a saída CSV do Locust para registro das estatísticas.

### 4.1. Teste de carga — 100 usuários por 2 minutos

**Resultado: reprovado no SLA do comprovante.**

| Endpoint                               | Requisições | Falhas | Tempo médio |      p95 |
| -------------------------------------- | ----------: | -----: | ----------: | -------: |
| GET `/api/disciplinas`                 |       5.827 |      0 |       38 ms |    69 ms |
| POST `/api/matriculas`                 |       5.825 |      0 |       69 ms |   100 ms |
| GET `/api/matriculas/[id]/comprovante` |          97 |      0 |    4.589 ms | 9.700 ms |

**Estatísticas gerais:**

- Requisições: 11.749
- Vazão: 89,68 requisições/s
- p95 geral: 100 ms
- Taxa de falhas registrada: 0%
- HTTP 409: 5.728
- HTTP 422: 0
- HTTP 5xx: 0
- Timeouts: 0

O p95 geral ficou abaixo do limite de 800 ms e não foram observados erros técnicos. Entretanto, o p95 da geração de comprovantes foi de 9.700 ms, ultrapassando o limite de 1.500 ms. Portanto, o sistema não atendeu integralmente ao SLA.

### 4.2. Teste de pico — aumento rápido para 200 usuários

**Resultado: reprovado no SLA do comprovante.**

| Endpoint                               | Requisições | Falhas | Tempo médio |       p95 |
| -------------------------------------- | ----------: | -----: | ----------: | --------: |
| GET `/api/disciplinas`                 |       2.473 |      0 |       68 ms |    160 ms |
| POST `/api/matriculas`                 |       2.467 |      0 |      100 ms |    180 ms |
| GET `/api/matriculas/[id]/comprovante` |         130 |      0 |   11.215 ms | 17.000 ms |

**Estatísticas gerais:**

- Requisições: 5.070
- Vazão: 142,17 requisições/s
- p95 geral: 200 ms
- Taxa de falhas registrada: 0%
- HTTP 409: 2.337
- HTTP 422: 0
- HTTP 5xx: 0
- Timeouts: 0

O sistema manteve o p95 geral dentro do limite e não apresentou falhas nas requisições. Porém, o p95 dos comprovantes chegou a 17.000 ms, muito acima do limite de 1.500 ms.

Em comparação com o teste de carga, o tempo de resposta dos comprovantes aumentou. Isso indica que essa operação é especialmente sensível ao aumento da concorrência.

### 4.3. Teste de estresse — aumento progressivo até 400 usuários

**Resultado: reprovado.**

| Endpoint                               | Requisições | Falhas | Tempo médio |      p95 |
| -------------------------------------- | ----------: | -----: | ----------: | -------: |
| GET `/api/disciplinas`                 |      19.559 |      1 |      235 ms | 1.200 ms |
| POST `/api/matriculas`                 |      19.394 |  4.630 |      494 ms | 2.000 ms |
| GET `/api/matriculas/[id]/comprovante` |         125 |      0 |    2.592 ms | 7.300 ms |

**Estatísticas gerais finais:**

- Requisições: 39.078
- Falhas: 4.631 (11,85%)
- Tempo médio geral: 371 ms
- p95 geral: 1.700 ms
- HTTP 409: 14.639
- HTTP 422: 0
- HTTP 5xx: 0
- Timeouts contabilizados: 0

A maior parte das falhas foi composta por **4.628 respostas HTTP 401** no endpoint de matrícula. Isso ocorreu porque o teste ultrapassou os 200 identificadores de alunos válidos cadastrados na aplicação. Também foram registradas três falhas de conexão (HTTP 0): duas no endpoint de matrícula e uma na consulta de disciplinas.

O p95 geral ultrapassou o limite de 800 ms. A consulta de disciplinas também atingiu p95 de 1.200 ms, enquanto o endpoint de matrícula apresentou p95 de 2.000 ms. O resultado indica degradação sob estresse, mas a taxa total de falhas precisa ser interpretada considerando a limitação dos dados de teste: a maioria dos erros foi causada por identificadores inexistentes, e não por respostas HTTP 5xx.

---

## 5. Análise dos Resultados

### 5.1. Endpoint mais sensível

O endpoint de geração de comprovantes apresentou o maior tempo de resposta nos três cenários:

- **Carga:** p95 de 9.700 ms.
- **Pico:** p95 de 17.000 ms.
- **Estresse:** p95 de 7.300 ms.

A implementação da aplicação utiliza um bloqueio (`lock`) durante a geração do PDF e mantém uma espera de 250 ms dentro da região protegida. Como consequência, as gerações de comprovantes são serializadas: enquanto uma requisição está gerando o documento, as demais precisam aguardar a liberação do bloqueio.

Esse comportamento é compatível com os tempos elevados observados, especialmente nos testes de carga e pico. O comprovante é, portanto, o principal gargalo de desempenho identificado.

### 5.2. Comportamento dos demais endpoints

No teste de carga, a consulta de disciplinas e a realização de matrículas apresentaram p95 baixo e nenhuma falha.

No teste de pico, esses dois endpoints continuaram dentro do limite geral. Já no teste de estresse, houve aumento expressivo nos tempos de resposta: o p95 da consulta chegou a 1.200 ms e o da matrícula a 2.000 ms.

### 5.3. Integridade das vagas

A simulação verifica se a quantidade de vagas retornada pela consulta de disciplinas é negativa. Não foi registrado resultado indicando vagas negativas durante as execuções analisadas.

### 5.4. Limitações da avaliação

- **Massa de alunos:** A quantidade de alunos válidos está limitada a 200 identificadores. Por isso, no teste de estresse, parte significativa das falhas foi causada por HTTP 401, devido à geração de identificadores além dos cadastrados. Essa limitação reduz a capacidade de avaliar exclusivamente a taxa de erros técnicos em cargas superiores a 200 usuários. Para uma avaliação mais precisa nesse cenário, seria necessário ampliar os dados de alunos válidos ou ajustar a geração de identificadores, sem alterar as regras funcionais da aplicação.

---

## 6. Conclusão

O sistema apresentou comportamento satisfatório nos endpoints de consulta e matrícula durante o teste de carga e o teste de pico, sem erros técnicos registrados. Entretanto, **não atendeu ao SLA de geração de comprovantes em nenhum dos cenários**, devido aos tempos de resposta elevados.

No teste de estresse, houve degradação adicional dos endpoints de consulta e matrícula. A interpretação da taxa de falhas deve considerar que a maioria dos erros foi causada pela quantidade limitada de identificadores de alunos válidos.

O principal gargalo identificado foi a geração de comprovantes, cujo mecanismo de bloqueio serializa as solicitações. Os resultados mostram que essa operação precisa de atenção prioritária em uma futura otimização.
