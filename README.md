# Trabalho de Testes Funcionais e de Desempenho

Repositório organizado por pacotes, preservando seus nomes originais.

## Estrutura

```text
02_Pacote_A_SaborExpress_Matricula/
  exemplo/
  desafio/
03_Pacote_B_Biblioteca_Minicursos/
  exemplo/
  desafio/
projeto_anterior/
  funcionais/
resultados/
  02_Pacote_A_SaborExpress_Matricula/
  03_Pacote_B_Biblioteca_Minicursos/
  projeto_anterior/
Modelo_Matriz_Casos_de_Teste.csv
Modelo_Registro_Resultados_Desempenho.csv
00_LEIA-ME_Guia_do_Aluno.pdf
```

Cada pacote tem um README com os comandos específicos. `exemplo/` guarda referências e atividades de aula; `desafio/` guarda os materiais dos trabalhos. Os testes do projeto anterior e suas evidências ficam separados dos pacotes atuais.

## Aplicações

**Pacote A — Sabor Express e Matrícula** (Python; porta 5000):

```bash
cd 02_Pacote_A_SaborExpress_Matricula/app
python -m pip install -r requirements.txt
python app.py
```

**Pacote B — Biblioteca e Minicursos** (Python; porta 8000):

```bash
cd 03_Pacote_B_Biblioteca_Minicursos/desafio
python -m pip install -r requirements.txt
python app.py
```

**Projeto anterior — Mini-Prontuário** (Node.js; porta 3000):

```bash
cd projeto_anterior
npm install
npm run db:reset
npm run dev
```

## Testes funcionais do projeto anterior

Com o Mini-Prontuário rodando e o Chrome instalado, em outro terminal:

```bash
python -m pip install selenium pytest
python -m pytest projeto_anterior/funcionais -v
```

O Selenium Manager pode precisar de internet na primeira execução para localizar o driver do Chrome. Os detalhes e opções estão em `projeto_anterior/funcionais/README.md`.

## Resultados e versões registradas

Os CSVs, relatórios HTML e evidências disponíveis estão organizados em `resultados/`. Os arquivos `Modelo_*.csv` são modelos para preencher, não resultados de execução.

O relatório de desempenho do Pacote B registra a equipe Kamila Rocha, Vitória Barbosa e Mylena Duarte, Python 3.14.3 e Locust 2.47.0. As faixas de dependências Selenium, pytest e Locust estão nos arquivos `requirements.txt` de cada pacote.
