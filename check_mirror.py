import urllib.request, re, os, socket
socket.setdefaulttimeout(15)

base = r'D:\codex_file\易起来AI选股\build_tools'
os.makedirs(base, exist_ok=True)

# Try to find JDK on Huawei mirror
test_urls = [
    'https://mirrors.huaweicloud.com/adoptium/17/jdk/x64/windows/',
    'https://mirrors.huaweicloud.com/adoptium/',
]
for url in test_urls:
    try:
        resp = urllib.request.urlopen(url)
        data = resp.read(5000).decode('utf-8', errors='replace')
        resp.close()
        links = re.findall(r'href="([^"]+)"', data)
        zips = [l for l in links if l.endswith('.zip') and 'jdk' in l.lower()]
        dirs = [l for l in links if l.endswith('/') and l != '../']
        print(f'{url}: {len(zips)} zips, {len(dirs)} dirs')
        for z in zips[:5]:
            print(f'  ZIP: {z}')
        if len(dirs) > 0:
            for d in dirs[:10]:
                print(f'  DIR: {d}')
        if zips:
            # Try first zip
            dl_url = zips[0] if zips[0].startswith('http') else url.rstrip('/') + '/' + zips[0]
            print(f'\\nTrying download: {dl_url}')
            dest = os.path.join(base, 'jdk_test.zip')
            socket.setdefaulttimeout(600)
            urllib.request.urlretrieve(dl_url, dest)
            sz = os.path.getsize(dest)
            print(f'  Size: {sz} bytes')
            if sz > 1000000:
                print('  Looks like a valid JDK!')
            os.remove(dest)
            break
    except Exception as e:
        print(f'{url}: {type(e).__name__}: {str(e)[:80]}')
