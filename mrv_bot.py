from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import traceback
import xml.etree.ElementTree as ET

print("Iniciando crawler...")

# Configuração do navegador
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # roda sem abrir janela
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

print("Configurando ChromeDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.set_page_load_timeout(30)

try:
    print("Abrindo página alvo...")
    driver.get("https://www.mrv.com.br/imoveis/sao-paulo")
    print("Página carregada com sucesso!")

    # Espera inicial para os primeiros cards
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-button"))
    )
    print("Primeiros cards detectados!")

    # Loop para clicar no botão "Carregar mais imóveis"
    while True:
        try:
            botao = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "load-more-button"))
            )
            driver.execute_script("arguments[0].click();", botao)
            print("Botão 'Carregar mais imóveis' clicado.")
            time.sleep(3)  # espera carregar novos cards
        except:
            print("Nenhum botão 'Carregar mais imóveis' encontrado. Todos os imóveis carregados.")
            break

    # Captura do HTML final
    html = driver.page_source
    print("HTML completo capturado, iniciando parsing...")

    soup = BeautifulSoup(html, "lxml")
    print("Parsing concluído!")

    # Busca pelos cards
    cards = soup.find_all("div", class_="card-button")
    print(f"Encontrados {len(cards)} imóveis.")

    # Criar XML
    root = ET.Element("imoveis")

    for idx, card in enumerate(cards, start=1):
        botao = card.get_text(strip=True)

        imagem = card.find_next("img", class_="card-image")
        imagem_src = imagem["src"] if imagem else "Sem imagem"

        link = card.find_parent("a")["href"] if card.find_parent("a") else "Sem link"

        print(f"[{idx}] Botão: {botao} | Imagem: {imagem_src} | Link: {link}")

        imovel = ET.SubElement(root, "imovel")
        ET.SubElement(imovel, "id").text = str(idx)
        ET.SubElement(imovel, "botao").text = botao
        ET.SubElement(imovel, "imagem").text = imagem_src
        ET.SubElement(imovel, "link").text = link

    tree = ET.ElementTree(root)
    tree.write("saida.xml", encoding="utf-8", xml_declaration=True)

    print("Arquivo XML 'saida.xml' gerado com sucesso!")

except Exception as e:
    print("Erro durante execução:")
    print(traceback.format_exc())

finally:
    driver.quit()
    print("Navegador fechado. Script finalizado.")
