import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE = os.environ.get("BASE_URL", "http://127.0.0.1:3000")


def abrir(driver):
    driver.get(BASE)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#patient-list [data-patient-id]"))
    )


def test_lista_pacientes_carrega(driver):
    abrir(driver)
    assert "Ana Beatriz Nogueira" in driver.find_element(By.ID, "patient-list").text


def test_busca_paciente_por_nome(driver):
    abrir(driver)
    campo = driver.find_element(By.ID, "search-input")
    campo.send_keys("Carlos Eduardo")
    lista = driver.find_element(By.ID, "patient-list").text
    assert "Carlos Eduardo Matias" in lista
    assert "Ana Beatriz Nogueira" not in lista


def test_regra_filtro_apenas_ativos(driver):
    abrir(driver)
    driver.find_element(By.ID, "only-active-input").click()
    lista = driver.find_element(By.ID, "patient-list").text
    assert "Eduardo Vasconcelos" not in lista
    assert "Ana Beatriz Nogueira" in lista


def test_cadastro_paciente_com_sucesso(driver):
    abrir(driver)
    driver.find_element(By.ID, "name-input").send_keys("Paciente Teste Funcional")
    driver.find_element(By.ID, "birth-date-input").send_keys("1990-04-12")
    driver.find_element(By.ID, "national-id-input").send_keys("799900000000001")
    driver.find_element(By.ID, "save-button").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "form-feedback"), "cadastrado")
    )
    assert "Paciente Teste Funcional" in driver.find_element(By.ID, "patient-list").text


def test_cadastro_rejeita_cns_duplicado(driver):
    abrir(driver)
    driver.find_element(By.ID, "name-input").send_keys("Paciente com CNS repetido")
    driver.find_element(By.ID, "birth-date-input").send_keys("1990-04-12")
    driver.find_element(By.ID, "national-id-input").send_keys("700012345678901")
    driver.find_element(By.ID, "save-button").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "form-feedback"), "Ja existe")
    )


def test_cadastro_rejeita_nome_vazio(driver):
    abrir(driver)
    driver.find_element(By.ID, "birth-date-input").send_keys("1990-04-12")
    driver.find_element(By.ID, "national-id-input").send_keys("799900000000002")
    driver.find_element(By.ID, "save-button").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "form-feedback"), "name")
    )


def test_registra_atendimento_com_sucesso(driver):
    abrir(driver)
    driver.find_element(By.CSS_SELECTOR, '[data-patient-id="1"]').click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "encounter-complaint-input")))
    driver.find_element(By.ID, "encounter-date-input").send_keys("2026-09-10T10:30")
    driver.find_element(By.ID, "encounter-complaint-input").send_keys("Consulta de teste funcional")
    driver.find_element(By.ID, "save-encounter-button").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "detail-panel"), "Consulta de teste funcional")
    )


def test_atendimento_rejeita_queixa_vazia(driver):
    abrir(driver)
    driver.find_element(By.CSS_SELECTOR, '[data-patient-id="1"]').click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "save-encounter-button")))
    driver.find_element(By.ID, "encounter-date-input").send_keys("2026-09-10T10:30")
    driver.find_element(By.ID, "save-encounter-button").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "encounter-feedback"), "chiefComplaint")
    )
