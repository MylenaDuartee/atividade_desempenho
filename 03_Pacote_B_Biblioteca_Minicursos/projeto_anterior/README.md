# Mini-Prontuário — Testes de Desempenho

Projeto desenvolvido originalmente na disciplina de **Programação para Internet II (TEC.1052)**, do Instituto Federal do Piauí (IFPI), Campus Teresina Central, utilizado neste trabalho para a realização de testes de desempenho na disciplina de Engenharia de Software III.

O Mini-Prontuário é um sistema de prontuário eletrônico que permite o gerenciamento de pacientes e atendimentos. Neste trabalho, foi selecionada a operação de listagem de pacientes para avaliar o comportamento da API sob diferentes níveis de carga.

## 1. Tecnologias utilizadas

- **Node.js:** execução do servidor.
- **TypeScript:** desenvolvimento do backend.
- **Express:** criação da API HTTP.
- **SQLite:** banco de dados.
- **Locust:** ferramenta utilizada nos testes de desempenho.
- **Python:** linguagem utilizada para implementar os cenários de teste.

## 2. Requisitos

Para executar o projeto, são necessários:

- Node.js 22 ou superior.
- npm.
- Python instalado.
- A ferramenta Locust.

## 3. Instalação e execução do sistema

Clone o repositório e acesse a pasta do projeto:

```bash
cd projeto_anterior
```

Instale as dependências:

```bash
npm install
```

Inicie o servidor:

```bash
npm run dev
```

O servidor será disponibilizado em:

```text
http://localhost:3000
```

Para verificar se a API está funcionando, acesse:

```text
http://localhost:3000/api/health
```

A resposta esperada é:

```json
{"status":"ok"}
```

## 4. Operação selecionada para os testes

A operação selecionada foi:

```http
GET /api/patients
```

Essa rota retorna a lista de pacientes cadastrados no banco de dados.

O teste foi implementado no arquivo `locustfile_patients.py`, localizado na raiz do projeto.

Além de verificar o código HTTP 200, o script valida o conteúdo da resposta, verificando se ela é uma lista JSON e se os registros retornados possuem os campos esperados:

- `id`
- `name`
- `birthDate`
- `nationalId`
- `active`

Dessa forma, os testes verificam tanto o comportamento da aplicação quanto a integridade básica das respostas.

## 5. Instalação do Locust

Instale o Locust utilizando o pip:

```bash
python -m pip install locust
```

Para verificar a versão instalada:

```bash
python -m locust --version
```

## 6. Execução dos testes de desempenho

Antes de iniciar os testes, certifique-se de que o servidor do Mini-Prontuário está em execução.

Abra outro terminal na pasta `projeto_anterior` e execute o script com o Locust.

### Verificação inicial

```bash
python -m locust -f locustfile_patients.py --host http://127.0.0.1:3000 --headless -u 1 -r 1 -t 15s --csv verificacao --html verificacao.html
```

### Carga de referência — 5 usuários

```bash
python -m locust -f locustfile_patients.py --host http://127.0.0.1:3000 --headless -u 5 -r 1 -t 90s --stop-timeout 5s --csv referencia_r1 --html referencia_r1.html
```

Para as outras repetições, altere os sufixos para `r2` e `r3`.

### Carga nominal — 20 usuários

```bash
python -m locust -f locustfile_patients.py --host http://127.0.0.1:3000 --headless -u 20 -r 2 -t 90s --stop-timeout 5s --csv nominal_r1 --html nominal_r1.html
```

Para as outras repetições, altere os sufixos para `r2` e `r3`.

### Estresse 1 — 50 usuários

```bash
python -m locust -f locustfile_patients.py --host http://127.0.0.1:3000 --headless -u 50 -r 5 -t 90s --stop-timeout 5s --csv estresse1_r1 --html estresse1_r1.html
```

Para as outras repetições, altere os sufixos para `r2` e `r3`.

### Estresse 2 — 100 usuários

```bash
python -m locust -f locustfile_patients.py --host http://127.0.0.1:3000 --headless -u 100 -r 10 -t 90s --stop-timeout 5s --csv estresse2_r1 --html estresse2_r1.html
```

Para as outras repetições, altere os sufixos para `r2` e `r3`.

### Recuperação

Após a execução dos testes de estresse, o sistema foi submetido novamente ao patamar de 20 usuários:

```bash
python -m locust -f locustfile_patients.py --host http://127.0.0.1:3000 --headless -u 20 -r 2 -t 90s --stop-timeout 5s --csv recuperacao --html recuperacao.html
```

## 7. Perfis de carga utilizados

| Etapa | Usuários | Taxa de inicialização | Duração |
|---|---:|---:|---:|
| Verificação | 1 | 1 usuário/s | 15 segundos |
| Referência | 5 | 1 usuário/s | 90 segundos |
| Nominal | 20 | 2 usuários/s | 90 segundos |
| Estresse 1 | 50 | 5 usuários/s | 90 segundos |
| Estresse 2 | 100 | 10 usuários/s | 90 segundos |
| Recuperação | 20 | 2 usuários/s | 90 segundos |

Os patamares de referência, nominal, estresse 1 e estresse 2 foram executados em três repetições.

O tempo de espera entre as requisições foi configurado entre 0,2 e 0,6 segundo.

## 8. Resultados dos testes

Os arquivos gerados pelo Locust incluem:

- Arquivos CSV com estatísticas, histórico, falhas e exceções.
- Relatórios HTML com tabelas e gráficos dos resultados.

Os resultados devem ser armazenados na pasta `resultados/` do repositório principal, mantendo a identificação de cada execução.

As evidências visuais das execuções também devem ser organizadas nessa pasta.

## 9. Ambiente utilizado

Ambiente utilizado durante os testes:

| Componente | Configuração |
|---|---|
| Sistema operacional | Windows 11 |
| Processador | Intel Core i5-13420H, 13ª geração |
| Memória RAM | 8 GB LPDDR5 |
| Node.js | v22.23.2 |
| Python | v3.14.3 |
| Locust | v2.47.0 |
| Banco de dados | SQLite |

A aplicação e o gerador de carga foram executados na mesma máquina.

## 10. Observações

- O servidor deve permanecer em execução durante os testes.
- Os testes devem ser realizados com a aplicação disponível em `http://127.0.0.1:3000`.
- A operação selecionada realiza consultas, sem modificar os registros de pacientes.
- Os resultados devem ser preservados para permitir a análise e a comparação entre as execuções.
- As análises, metas, gráficos, limitações e recomendações estão documentados no relatório de desempenho do trabalho.

