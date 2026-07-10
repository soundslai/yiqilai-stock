import base64
import io
import os

import qrcode

RELEASE_DIR = r"D:\codex_file\易起来AI选股\release"
APK_URL = "https://github.com/soundslai/yiqilai-stock/releases/download/v1.0.0-apk/yiqilai-stock-app-debug.apk"
APP_NAME = "易起来AI选股"
VERSION = "v1.0.0 (debug)"
SIZE_MB = "4.1 MB"

os.makedirs(RELEASE_DIR, exist_ok=True)

# ---------- 1. 生成二维码 PNG ----------
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高容错，部分遮挡仍可扫
    box_size=12,
    border=4,
)
qr.add_data(APK_URL)
qr.make(fit=True)
img = qr.make_image(fill_color="#1f2937", back_color="white")
png_path = os.path.join(RELEASE_DIR, "apk-qr.png")
img.save(png_path)

# 转 base64 供 HTML 内嵌（单文件离线可用）
buf = io.BytesIO()
img.save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
data_uri = f"data:image/png;base64,{b64}"

# ---------- 2. 生成自包含下载页 ----------
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{APP_NAME} · APK 下载</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #eef2ff 0%, #f0fdf4 100%);
    color: #1f2937;
    display: flex; align-items: center; justify-content: center;
    padding: 24px;
  }}
  .card {{
    width: 100%; max-width: 420px;
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 12px 40px rgba(37, 99, 235, 0.15);
    padding: 32px 28px 28px;
    text-align: center;
  }}
  .badge {{
    display: inline-block;
    background: #dbeafe; color: #1d4ed8;
    font-size: 13px; font-weight: 600;
    padding: 4px 12px; border-radius: 999px;
    margin-bottom: 14px;
  }}
  h1 {{ font-size: 24px; margin: 0 0 4px; letter-spacing: .5px; }}
  .sub {{ color: #6b7280; font-size: 14px; margin-bottom: 22px; }}
  .qr-wrap {{
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    display: inline-block;
    margin-bottom: 8px;
  }}
  .qr-wrap img {{ width: 240px; height: 240px; display: block; }}
  .scan-tip {{ font-size: 13px; color: #2563eb; font-weight: 600; margin: 10px 0 18px; }}
  .btn {{
    display: block; width: 100%;
    background: linear-gradient(135deg, #2563eb, #16a34a);
    color: #fff; text-decoration: none;
    font-size: 16px; font-weight: 700;
    padding: 14px; border-radius: 14px;
    margin-bottom: 22px;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3);
  }}
  .steps {{
    text-align: left;
    background: #f9fafb;
    border-radius: 14px;
    padding: 16px 18px 16px 36px;
    font-size: 14px; line-height: 1.7;
    color: #374151;
    margin-bottom: 18px;
  }}
  .steps li {{ margin-bottom: 4px; }}
  .foot {{ font-size: 12px; color: #9ca3af; line-height: 1.6; }}
  .foot code {{ background:#eef2ff; color:#1d4ed8; padding:1px 6px; border-radius:6px; word-break: break-all; }}
</style>
</head>
<body>
  <div class="card">
    <div class="badge">Android · 扫码安装</div>
    <h1>{APP_NAME}</h1>
    <div class="sub">AI 智能选股 · 移动端 APK</div>

    <div class="qr-wrap">
      <img src="{data_uri}" alt="APK 下载二维码">
    </div>
    <div class="scan-tip">手机扫码，自动下载安装</div>

    <a class="btn" href="{APK_URL}" target="_blank" rel="noopener">⬇ 点击直接下载 APK</a>

    <ol class="steps">
      <li>用手机相机 / 微信扫一扫上方二维码</li>
      <li>浏览器打开后点「下载」，等待 APK 下载完成</li>
      <li>若提示「禁止安装」，请到系统设置开启 <b>允许未知来源应用</b></li>
      <li>点击已下载的 APK 文件，按提示完成安装</li>
    </ol>

    <div class="foot">
      版本 {VERSION} · 大小 {SIZE_MB}<br>
      下载地址：<code>{APK_URL}</code>
    </div>
  </div>
</body>
</html>
"""

html_path = os.path.join(RELEASE_DIR, "download.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("PNG  ->", png_path, os.path.getsize(png_path), "bytes")
print("HTML ->", html_path, os.path.getsize(html_path), "bytes")
print("QR target:", APK_URL)
