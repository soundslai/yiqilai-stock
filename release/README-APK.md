# 易起来AI选股 · APK 发布包（release）

本目录集中存放《易起来AI选股》Android 安装包（APK）及完整构建资料。
项目根目录 `D:\codex_file\易起来AI选股` 为 Capacitor + PWA 跨平台工程，本 `release\` 子目录为**最终交付物**。

> 生成时间：2026-07-10｜构建方式：GitHub Actions 云端自动构建（绕开本地防火墙）

---

## 1. APK 基本信息

| 项 | 值 |
|----|----|
| 文件名 | `yiqilai-stock-app-debug.apk` |
| 包名 (Application ID) | `com.yiqilai.stock` |
| 版本 | 1.0（debug 签名） |
| 大小 | 约 4.14 MB |
| 完整性 | 合法 ZIP / 447 条目 / 含 `AndroidManifest.xml` 与 `classes.dex` ✅ |
| 原始制品 | `apk-artifact.zip`（GitHub Actions 下载的原始压缩包，内含同名 APK） |

---

## 2. 获取 APK 的三种方式

1. **本目录直接拿**：`release/yiqilai-stock-app-debug.apk`
2. **GitHub Release 公开下载**（任何人可点，无需登录）：
   ```
   https://github.com/soundslai/yiqilai-stock/releases/download/v1.0.0-apk/yiqilai-stock-app-debug.apk
   ```
3. **邮箱**：已通过 QQ 邮箱（SMTP）发送至 `860614153@qq.com`（含 APK 附件）。

---

## 3. 手机安装步骤

1. 将 `yiqilai-stock-app-debug.apk` 传到手机（微信文件传输/数据线/U 盘均可）。
2. 手机「设置 → 安全/隐私」中**开启「允许未知来源应用安装」**（或安装时按提示授权当前使用的文件管理器/浏览器）。
3. 点击 APK 文件，按提示完成安装。
4. 桌面出现「易起来AI选股」图标即可打开。
   - 这是 **debug 签名**包，无需 Google Play，普通安卓手机均可装。
   - 若提示「该应用未上架应用商店」，属正常现象，点「继续安装」即可。

> 备选方案：不想装 APK 也可直接用 **PWA**——手机 Chrome 访问局域网地址 `http://<电脑IP>:8080`，点「添加到主屏幕」即得到一个类原生图标（需 `serve-pwa.ps1` 起服务，详见根目录 `BUILD_GUIDE.md`）。

---

## 4. 构建来源与踩坑记录

构建全程在 **GitHub Actions（美国 Runner）** 完成，自动直连 Google 下载 Android SDK，不依赖本机网络。
共触发 **4 次**构建，前 3 次失败、第 4 次成功：

| 次数 | Run ID | 提交 | 结果 | 失败根因 → 修复 |
|------|--------|------|------|----------------|
| 1 | `29054208041` | `958c5cc` | ❌ | `sdkmanager: command not found` → step 内 `export PATH` |
| 2 | `29070981094` | `7c34859` | ❌ | Capacitor CLI 8.4.1 要求 Node≥22（当时 20）→ Node 20→22 |
| 3 | `29071149807` | `c00393b` | ❌ | `invalid source release: 21`（JDK 17 编译不了）→ JDK 17→21 |
| 4 | `29071582445` | `8164bef` | ✅ | `BUILD SUCCESSFUL in 1m 23s` |

最终可用的工作流文件位于仓库根：`.github/workflows/build-apk.yml`
（关键设定：Node 22 + Temurin JDK 21 + `sdkmanager --licenses` 在装包前 + `export PATH` 让 sdkmanager 即时可用）。

---

## 5. 目录结构说明

```
release/
├── README-APK.md                      ← 本说明文档
├── yiqilai-stock-app-debug.apk        ← 【主交付】APK 安装包
├── apk-artifact.zip                   ← GitHub Actions 原始制品（含同名 APK，备用）
├── logs/                              ← 完整构建日志
│   ├── build-success-29071582445.txt      ✅ 第4次成功构建日志
│   ├── build-fail-29070981094-node-version.txt   ❌ 第2次(Node版本)失败日志
│   └── build-fail-29071149807-jdk-version.txt    ❌ 第3次(JDK版本)失败日志
└── scripts/                           ← 配套脚本（可复用）
    ├── send_apk_email.py              ← 通过 QQ 邮箱 SMTP 把 APK 发到指定邮箱
    └── upload_release.py              ← 创建 GitHub Release 并上传 APK 作为下载资产
```

### scripts 用法
```bash
# 发邮件（需 QQ 邮箱 SMTP 授权码）
python scripts/send_apk_email.py \
  --apk yiqilai-stock-app-debug.apk \
  --sender 你的QQ号@qq.com --authcode 你的授权码 \
  --to 860614153@qq.com

# 重新发布到 GitHub Release（需 GitHub token，且仓库 remote 已配置）
python scripts/upload_release.py
```

---

## 6. 安全提示

- 发送邮件用过的 **QQ 邮箱授权码**属于敏感凭证，建议用完后到
  QQ 邮箱「设置 → 账户 → 管理授权码/设备管理」中**吊销该码**。
- 本目录的 APK 为 **debug 签名**，仅供内部测试/分发；若要正式上架应用商店，
  需用自有 keystore 做 release 签名（修改 `android/app/build.gradle`  signingConfigs 即可）。
- 仓库 `soundslai/yiqilai-stock` 为 **public**，APK 下载链接任何人可见，请勿在代码中硬编码密钥。
