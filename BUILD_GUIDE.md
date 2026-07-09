# 易起来AI选股 · 构建落地指南

> 状态诊断：防火墙确实封锁了 `dl.google.com`，国内镜像（腾讯/清华/阿里/华为）均不托管
> `platform-34` 与 `build-tools-34.0.0` 的 zip 包，因此本地无法直连下载这两个组件。
> 此外已修掉 3 个隐藏炸弹（见下），否则即使换到能访问 Google 的机器也会失败。

## 一、已修复的隐藏问题（重要）

| # | 问题 | 现象 | 修复 |
|---|------|------|------|
| 1 | `capacitor.config.json` 第 4–5 行**缺逗号** | JSON 非法，`npx cap sync` 必崩 | 已补逗号 |
| 2 | `android/local.properties` 的 `sdk.dir` 是**中文路径乱码** | Gradle 按 Latin-1 读属性，找不到 SDK | 改由 `ANDROID_HOME` 环境变量提供（支持 Unicode） |
| 3 | `android.jar` / `aapt2.exe` 是 **0 字节空壳** | 原脚本只判断"目录存在"会跳过下载 | `build-apk.ps1` 改为按文件大小校验，空壳自动清除重下 |

## 二、三条可用路径

### 路径 A：PWA（立即可用，零门槛）✅ 推荐先上
手机 Chrome 访问 `http://<本机局域网IP>:8080` → 菜单"添加到主屏幕"。
```powershell
# 在本机项目目录执行（自动用 Node 起一个 0.0.0.0:8080 静态服务）
.\serve-pwa.ps1
```
> 注意：Service Worker 需要 **HTTPS** 才能触发"安装"提示。HTTP 局域网下手机只会得到普通网页快捷方式。
> 如需真·PWA 安装体验，加一层隧道即可：
> `cloudflared tunnel --url http://localhost:8080` （拿到 https 域名后手机访问即可安装）。

### 路径 B：GitHub Actions 云端构建 APK（彻底绕过防火墙）✅ 最稳
云端 Runner（美国）可直连 Google，自动下载 Platform/Build-Tools 并产出 APK 制品。
```bash
# 1) 本机初始化 git 并推到 GitHub（新建一个私有/公开仓库）
git init
git add -A
git commit -m "init yiqilai stock"
git remote add origin https://github.com/<你的账号>/yiqilai-stock.git
git push -u origin main

# 2) 在 GitHub 仓库 → Actions → 手动触发 "Build APK"（或 push 即自动触发）
# 3) 构建完成后到 Actions 制品(Artifact) 下载 yiqilai-stock.apk
```
工作流文件已就位：`.github/workflows/build-apk.yml`

### 路径 C：换到能访问 Google 的机器本地构建
把整个 `D:\codex_file\易起来AI选股` 复制到能访问 Google 的电脑，直接运行（已含自愈逻辑）：
```powershell
.\build-apk.ps1
```
> JDK / Gradle / cmdline-tools 缓存会复用，只需额外下载 Platform + Build-Tools（约 60MB）。

### 路径 D：本机若已挂可用代理（如 Clash 7897）
只要代理真能出 Google，本机也可直接构建：
```powershell
.\build-apk.ps1 -Proxy http://127.0.0.1:7897
```
> 经实测，当前 `127.0.0.1:7897` 并未在运行（连接被拒），需先启动代理软件并确保其监听该端口。

## 三、文件清单
- `capacitor.config.json` — 已修正 JSON
- `build-apk.ps1` — 代理感知 + 自愈 + 中文路径修复 的构建脚本
- `.github/workflows/build-apk.yml` — 云端构建工作流
- `serve-pwa.js` / `serve-pwa.ps1` — 局域网 PWA 静态服务
- 本文件 `BUILD_GUIDE.md`
