package br.edu.es3.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** Page Object da tela de cardápio da Sabor Express. */
public class CardapioPage {

    private static final By TITULO = By.tagName("h1");
    private static final By QTD_CARRINHO = By.id("qtd-carrinho");
    private static final By USUARIO_LOGADO = By.id("usuario-logado");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public CardapioPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(5));
    }

    public boolean estaAberta() {
        return wait.until(ExpectedConditions.textToBePresentInElementLocated(TITULO, "Cardápio"));
    }

    public String usuarioLogado() {
        return driver.findElement(USUARIO_LOGADO).getText();
    }

    public CardapioPage adicionarItem(int itemId) {
        WebElement botao = wait.until(ExpectedConditions.elementToBeClickable(By.id("add-" + itemId)));
        botao.click();
        // O clique recarrega a página: espera o botão antigo "sumir" (stale)
        // para não interagir com a página velha (StaleElementReferenceException).
        wait.until(ExpectedConditions.stalenessOf(botao));
        return this;
    }

    public int quantidadeNoCarrinho() {
        return Integer.parseInt(
                wait.until(ExpectedConditions.visibilityOfElementLocated(QTD_CARRINHO)).getText());
    }
}
