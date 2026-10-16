#!/usr/bin/env python3
"""
Downloads doctor portrait, clinic visuals, and certificates from Practo and DocTube.
"""
import urllib.request
import os

assets = {
    'doctor-sachchidanand-singh.jpg': 'https://imagesx.practo.com/providers/dr-sachchidanand-singh-neuropsychiatry-patna-6093b8fb-e6d7-400c-8c18-0f1034f3f8f8.jpg',
    'doctor-video-thumbnail.png': 'https://img.doctube.com/IgfISfoAxCINwkcC7Zvl_22_e3053f221d10d80e3477184e5a0c41fc_image.png',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

dest_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'img')
os.makedirs(dest_dir, exist_ok=True)

for filename, url in assets.items():
    target = os.path.join(dest_dir, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp, open(target, 'wb') as out_f:
            out_f.write(resp.read())
        size = os.path.getsize(target)
        print(f"Downloaded {filename} ({size} bytes)")
    except Exception as err:
        print(f"Failed to download {filename} from {url}: {err}")
