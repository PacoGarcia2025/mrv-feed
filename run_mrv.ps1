# Caminhos
$project = "C:\Projetos\mrv-bot"
$python = "$project\.venv\Scripts\python.exe"
$script = "$project\mrv_bot.py"
$xml = "$project\saida.xml"
$git = "C:\Program Files\Git\bin\git.exe"

# TLS moderno
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Executar crawler
& $python $script

# Verificar XML
if (Test-Path $xml) {
    Set-Location $project
    & $git add $xml
    $msg = "Atualização automática do XML em " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    & $git commit -m "$msg"
    & $git push origin main
}
