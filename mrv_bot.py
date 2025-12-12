from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

print("Iniciando crawler...")

# Configuração do navegador
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # roda sem abrir janela
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

print("Configurando ChromeDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Timeout para carregamento de página
driver.set_page_load_timeout(30)

try:
    print("Abrindo página alvo...")
    driver.get("https://www.mrv.com.br/imoveis")  # URL real que você já usava
    print("Página carregada com sucesso!")

    # Espera até que os elementos dos imóveis estejam presentes
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-imovel"))  # ajuste conforme seletor real
    )
    print("Elementos de imóveis detectados!")

    # Captura do HTML
    html = driver.page_source
    print("HTML capturado, iniciando parsing...")

    # Parsing com BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    print("Parsing concluído!")

    # Busca pelos imóveis (ajuste conforme seletor real que você já tinha)
    imoveis = soup.find_all("div", class_="card-imovel")
    print(f"Encontrados {len(imoveis)} imóveis.")

    # Processamento dos imóveis
    for idx, imovel in enumerate(imoveis, start=1):
        titulo = imovel.find("h2").get_text(strip=True) if imovel.find("h2") else "Sem título"
        cidade = imovel.find("span", class_="cidade").get_text(strip=True) if imovel.find("span", class_="cidade") else "Sem cidade"
        print(f"[{idx}] {titulo} - {cidade}")

    # Aqui você mantém a lógica de salvar no XML (saida.xml)
    # Exemplo:
    # with open("saida.xml", "w", encoding="utf-8") as f:
    #     f.write(gerar_xml(imoveis))

    print("Processamento concluído, saída gerada!")

except Exception as e:
    print(f"Erro durante execução: {e}")

finally:
    driver.quit()
    print("Navegador fechado. Script finalizado.")
