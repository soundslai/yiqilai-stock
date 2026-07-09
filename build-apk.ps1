#requires -Version 5.1
<#
  Yiqilai Stock - APK Builder
  特性：
    - 防火墙感知：可挂代理下载被墙的 Android SDK 组件
    - 自愈：Android Platform/Build-Tools 若为空壳(0字节)会自动清除并重下
    - 修掉中文路径乱码：删除 mojibake 的 local.properties，改用 ANDROID_HOME 环境变量(Unicode安全)
  用法：
    .\build-apk.ps1                          # 使用系统已设的 HTTP(S)_PROXY
    .\build-apk.ps1 -Proxy http://127.0.0.1:7897
#>
[CmdletBinding()]
param(
    [string]$Proxy = ""
)

$ErrorActionPreference = "Stop"
$rootDir = $PSScriptRoot
if (-not $rootDir) { $rootDir = "D:\codex_file\易起来AI选股" }
$toolsDir = Join-Path $rootDir "build_tools"
$sdkDir   = Join-Path $toolsDir "android-sdk"

# ---- 代理设置 ----
if ($Proxy -ne "") {
    $env:HTTP_PROXY  = $Proxy
    $env:HTTPS_PROXY = $Proxy
    $env:http_proxy  = $Proxy
    $env:https_proxy = $Proxy
} elseif ($env:HTTPS_PROXY -or $env:HTTP_PROXY) {
    $Proxy = $env:HTTPS_PROXY
    if (-not $Proxy) { $Proxy = $env:HTTP_PROXY }
}
Write-Host "===== Yiqilai Stock APK Builder =====" -ForegroundColor Cyan
if ($Proxy) { Write-Host "代理: $Proxy" -ForegroundColor Yellow } else { Write-Host "未设代理 (下载 Android SDK 需能访问 dl.google.com)" -ForegroundColor Yellow }

# ---- 1) JDK 17 ----
$jdkDir  = Join-Path $toolsDir "jdk-17.0.19+10"
$javaExe = Join-Path $jdkDir "bin\java.exe"
if (!(Test-Path $javaExe) -or ((Get-Item $javaExe).Length -lt 1MB)) {
    Write-Host "[1/5] 下载 JDK 17..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
    $jdkZip = Join-Path $toolsDir "jdk17.zip"
    $url = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.19%2B10/OpenJDK17U-jdk_x64_windows_hotspot_17.0.19_10.zip"
    (New-Object System.Net.WebClient).DownloadFile($url, $jdkZip)
    Expand-Archive -Path $jdkZip -DestinationPath $toolsDir -Force
    Remove-Item $jdkZip -Force
}
$env:JAVA_HOME = $jdkDir
$env:Path = "$jdkDir\bin;$env:Path"
Write-Host "[1/5] Java 就绪" -ForegroundColor Green

# ---- 2) cmdline-tools ----
$cmdlineToolsDir = Join-Path $sdkDir "cmdline-tools\latest"
$sdkmanager = Join-Path $cmdlineToolsDir "bin\sdkmanager.bat"
if (!(Test-Path $sdkmanager) -or ((Get-Item $sdkmanager).Length -lt 10KB)) {
    Write-Host "[2/5] 下载 Android cmdline-tools..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path (Split-Path $cmdlineToolsDir -Parent) | Out-Null
    $ctZip = Join-Path $toolsDir "cmdline-tools.zip"
    $url2 = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
    (New-Object System.Net.WebClient).DownloadFile($url2, $ctZip)
    $temp = Join-Path $toolsDir "cmdline-tools-temp"
    Expand-Archive -Path $ctZip -DestinationPath $temp -Force
    Move-Item "$temp\cmdline-tools\*" $cmdlineToolsDir -Force
    Remove-Item $temp -Recurse -Force
    Remove-Item $ctZip -Force
}
$env:ANDROID_HOME = $sdkDir
$env:Path = "$cmdlineToolsDir\bin;$env:Path"
Write-Host "[2/5] cmdline-tools 就绪" -ForegroundColor Green

