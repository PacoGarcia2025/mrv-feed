from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

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
    driver.get("https://www.mrv.com.br/imoveis/sao-paulo")
    print("Página carregada com sucesso!")

    # Espera até que os cards estejam presentes
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-button"))
    )
    print("Cards detectados!")

    # Captura do HTML
    html = driver.page_source
    print("HTML capturado, iniciando parsing...")

    # Parsing com BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    print("Parsing concluído!")

    # Busca pelos botões dos cards
    cards = soup.find_all("div", class_="card-button")
    print(f"Encontrados {len(cards)} imóveis.")

    # Processamento dos cards
    for idx, card in enumerate(cards, start=1):
        # Texto do botão
        botao = card.get_text(strip=True)

        # Imagem associada ao card
        imagem = card.find_next("img", class_="card-image")
        imagem_src = imagem["src"] if imagem else "Sem imagem"

        # Link da página do imóvel (pai <a>)
        link = card.find_parent("a")["href"] if card.find_parent("a") else "Sem link"

        print(f"[{idx}] Botão: {botao} | Imagem: {imagem_src} | Link: {link}")

    print("Processamento concluído, saída gerada!")

except Exception as e:
    print(f"Erro durante execução: {e}")

finally:
    driver.quit()
    print("Navegador fechado. Script finalizado.")
