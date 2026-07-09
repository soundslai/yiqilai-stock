// 零依赖静态服务器：把 www/ 以 HTTP 提供在 0.0.0.0:8080
// 用法: node serve-pwa.js   (然后手机浏览器访问 http://<本机局域网IP>:8080)
const http = require('http');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, 'www');
const port = 8080;

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.mjs':  'application/javascript; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webmanifest': 'application/manifest+json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.wasm': 'application/wasm'
};

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  if (urlPath === '/') urlPath = '/index.html';
  const filePath = path.join(root, urlPath);
  if (!filePath.startsWith(root)) { res.writeHead(403); res.end('Forbidden'); return; }
  fs.readFile(filePath, (err, data) => {
    if (err) {
      // SPA / 兜底回 index.html
      fs.readFile(path.join(root, 'index.html'), (e2, d2) => {
        if (e2) { res.writeHead(404); res.end('Not found'); }
        else { res.writeHead(200, { 'Content-Type': mime['.html'] }); res.end(d2); }
      });
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

server.listen(port, '0.0.0.0', () => {
  console.log(`PWA 已启动: http://0.0.0.0:${port}`);
  console.log(`手机同局域网访问: http://<本机IP>:${port}`);
  console.log(`提示: Service Worker 需要 HTTPS 才能"添加到主屏幕"。`);
  console.log(`      如需真·PWA安装，可加隧道: cloudflared tunnel --url http://localhost:${port}`);
});
