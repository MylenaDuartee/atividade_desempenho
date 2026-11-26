package br.edu.es3.testes;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import br.edu.es3.pages.CardapioPage;
import br.edu.es3.pages.LoginPage;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

/** Exemplo da Aula 2 - Teste funcional automatizado com Selenium + JUnit 5. */
class LoginTest extends BaseTeste {

    @Test
    @DisplayName("Login válido leva ao cardápio")
    void loginValidoLevaAoCardapio() {
        // Arrange
        LoginPage login = new LoginPage(driver, BASE_URL).abrir();
        // Act
        login.entrar("aluno", "123456");
        // Assert
        CardapioPage cardapio = new CardapioPage(driver);
        assertTrue(cardapio.estaAberta());
        assertEquals("aluno", cardapio.usuarioLogado());
    }

    @ParameterizedTest(name = "usuário=''{0}'' senha=''{1}'' -> {2}")
    @CsvSource(value = {
            "aluno   | errada | Usuário ou senha inválidos.",
            "ninguem | 123456 | Usuário ou senha inválidos.",
            "''      | ''     | Informe usuário e senha."
    }, delimiter = '|')
    @DisplayName("Login inválido mostra mensagem de erro")
    void loginInvalidoMostraMensagem(String usuario, String senha, String mensagem) {
        LoginPage login = new LoginPage(driver, BASE_URL).abrir();
        login.entrar(usuario, senha);
        assertEquals(mensagem, login.mensagemErro());
    }

    @Test
    @DisplayName("Adicionar itens atualiza o contador do carrinho")
    void adicionarItensAtualizaContador() {
        new LoginPage(driver, BASE_URL).abrir().entrar("aluno", "123456");
        CardapioPage cardapio = new CardapioPage(driver);
        cardapio.adicionarItem(1).adicionarItem(5);
        assertEquals(2, cardapio.quantidadeNoCarrinho());
    }
}
