#!/usr/bin/env python3
"""Download the libraries and fonts once, so Eden never needs the internet to start.

Run this ONCE on a computer with internet:   python3 tools/vendor.py
Then run  python3 tools/stamp.py  and upload everything, including the new vendor/ folder.
(index.html already looks in vendor/ first and only falls back to the CDN if a file is missing.)"""
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(ROOT, 'vendor'); FONTS = os.path.join(VENDOR, 'fonts')
LIBS = {
    'chart.umd.min.js':   'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js',
    'jspdf.umd.min.js':   'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
    'html2canvas.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js',
}
FONT_CSS = ('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800'
            '&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap')
KEEP = ('latin', 'latin-ext')          # the character sets Eden needs (English / Swahili)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def get(url, ua=None):
    req = urllib.request.Request(url, headers={'User-Agent': ua or UA})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()

os.makedirs(FONTS, exist_ok=True)
listed = []
for name, url in LIBS.items():
    print('downloading', name); data = get(url)
    if len(data) < 10000: sys.exit('%s looks wrong (%d bytes)' % (name, len(data)))
    open(os.path.join(VENDOR, name), 'wb').write(data); listed.append(name)

print('downloading fonts')
css = get(FONT_CSS).decode('utf-8')
blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
out, got = [], {}
for subset, block in blocks:
    if subset not in KEEP: continue
    url = re.search(r'url\((https://[^)]+)\)', block).group(1)
    if url not in got:
        fname = re.sub(r'[^A-Za-z0-9._-]', '_', url.split('/')[-1])
        if not fname.endswith('.woff2'): fname += '.woff2'
        open(os.path.join(FONTS, fname), 'wb').write(get(url)); got[url] = fname
    out.append('/* %s */\n%s' % (subset, block.replace(url, 'fonts/' + got[url])))
if not out: sys.exit('no fonts found in the Google Fonts response')
open(os.path.join(VENDOR, 'fonts.css'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
listed += ['fonts.css'] + ['fonts/' + f for f in sorted(set(got.values()))]
json.dump(listed, open(os.path.join(VENDOR, 'manifest.json'), 'w'), indent=1)
print('done: %d files in vendor/. Now run: python3 tools/stamp.py' % len(listed))
