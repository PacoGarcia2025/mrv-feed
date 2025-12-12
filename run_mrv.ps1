# Caminhos
$project = "C:\Projetos\mrv-bot"
$python = "$project\.venv\Scripts\python.exe"
$script = "$project\mrv_bot.py"
$xml = "$project\saida.xml"

# Ativar TLS moderno para push via HTTPS (se usado)
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Executar o crawler
& $python $script

# Verificar se o XML foi gerado
if (Test-Path $xml) {
    Set-Location $project
    git add $xml
    $msg = "Atualização automática do XML em " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    git commit -m $msg
    git push origin main
}
