# 易起来AI选股 - Android 安装指南

## 方式一：通过浏览器安装 PWA（推荐，无需构建）

1. 在 Android 手机上打开 Chrome 浏览器
2. 访问易起来AI选股的网页地址
3. 点击 Chrome 菜单（右上角三个点）
4. 选择 **"添加到主屏幕"** 或 **"安装应用"**
5. 确认安装，应用会出现在桌面

> 优点：无需安装 Java/Android SDK，自动更新

## 方式二：构建原生 APK

### 前置要求
- **Java JDK 17+** - 下载: https://adoptium.net/
- **Android Studio** (含 Android SDK) - 下载: https://developer.android.com/studio

### 环境配置
```bash
# 设置 Java 环境变量
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

# 设置 Android SDK 环境变量
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
```

### 构建步骤
1. 双击运行 **`build-apk.bat`**
2. 等待 Gradle 构建完成
3. APK 文件生成在项目根目录：`易起来AI选股.apk`

### 手动构建
```bash
# 同步 Web 文件
npx cap sync android

# 构建 APK
cd android
./gradlew assembleDebug

# APK 位置:
# android\app\build\outputs\apk\debug\app-debug.apk
```

## 方式三：使用 Android Studio 打开
```bash
npx cap open android
```
然后在 Android Studio 中点击 **Build → Build Bundle(s) / APK(s) → Build APK(s)**

## 文件结构
```
易起来AI选股/
├── index.html          # 主应用
├── manifest.json       # PWA 清单
├── sw.js              # Service Worker (离线支持)
├── icons/             # 应用图标
├── www/               # Capacitor Web 资源
├── android/           # Android 原生项目
├── capacitor.config.json  # Capacitor 配置
├── build-apk.bat      # APK 构建脚本
└── README_ANDROID.md  # 本文件
```
