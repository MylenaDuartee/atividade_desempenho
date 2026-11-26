# Testes funcionais do Mini-Prontuário

Os testes cobrem cadastro de pacientes e registro de atendimentos pela interface web. Há cenários de sucesso, rejeição de dados inválidos ou duplicados e a regra de mostrar apenas pacientes ativos.

## Executar

Em um terminal, na pasta `projeto_anterior`:

```bash
npm install
npm run db:reset
npm run dev
```

Em outro terminal, instale o Selenium e o pytest e execute:

```bash
python -m pip install selenium pytest
python -m pytest funcionais -v
```

O Chrome precisa estar instalado. O Selenium Manager localiza o driver automaticamente. Para usar outro endereço, defina `BASE_URL`; para execução visível, defina `HEADLESS=0`.

Se um teste falhar, uma captura de tela será salva em `funcionais/evidencias/`.
