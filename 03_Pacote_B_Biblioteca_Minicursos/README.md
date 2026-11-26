# Pacote B — Biblioteca e Minicursos

Este pacote contém um exemplo funcional, alternativas Java e o desafio de testes para a aplicação Biblioteca e Minicursos.

## Estrutura

- `exemplo/`: exemplo funcional de login e testes de referência em Java.
- `desafio/`: aplicação web, testes funcionais e scripts de desempenho do desafio.
- `conftest.py`: configuração compartilhada do Selenium para os testes deste pacote.

## Iniciar a aplicação do desafio

Na pasta deste pacote:

```bash
cd desafio
python -m pip install -r requirements.txt
python app.py
```

A aplicação fica disponível em `http://127.0.0.1:8000`.

## Executar o exemplo funcional

Com a aplicação iniciada, a partir da pasta deste pacote:

```bash
python -m pytest exemplo/funcionais/test_login.py -v
```

## Executar o desafio de desempenho

Com a aplicação iniciada e Locust instalado:

```bash
python -m locust -f desafio/desempenho/desafio_locust.py --host http://127.0.0.1:8000
```

Os resultados existentes estão em [`../resultados/03_Pacote_B_Biblioteca_Minicursos/`](../resultados/03_Pacote_B_Biblioteca_Minicursos/). O plano e relatório do desafio estão em `desafio/Relatorio_Desempenho_Desafio_B.md`.
