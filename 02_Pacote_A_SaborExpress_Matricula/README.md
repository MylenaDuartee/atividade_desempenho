# Pacote A — Sabor Express e Matrícula

Este pacote reúne os exemplos de aula e o desafio de matrícula. O sistema usado nos exercícios fica em `app/`.

## Estrutura

- `exemplo/aula1-desempenho/`: exemplo de desempenho com Locust e Gatling.
- `exemplo/aula2-funcionalidades/`: exemplos de testes funcionais com Selenium, Playwright e JUnit.
- `exemplo/solucao-professor/`: solução de referência e seus resultados.
- `desafio/java/` e `desafio/python/`: materiais do desafio de matrícula.
- `../resultados/02_Pacote_A_SaborExpress_Matricula/`: resultados de desempenho do desafio.

## Iniciar o sistema

Na pasta deste pacote:

```bash
cd app
python -m pip install -r requirements.txt
python app.py
```

O sistema fica disponível em `http://localhost:5000`. Os READMEs e instruções dentro de cada exemplo explicam como executar os testes correspondentes.

## Requisitos

- Python 3.10 ou superior.
- JDK 17 e Maven 3.9 ou superior para os exemplos Java.
- Chrome para testes Selenium.

O roteiro geral da disciplina está em [`00_LEIA-ME_Guia_do_Aluno.pdf`](../00_LEIA-ME_Guia_do_Aluno.pdf).
