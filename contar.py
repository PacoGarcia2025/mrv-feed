import xml.etree.ElementTree as ET

# Carrega o XML
tree = ET.parse("saida.xml")
root = tree.getroot()

# Conta empreendimentos
empreendimentos = root.findall("empreendimento")
print("Total de empreendimentos:", len(empreendimentos))

# Conta cidades únicas
cidades = set()
for emp in empreendimentos:
    endereco = emp.findtext("endereco", default="")
    if endereco:
        cidade = endereco.split("-")[0].strip()
        cidades.add(cidade)

print("Total de cidades únicas:", len(cidades))
print("Lista de cidades:", sorted(cidades))
