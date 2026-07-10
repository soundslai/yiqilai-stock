import os, sys, json, urllib.request

TOKEN = os.environ["GH_TOKEN"]
WORK = os.environ.get("WORK_DIR", "C:/Users/Administrator/WorkBuddy/2026-07-10-05-02-24")
APK = os.path.join(WORK, "yiqilai-stock-app-debug.apk")
API = "https://api.github.com/repos/soundslai/yiqilai-stock/releases"

def req(url, data=None, method="GET", ctype="application/json"):
    body = json.dumps(data).encode() if isinstance(data, (dict, list)) else (data or b"")
    r = urllib.request.Request(url, data=body if body else None, method=method)
    r.add_header("Authorization", "token " + TOKEN)
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "workbuddy-agent")
    if body:
        r.add_header("Content-Type", ctype)
    return urllib.request.urlopen(r, timeout=120)

# 1) 创建 release
payload = {
    "tag_name": "v1.0.0-apk",
    "name": "易起来AI选股 APK v1.0 (debug)",
    "body": "GitHub Actions 云端自动构建的 Debug APK。应用ID: com.yiqilai.stock, 版本: 1.0。下载后传手机安装即可。",
}
try:
    d = json.load(req(API, payload, "POST"))
    print("release_id=", d.get("id"))
    print("release_html=", d.get("html_url"))
    upload_url = d["upload_url"].replace("{?name,label}", "")
except Exception as e:
    print("CREATE_RELEASE_ERR:", e)
    # 可能已存在，查已有 release 复用 upload_url
    lst = json.load(req(API))
    if lst:
        upload_url = lst[0]["upload_url"].replace("{?name,label}", "")
        print("reuse_release_upload_url")
    else:
        raise

# 2) 上传 APK
with open(APK, "rb") as f:
    apk_bytes = f.read()
u = urllib.request.Request(upload_url + "?name=yiqilai-stock-app-debug.apk", data=apk_bytes, method="POST")
u.add_header("Authorization", "token " + TOKEN)
u.add_header("Content-Type", "application/vnd.android.package-archive")
u.add_header("User-Agent", "workbuddy-agent")
ad = json.load(urllib.request.urlopen(u, timeout=120))
print("asset_name=", ad.get("name"))
print("asset_browser_url=", ad.get("browser_download_url"))
print("DONE")
