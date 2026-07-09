import urllib.request, os, zipfile, shutil, ssl, sys, time
ssl._create_default_https_context = ssl._create_unverified_context

base_url = 'https://redirector.gvt1.com/edgedl/android/repository/'
sdk_dir = r'D:\codex_file\易起来AI选股\build_tools\android-sdk'
proxy = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.makedirs(sdk_dir, exist_ok=True)

def download_and_extract(name, url_path, extract_to):
    url = base_url + url_path
    dest = os.path.join(sdk_dir, name + '.zip')
    extract_dir = os.path.join(sdk_dir, extract_to)
    
    print(f'Downloading {name}...')
    t0 = time.time()
    urllib.request.urlretrieve(url, dest)
    elapsed = time.time() - t0
    sz = os.path.getsize(dest)
    print(f'  {sz/1e6:.1f} MB in {elapsed:.0f}s ({sz/elapsed/1e6*8:.1f} Mbps)')
    
    print('  Extracting...')
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(dest) as z:
        z.extractall(extract_dir)
    os.remove(dest)
    print(f'  Done: {extract_dir}')

# Download platform 34
download_and_extract('platform-34', 'platform-34_r03.zip', 'platforms\\android-34')

# Download build-tools 34.0.0
download_and_extract('build-tools', 'build-tools_r34.0.0-windows.zip', 'build-tools\\34.0.0')

# Verify
jar_path = os.path.join(sdk_dir, 'platforms', 'android-34', 'android.jar')
aapt_path = os.path.join(sdk_dir, 'build-tools', '34.0.0', 'aapt2.exe')
print(f'\nVerification:')
print(f'  android.jar: {os.path.exists(jar_path)}')
print(f'  aapt2.exe: {os.path.exists(aapt_path)}')
print('SDK installation complete!')
