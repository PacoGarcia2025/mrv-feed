from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import re

def limpar_nome_tag(texto):
    return re.sub(r'\W+', '_', texto.strip().lower())

def extrair_empreendimento(url, driver):
    driver.get(url)
    time.sleep(8)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    emp = ET.Element("empreendimento")

    # Nome
    nome = soup.title.string.strip() if soup.title else "Nome não encontrado"
    ET.SubElement(emp, "nome").text = nome

    # Descrição
    desc_div = soup.find("div", id="complemento-descricao")
    descricao_texto = desc_div.get_text(" ", strip=True) if desc_div else ""
    ET.SubElement(emp, "descricao").text = descricao_texto

    # Endereço
    endereco = ""
    for p in soup.find_all("p"):
        texto = p.get_text(strip=True)
        if "São Paulo" in texto:
            endereco = texto
            break
    ET.SubElement(emp, "endereco").text = endereco

    # Tipologias
    tipologias = ET.SubElement(emp, "tipologias")
    for detail in soup.find_all("p", class_="property-details-text"):
        ET.SubElement(tipologias, "tipologia").text = detail.get_text(strip=True)

    accordion = soup.find("div", class_="accordion-content")
    if accordion:
        ul = accordion.find("ul")
        if ul:
            for li in ul.find_all("li"):
                ET.SubElement(tipologias, "tipologia").text = li.get_text(strip=True)

    # Diferenciais
    diferenciais = ET.SubElement(emp, "diferenciais_condominio")
    for item in soup.find_all("li", class_="sc-hylbpc jqUSgi"):
        span = item.find("span")
        if span:
            ET.SubElement(diferenciais, "diferencial").text = span.get_text(strip=True)

    # Galeria
    galeria = ET.SubElement(emp, "galeria")
    for img in soup.find_all("img"):
        url_img = img.get("src", "")
        desc = img.get("alt", "")
        if url_img and ("upload/imagens" in url_img.lower()):
            foto = ET.SubElement(galeria, "foto")
            ET.SubElement(foto, "descricao").text = desc
            ET.SubElement(foto, "imagem").text = url_img

    # Plantas
    plantas_div = soup.find("div", id="plantas")
    plantas = ET.SubElement(emp, "plantas")
    if plantas_div:
        for img in plantas_div.find_all("img"):
            foto = ET.SubElement(plantas, "planta")
            ET.SubElement(foto, "descricao").text = img.get("alt", "")
            ET.SubElement(foto, "imagem").text = img.get("src", "")

    # Localização
    loc_div = soup.find("p", id="descricao-localizacao-p")
    ET.SubElement(emp, "descricao_localizacao").text = loc_div.get_text(" ", strip=True) if loc_div else ""

    # Dados técnicos extras
    dados_tecnicos = ET.SubElement(emp, "dados_tecnicos")
    if accordion:
        subs = accordion.find_all("p", class_="accordion-subtitle")
        for sub in subs:
            titulo = limpar_nome_tag(sub.get_text())
            next_el = sub.find_next_sibling("p")
            if next_el:
                ET.SubElement(dados_tecnicos, titulo).text = next_el.get_text(strip=True)

    # Novos blocos
    ET.SubElement(emp, "status_obra").text = ""
    ET.SubElement(emp, "condicoes_comerciais").text = ""
    ET.SubElement(emp, "programa_habitacional").text = ""
    infraestrutura = ET.SubElement(emp, "infraestrutura_urbana")
    ficha_tecnica = ET.SubElement(emp, "ficha_tecnica")
    ET.SubElement(ficha_tecnica, "torres").text = ""
    ET.SubElement(ficha_tecnica, "pavimentos").text = ""
    ET.SubElement(ficha_tecnica, "unidades_por_andar").text = ""

    return emp

# Configurações do Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Página inicial da MRV filtrada para São Paulo
driver.get("https://www.mrv.com.br/imoveis/sao-paulo")
time.sleep(5)

# Loop para clicar no botão "Carregar mais imóveis" até não aparecer mais
while True:
    try:
        botao = driver.find_element(By.XPATH, "//button[contains(text(),'Carregar mais imóveis')]")
        driver.execute_script("arguments[0].click();", botao)
        time.sleep(5)  # espera carregar os novos cards
    except NoSuchElementException:
        break  # não tem mais botão, saímos do loop

# Agora todos os cards estão carregados
soup = BeautifulSoup(driver.page_source, "lxml")

# Coletar todos os links de empreendimentos em SP
links = []
base_url = "https://www.mrv.com.br"
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/imoveis/sao-paulo/" in href and "apartamentos" in href:
        if href.startswith("/"):
            href = base_url + href
        links.append(href)

links = list(set(links))  # remove duplicados

# Criar XML com todos os empreendimentos de SP
root = ET.Element("feed")
for link in links:
    try:
        emp = extrair_empreendimento(link, driver)
        root.append(emp)
    except Exception as e:
        print(f"Erro ao processar {link}: {e}")

tree = ET.ElementTree(root)
tree.write("saida.xml", encoding="utf-8", xml_declaration=True)

driver.quit()
