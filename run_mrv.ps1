Write-Output "===== Iniciando execução do script MRV ====="

# Caminho do Python dentro do ambiente virtual
$pythonPath = "C:\Projetos\mrv-bot\.venv\Scripts\python.exe"
# Caminho do script Python
$scriptPath = "C:\Projetos\mrv-bot\mrv_bot.py"

Write-Output "Executando crawler Python..."
& $pythonPath $scriptPath

Write-Output "Crawler finalizado. Verificando saída..."

# Caminho do repositório
$repoPath = "C:\Projetos\mrv-bot"
Set-Location $repoPath

Write-Output "Adicionando arquivos ao Git..."
& "C:\Program Files\Git\bin\git.exe" add .

Write-Output "Criando commit..."
& "C:\Program Files\Git\bin\git.exe" commit -m "Atualização automática via run_mrv.ps1"

Write-Output "Enviando para o GitHub..."
& "C:\Program Files\Git\bin\git.exe" push origin main

Write-Output "===== Execução concluída com sucesso ====="

# Força o encerramento do PowerShell
exit
