import time
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configuração do navegador (headless)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# URL inicial da MRV
url = "https://www.mrv.com.br/imoveis"
driver.get(url)
time.sleep(3)

# Clicar em "Carregar mais imóveis" até não aparecer mais
while True:
    try:
        botao = driver.find_element(By.XPATH, "//button[contains(text(),'Carregar mais imóveis')]")
        botao.click()
        time.sleep(2)
    except:
        break

# Capturar todos os cards de imóveis
cards = driver.find_elements(By.CSS_SELECTOR, ".card-imovel")

# Criar estrutura XML
root = ET.Element("imoveis")

for idx, card in enumerate(cards, start=1):
    try:
        # Nome do empreendimento no card
        nome = card.find_element(By.CSS_SELECTOR, ".highlight-title").text.strip()

        # Clicar no botão "Saiba mais"
        try:
            saiba_mais = card.find_element(By.XPATH, ".//a[contains(text(),'Saiba mais')]")
            saiba_mais.click()
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Não achou botão Saiba mais para {nome}: {e}")
            continue

        # Trocar para a nova aba/janela aberta
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        # Extrair informações detalhadas
        cidade = ""
        status = ""
        tipologia = ""
        galeria = []
        tipologias = []
        lazer = []

        try:
            status = driver.find_element(By.CSS_SELECTOR, ".highlight-label").text.strip()
        except:
            pass

        try:
            cidade = driver.find_elements(By.CSS_SELECTOR, ".property-details-text")[0].text.strip()
        except:
            pass

        try:
            tipologia = driver.find_elements(By.CSS_SELECTOR, ".property-details-text")[1].text.strip()
        except:
            pass

        # Galeria de imagens
        try:
            imagens = driver.find_elements(By.CSS_SELECTOR, "#cmp-gallery img")
            galeria = [img.get_attribute("src") for img in imagens]
        except:
            pass

        # Tipologias (plantas)
        try:
            plantas = driver.find_elements(By.CSS_SELECTOR, "img[alt*='Planta']")
            for planta in plantas:
                tipologias.append(planta.get_attribute("src"))
        except:
            pass

        # Área de lazer
        try:
            itens = driver.find_elements(By.CSS_SELECTOR, ".sc-bnGbuY li span")
            lazer = [item.text for item in itens]
        except:
            pass

        # Fechar aba e voltar
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Montar XML
        imovel = ET.SubElement(root, "imovel")
        ET.SubElement(imovel, "id").text = str(idx)
        ET.SubElement(imovel, "nome").text = nome
        ET.SubElement(imovel, "cidade").text = cidade
        ET.SubElement(imovel, "status").text = status
        ET.SubElement(imovel, "tipologia").text = tipologia

        galeria_tag = ET.SubElement(imovel, "galeria")
        for img in galeria:
            ET.SubElement(galeria_tag, "imagem").text = img

        tipologias_tag = ET.SubElement(imovel, "plantas")
        for t in tipologias:
            ET.SubElement(tipologias_tag, "planta").text = t

        lazer_tag = ET.SubElement(imovel, "lazer")
        for item in lazer:
            ET.SubElement(lazer_tag, "item").text = item

        ET.SubElement(imovel, "link").text = driver.current_url

        print(f"✅ Capturado: {nome}")

    except Exception as e:
        print(f"⚠️ Erro no imóvel {idx}: {e}")
        continue

# Salvar XML
tree = ET.ElementTree(root)
tree.write("saida_orulo.xml", encoding="utf-8", xml_declaration=True)

driver.quit()
print("Crawler finalizado. Arquivo saida_orulo.xml gerado.")
