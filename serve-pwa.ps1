#requires -Version 5.1
$root = $PSScriptRoot
$node = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $node) { Write-Host "未找到 node，请先安装 Node.js" -ForegroundColor Red; exit 1 }
Write-Host "启动 PWA 服务器 (Ctrl+C 停止)..." -ForegroundColor Cyan
& $node (Join-Path $root "serve-pwa.js")
