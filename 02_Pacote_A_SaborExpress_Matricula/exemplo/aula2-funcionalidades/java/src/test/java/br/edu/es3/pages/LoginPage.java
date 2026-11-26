package br.edu.es3.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** Page Object da tela de login da Sabor Express. */
public class LoginPage {

    private static final By CAMPO_USUARIO = By.id("usuario");
    private static final By CAMPO_SENHA = By.id("senha");
    private static final By BOTAO_ENTRAR = By.id("btn-entrar");
    private static final By MENSAGEM_ERRO = By.cssSelector("[data-testid='erro']");

    private final WebDriver driver;
    private final String baseUrl;
    private final WebDriverWait wait;

    public LoginPage(WebDriver driver, String baseUrl) {
        this.driver = driver;
        this.baseUrl = baseUrl;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(5));
    }

    public LoginPage abrir() {
        driver.get(baseUrl + "/login");
        return this;
    }

    public void entrar(String usuario, String senha) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(CAMPO_USUARIO)).sendKeys(usuario);
        driver.findElement(CAMPO_SENHA).sendKeys(senha);
        driver.findElement(BOTAO_ENTRAR).click();
    }

    public String mensagemErro() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(MENSAGEM_ERRO)).getText();
    }
}
