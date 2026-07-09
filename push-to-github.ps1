# ============================================================
# 推送到 GitHub 并触发云端构建 APK
# 用法：
#   .\push-to-github.ps1 -User "你的GitHub用户名" -Repo "yiqilai-stock"
#   .\push-to-github.ps1 -User "xxx" -Repo "yiqilai-stock" -Proxy "http://127.0.0.1:7897"
#   .\push-to-github.ps1 -User "xxx" -Repo "yiqilai-stock" -Token "ghp_xxx"
#   （可选 -GitName / -GitEmail 覆盖本地提交身份）
# ============================================================
param(
  [Parameter(Mandatory = $true)]  [string] $User,
  [Parameter(Mandatory = $true)]  [string] $Repo,
  [string] $Proxy   = "",
  [string] $Token   = "",
  [string] $GitName  = "",
  [string] $GitEmail = ""
)

$ErrorActionPreference = "Stop"

# 1) 可选：覆盖本地 git 身份（关联你自己的 GitHub 账号）
if ($GitName)  { git config user.name  $GitName }
if ($GitEmail) { git config user.email $GitEmail }

# 2) 构造远端 URL（带 Token 则嵌入，免交互凭证）
if ($Token) {
  $origin = "https://$Token@github.com/$User/$Repo.git"
} else {
  $origin = "https://github.com/$User/$Repo.git"
}

# 3) 添加 / 更新 remote
$existing = git remote get-url origin 2>$null
if ($existing) {
  git remote set-url origin $origin
} else {
  git remote add origin $origin
}

# 4) 推送（若指定代理则临时走代理）
Write-Host "==> 推送 main 到 https://github.com/$User/$Repo" -ForegroundColor Cyan
if ($Proxy) {
  git -c http.proxy="$Proxy" -c https.proxy="$Proxy" push -u origin main
} else {
  git push -u origin main
}

if ($LASTEXITCODE -eq 0) {
  # 推送成功后移除远端 URL 中的明文 Token（安全起见）
  if ($Token) {
    git remote set-url origin "https://github.com/$User/$Repo.git"
    Write-Host "   已移除远端配置中的明文 Token。" -ForegroundColor DarkGray
  }
  Write-Host "`n✅ 推送成功！GitHub Actions 正在自动构建 APK（约 3-6 分钟）。" -ForegroundColor Green
  Write-Host "   打开查看进度: https://github.com/$User/$Repo/actions" -ForegroundColor Cyan
  Write-Host "   完成后在 Artifacts 下载 yiqilai-stock-apk，解压即得 app-debug.apk" -ForegroundColor Cyan
} else {
  Write-Host "`n❌ 推送失败。" -ForegroundColor Red
  Write-Host "   若提示网络不可达：加 -Proxy 参数，或按 PUSH_GUIDE.md 的「兜底方案」换机器推。" -ForegroundColor Yellow
  exit 1
}

