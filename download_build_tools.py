import urllib.request, os, zipfile, shutil, socket
socket.setdefaulttimeout(1800)

base = r'D:\codex_file\易起来AI选股\build_tools'
os.makedirs(base, exist_ok=True)

# 1. Download JDK 17
jdk_zip = os.path.join(base, 'jdk17.zip')
jdk_dir = os.path.join(base, 'jdk-17.0.19+10')
java_exe = os.path.join(jdk_dir, 'bin', 'java.exe')

if not os.path.exists(java_exe):
    print('[1/3] Downloading JDK 17 (~190MB)...')
    url = 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.19%2B10/OpenJDK17U-jdk_x64_windows_hotspot_17.0.19_10.zip'
    urllib.request.urlretrieve(url, jdk_zip)
    sz = os.path.getsize(jdk_zip)
    print(f'  Downloaded: {sz/1e6:.1f} MB. Extracting...')
    with zipfile.ZipFile(jdk_zip) as z:
        z.extractall(base)
    os.remove(jdk_zip)
    print('  JDK 17 ready!')
else:
    print('[1/3] JDK 17 already exists')

# 2. Download Android cmdline-tools
sdk_dir = os.path.join(base, 'android-sdk')
cmdline_bin = os.path.join(sdk_dir, 'cmdline-tools', 'bin', 'sdkmanager.bat')
cmdline_zip = os.path.join(base, 'cmdline-tools.zip')

if not os.path.exists(cmdline_bin):
    print('[2/3] Downloading Android cmdline-tools (~150MB)...')
    url = 'https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip'
    urllib.request.urlretrieve(url, cmdline_zip)
    sz = os.path.getsize(cmdline_zip)
    print(f'  Downloaded: {sz/1e6:.1f} MB. Extracting...')
    temp_dir = os.path.join(base, '_temp_ct')
    os.makedirs(temp_dir, exist_ok=True)
    with zipfile.ZipFile(cmdline_zip) as z:
        z.extractall(temp_dir)
    ct_root = os.path.join(sdk_dir, 'cmdline-tools')
    os.makedirs(ct_root, exist_ok=True)
    for item in os.listdir(os.path.join(temp_dir, 'cmdline-tools')):
        s = os.path.join(temp_dir, 'cmdline-tools', item)
        d = os.path.join(ct_root, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.remove(cmdline_zip)
    print('  Cmdline-tools ready!')
else:
    print('[2/3] Cmdline-tools already exists')

# 3. Install Android platform + build-tools via sdkmanager
sdkmanager = os.path.join(sdk_dir, 'cmdline-tools', 'bin', 'sdkmanager.bat')
platform_dir = os.path.join(sdk_dir, 'platforms', 'android-34')
bt_dir = os.path.join(sdk_dir, 'build-tools', '34.0.0')

if not os.path.exists(platform_dir) or not os.path.exists(bt_dir):
    print('[3/3] Installing Android SDK 34 + Build Tools...')
    import subprocess
    # Accept licenses
    subprocess.run([sdkmanager, f'--sdk_root={sdk_dir}', '--licenses'], input=b'y\n', capture_output=True, timeout=300)
    subprocess.run([sdkmanager, f'--sdk_root={sdk_dir}', 'platforms;android-34'], capture_output=True, timeout=300)
    subprocess.run([sdkmanager, f'--sdk_root={sdk_dir}', 'build-tools;34.0.0'], capture_output=True, timeout=300)
    print('  Android SDK ready!')
else:
    print('[3/3] Android SDK already installed')

print()
print('=== Build Environment Summary ===')
print(f'Java:    {os.path.exists(java_exe)}')
print(f'sdkmanager: {os.path.exists(cmdline_bin)}')
print(f'Platform 34: {os.path.exists(platform_dir)}')
print(f'Build Tools 34: {os.path.exists(bt_dir)}')
print('All downloads complete!')
