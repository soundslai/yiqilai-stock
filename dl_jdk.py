import urllib.request, os, zipfile, time, ssl
ssl._create_default_https_context = ssl._create_unverified_context

base = r'D:\codex_file\易起来AI选股\build_tools'
os.makedirs(base, exist_ok=True)
jdk_zip = os.path.join(base, 'jdk17.zip')
jdk_dir = os.path.join(base, 'jdk-17.0.19+10')

if os.path.exists(os.path.join(jdk_dir, 'bin', 'java.exe')):
    print('JDK already exists')
    exit(0)

# Try Tencent mirror
tencent_url = 'https://mirrors.cloud.tencent.com/eclipse/adoptium/releases/temurin17/jdk/x64/windows/OpenJDK17U-jdk_x64_windows_hotspot_17.0.19_10.zip'
print(f'Trying Tencent: {tencent_url}')
try:
    resp = urllib.request.urlopen(tencent_url, timeout=15)
    print(f'  Status: {resp.status}, Size: {resp.headers.get(\"Content-Length\", \"?\")}')
    resp.close()
    print('  Downloading...')
    start = time.time()
    urllib.request.urlretrieve(tencent_url, jdk_zip)
    elapsed = time.time() - start
    sz = os.path.getsize(jdk_zip)
    print(f'  Downloaded {sz/1e6:.1f} MB in {elapsed:.0f}s')
    print('  Extracting...')
    with zipfile.ZipFile(jdk_zip) as z:
        z.extractall(base)
    os.remove(jdk_zip)
    print('JDK ready!')
    exit(0)
except Exception as e:
    print(f'  Failed: {e}')

# Fallback: GitHub
github_url = 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.19%2B10/OpenJDK17U-jdk_x64_windows_hotspot_17.0.19_10.zip'
print(f'Trying GitHub (may be slow): {github_url}')
print('Downloading...')
start = time.time()
urllib.request.urlretrieve(github_url, jdk_zip)
elapsed = time.time() - start
sz = os.path.getsize(jdk_zip)
print(f'Downloaded {sz/1e6:.1f} MB in {elapsed:.0f}s')
print('Extracting...')
with zipfile.ZipFile(jdk_zip) as z:
    z.extractall(base)
os.remove(jdk_zip)
print('JDK ready!')
