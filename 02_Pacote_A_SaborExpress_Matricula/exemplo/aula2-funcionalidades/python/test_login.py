"""
Exemplo da Aula 2 - Teste funcional automatizado com Selenium + pytest

Pré-requisitos:
    pip install selenium pytest
    python ../../app/app.py         (em outro terminal)

Executar:
    pytest -v                       (abre o Chrome)
    HEADLESS=1 pytest -v            (sem janela; no Windows: set HEADLESS=1)
"""
import pytest

from pages.cardapio_page import CardapioPage
from pages.login_page import LoginPage


def test_login_valido_leva_ao_cardapio(driver, base_url):
    # Arrange (preparar)
    login = LoginPage(driver, base_url).abrir()
    # Act (agir)
    login.entrar("aluno", "123456")
    # Assert (verificar o resultado VISÍVEL para o usuário)
    cardapio = CardapioPage(driver)
    assert cardapio.esta_aberta()
    assert cardapio.usuario_logado() == "aluno"


@pytest.mark.parametrize("usuario, senha, mensagem", [
    ("aluno", "errada", "Usuário ou senha inválidos."),
    ("ninguem", "123456", "Usuário ou senha inválidos."),
    ("", "", "Informe usuário e senha."),
])
def test_login_invalido_mostra_mensagem(driver, base_url, usuario, senha, mensagem):
    login = LoginPage(driver, base_url).abrir()
    login.entrar(usuario, senha)
    assert login.mensagem_erro() == mensagem


def test_adicionar_itens_atualiza_contador_do_carrinho(driver, base_url):
    LoginPage(driver, base_url).abrir().entrar("aluno", "123456")
    cardapio = CardapioPage(driver)
    cardapio.adicionar_item(1)
    cardapio.adicionar_item(5)
    assert cardapio.quantidade_no_carrinho() == 2
