# Executa o crawler da MRV no padrão Orulo
python mrv_bot_orulo.py

# Adiciona o arquivo XML gerado ao Git
git add saida_orulo.xml

# Faz commit com mensagem padrão
git commit -m "Atualização automática do XML Orulo da MRV"

# Envia para o repositório remoto
git push origin main