# ---- 3) Platform 34 + Build-Tools 34.0.0 (自愈) ----
$platformDir   = Join-Path $sdkDir "platforms\android-34"
$buildToolsDir = Join-Path $sdkDir "build-tools\34.0.0"
$androidJar    = Join-Path $platformDir "android.jar"
$aapt2         = Join-Path $buildToolsDir "aapt2.exe"

$needSdk = $false
if (!(Test-Path $androidJar) -or ((Get-Item $androidJar).Length -lt 1MB)) { $needSdk = $true; Write-Host "  platform-34 缺失/损坏 -> 将重装" -ForegroundColor Yellow }
if (!(Test-Path $aapt2) -or ((Get-Item $aapt2).Length -lt 1MB)) { $needSdk = $true; Write-Host "  build-tools-34.0.0 缺失/损坏 -> 将重装" -ForegroundColor Yellow }

if ($needSdk) {
    if (Test-Path $platformDir)   { Remove-Item $platformDir -Recurse -Force }
    if (Test-Path $buildToolsDir) { Remove-Item $buildToolsDir -Recurse -Force }
    Write-Host "[3/5] 安装 Android SDK 34 + Build Tools 34.0.0..." -ForegroundColor Yellow
    & $sdkmanager --sdk_root=$sdkDir "platforms;android-34" "build-tools;34.0.0" --silent
    & $sdkmanager --sdk_root=$sdkDir --licenses 2>&1 | Out-Null
}
Write-Host "[3/5] Android SDK 就绪" -ForegroundColor Green

# ---- 3b) 修正 local.properties 中文路径乱码 ----
# Gradle 以 Latin-1 读取 local.properties；中文 sdk.dir 会乱码导致找不到 SDK。
# 解决：删除 local.properties，改用 ANDROID_HOME 环境变量(支持 Unicode 路径)。
$lp = Join-Path $rootDir "android\local.properties"
if (Test-Path $lp) { Remove-Item $lp -Force; Write-Host "  已移除乱码的 local.properties (改用 ANDROID_HOME)" -ForegroundColor Yellow }

# ---- 4) 同步 Web 资源 ----
Write-Host "[4/5] 同步 Web 资源 (cap sync)..." -ForegroundColor Yellow
Push-Location $rootDir
try {
    if (!(Test-Path (Join-Path $rootDir "node_modules"))) {
        npm install --no-audit --no-fund 2>&1 | Out-Null
    }
    $syncOk = $false
    & npx cap sync android 2>&1
    if ($LASTEXITCODE -eq 0) { $syncOk = $true }
    if (-not $syncOk) {
        Write-Host "  sync 失败，改用 cap copy..." -ForegroundColor Yellow
        npx cap copy android 2>&1
    }
} finally {
    Pop-Location
}

# ---- 5) 构建 APK ----
Write-Host "[5/5] 构建 Debug APK..." -ForegroundColor Yellow
Push-Location (Join-Path $rootDir "android")
try {
    if (Test-Path ".\gradlew.bat") { & ".\gradlew.bat" assembleDebug --no-daemon 2>&1 } else { & "./gradlew" assembleDebug --no-daemon 2>&1 }
} finally {
    Pop-Location
}

$apkPath = Join-Path $rootDir "android\app\build\outputs\apk\debug\app-debug.apk"
if (Test-Path $apkPath) {
    Copy-Item $apkPath (Join-Path $rootDir "yiqilai-stock.apk") -Force
    Write-Host "===== APK 构建成功 =====" -ForegroundColor Green
    Write-Host "APK: $(Join-Path $rootDir 'yiqilai-stock.apk')" -ForegroundColor Green
} else {
    Write-Host "===== APK 构建失败 =====" -ForegroundColor Red
    Write-Host "请确认可访问 Google (dl.google.com)，或挂代理后重跑本脚本。" -ForegroundColor Red
}

