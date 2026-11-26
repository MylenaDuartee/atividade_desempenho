"""
Alternativa ao Selenium: o MESMO teste com Playwright (Python).

    pip install pytest-playwright
    playwright install chromium
    pytest test_login_playwright.py            (--headed para ver o navegador)

O Playwright espera automaticamente o elemento estar pronto (auto-wait)
e o expect() repete a verificação até o tempo limite.
"""
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5000"


def test_login_valido_leva_ao_cardapio(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("#usuario", "aluno")
    page.fill("#senha", "123456")
    page.click("#btn-entrar")
    expect(page.locator("h1")).to_have_text("Cardápio")
    expect(page.locator("#usuario-logado")).to_have_text("aluno")


def test_login_invalido_mostra_mensagem(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("#usuario", "aluno")
    page.fill("#senha", "errada")
    page.click("#btn-entrar")
    expect(page.get_by_test_id("erro")).to_have_text("Usuário ou senha inválidos.")
