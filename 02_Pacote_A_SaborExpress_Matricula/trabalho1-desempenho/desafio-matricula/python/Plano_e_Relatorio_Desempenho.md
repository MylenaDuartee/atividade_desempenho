# Plano e Relatório de Teste de Desempenho

Equipe: **\*\*\*\***\_\_\_\_**\*\*\*\*** Pacote/Projeto: **\*\*\*\***\_\_\_\_**\*\*\*\*** Data: **_/_**/\_\_\_\_

## 1. Plano (preencher ANTES de executar)

| Item                              | Preenchimento                                                    |
| --------------------------------- | ---------------------------------------------------------------- |
| Pergunta / hipótese               | Ex.: "Com 20 usuários, a consulta de cursos atende p95 ≤ 500 ms" |
| Operações testadas e proporção    | Ex.: GET /api/cursos 70%, GET /api/cursos/1 30%                  |
| Verificações de conteúdo          | Ex.: status 200, total = 3, nome = Python                        |
| Think time (pausa entre ações)    | Ex.: 0,2 a 0,6 s                                                 |
| Massa de dados                    | Ex.: um aluno diferente por usuário virtual                      |
| Perfis (usuários, ritmo, duração) | Carga: **_ Estresse: _** Pico: **_ Recuperação: _**              |
| Repetições                        | Ex.: 3 por patamar                                               |
| Metas (SLA)                       | p95 ≤ **_ ms; falhas ≤ _** %; outras: \_\_\_                     |
| Critério de parada                | Ex.: falhas > 20% por 10 s ou p95 > 2000 ms por 10 s             |

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

Será utilizado um intervalo aleatório de 0,2 a 0,6 segundo entre as operações da jornada, simulando pequenas pausas entre as ações do aluno.

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

## 2. Ambiente

| Item                                          | Valor |
| --------------------------------------------- | ----- |
| Processador / memória                         |       |
| Sistema operacional                           |       |
| Python ou JDK (versão)                        |       |
| Ferramenta e versão (Locust/Gatling)          |       |
| Servidor e gerador de carga na mesma máquina? |       |

## 3. Resultados

Preencha `Modelo_Registro_Resultados_Desempenho.csv` com uma linha por execução e
cole aqui a tabela-resumo e os gráficos (p95, req/s e falhas por patamar).

## 4. Análise

- A meta foi atendida em cada teste? Em qual patamar deixou de ser?
- Qual endpoint piora primeiro? A vazão parou de crescer em algum ponto?
- O sistema se recuperou após o estresse? Em quanto tempo?
- As repetições deram resultados parecidos? O que explica as diferenças?

## 5. Limitações e recomendações

-
