package br.edu.es3.testes;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * Classe base: abre um navegador novo antes de cada teste e fecha depois.
 * Cada teste começa "limpo" (sem cookies/sessão do teste anterior).
 */
public abstract class BaseTeste {

    protected static final String BASE_URL = System.getProperty("baseUrl", "http://localhost:5000");
    protected WebDriver driver;

    @BeforeEach
    void abrirNavegador() {
        ChromeOptions opcoes = new ChromeOptions();
        if (Boolean.parseBoolean(System.getProperty("headless", "false"))) {
            opcoes.addArguments("--headless=new");
        }
        opcoes.addArguments("--window-size=1280,900");
        driver = new ChromeDriver(opcoes); // Selenium Manager resolve o driver
    }

    @AfterEach
    void fecharNavegador() {
        if (driver != null) {
            driver.quit();
        }
    }
}
