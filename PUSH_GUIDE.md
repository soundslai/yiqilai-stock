# 推送到 GitHub 云端构建 APK · 命令清单

> 目标：把本地 `易起来AI选股` 仓库推到 GitHub，由 GitHub Actions（美国 Runner）自动下载 Android SDK 并产出 `app-debug.apk`。**不依赖你本机网络**，一劳永逸。
>
> 本地仓库已就绪：`main` 分支、提交 `ad79dfd`、120 个文件、`build_tools/`(633MB) 与 `node_modules/` 已按 `.gitignore` 排除。

---

## 步骤 0 · 确认本机仓库状态（已完成）
```powershell
cd D:\codex_file\易起来AI选股
git log --oneline -1        # 应看到 ad79dfd 提交
git status                  # 应显示 "nothing to commit, working tree clean"
git remote -v               # 应为空（还没设远端）
```

## 步骤 1 · 在 GitHub 网页新建空仓库
1. 打开 https://github.com/new
2. **Repository name** 填：`yiqilai-stock`（或你喜欢的名字）
3. **不要**勾选 "Add a README file" / ".gitignore" / "LICENSE" —— 保持 **空仓库**，否则首次 push 会冲突。
4. 点 **Create repository**。

## 步骤 2 ·（推荐）改成本地 git 身份，关联你自己的 GitHub 账号
> 当前 commit 作者是占位的 `sulian-ai`，push 后不会关联你的 GitHub 头像。建议改成你自己的（因为还没 push，直接 amend 安全）。
```powershell
git config user.name  "你的GitHub用户名"
git config user.email "你的GitHub邮箱"
git commit --amend --reset-author --no-edit
```

## 步骤 3 · 添加远端并推送
> 把下面的 `<你的GitHub用户名>` 换成你真实的 GitHub 用户名。

**方式 A · 直接用脚本（最简单）**
```powershell
# 普通推送（若本机直连 GitHub 正常）
.\push-to-github.ps1 -User "你的GitHub用户名" -Repo "yiqilai-stock"

# 若本机需走代理才能上 GitHub（如 127.0.0.1:7897 真能出外网）
.\push-to-github.ps1 -User "你的GitHub用户名" -Repo "yiqilai-stock" -Proxy "http://127.0.0.1:7897"

# 若不想交互输密码，可带 Personal Access Token（脚本推送后会自动从配置里清除明文 Token）
.\push-to-github.ps1 -User "你的GitHub用户名" -Repo "yiqilai-stock" -Token "ghp_你的Token"
```

**方式 B · 手动命令（看得更清楚）**
```powershell
git remote add origin https://github.com/<你的GitHub用户名>/yiqilai-stock.git
git branch -M main
# 若需代理：
#   git -c http.proxy=http://127.0.0.1:7897 -c https.proxy=http://127.0.0.1:7897 push -u origin main
# 否则：
git push -u origin main
# 第一次会要求输入 GitHub 用户名 + 密码（密码处填 Personal Access Token，不是账号密码）
```

## 步骤 4 · 等 Actions 自动构建并下载 APK
1. 打开 `https://github.com/<你的GitHub用户名>/yiqilai-stock/actions`
2. 看到名为 **Build APK** 的工作流开始运行（push 自动触发，约 3–6 分钟）。
3. 变绿 ✅ 后，点进该次运行 → 页面右侧 **Artifacts** → 下载 `yiqilai-stock-apk`（是个 zip）。
4. 解压得到 `app-debug.apk`，手机安装即可（安装时需允许「未知来源」）。

> 之后每次改代码 `git push`，都会自动重新构建出新 APK。

---

## 兜底方案 · 本机连不上 GitHub 时
若本机直连/代理都上不了 GitHub，用 `git bundle` 把仓库打成**单文件**（仅含 git 跟踪内容，不含 633MB 的 `build_tools/`）再拷到能上网的机器推：

```powershell
# 本机（无需外网）：
cd D:\codex_file\易起来AI选股
git bundle create yiqilai-stock.bundle --all
# 把 yiqilai-stock.bundle 拷到能上 GitHub 的电脑
```
```bash
# 那台能上网的机器：
git clone yiqilai-stock.bundle yiqilai-repo
cd yiqilai-repo
git remote add origin https://github.com/<你的GitHub用户名>/yiqilai-stock.git
git push -u origin main
```

---

## 常见问题
| 现象 | 原因 / 解决 |
|------|------------|
| `push` 提示 `remote: Repository not found` | 仓库名拼错，或仓库不是空仓库（含 README）。删了重建空仓库。 |
| `push` 卡住 / 超时 | 本机连不上 GitHub。加 `-Proxy` 或走「兜底方案」换机器推。 |
| Actions 红 ✗：`sdkmanager` license 卡住 | 已在工作流里 `yes \| sdkmanager --licenses` 处理，正常不会再出现。 |
| Actions 红 ✗：`npx cap` 找不到 | 已确认 `package.json` 含 `@capacitor/cli@^8.4.1`，`npm install` 后会装上。 |
| 下载的 APK 装不上 | 用 debug 签名，需在手机「设置→安全」允许未知来源安装。 |
