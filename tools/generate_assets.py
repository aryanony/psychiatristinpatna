import os
from PIL import Image

src_banner = r'C:\Users\aryn1\.gemini\antigravity-ide\brain\5921805e-abc8-4890-8ea9-7c84a5f26dba\.user_uploaded\media_1792180152757.jpg'
logo_full_path = 'assets/img/logo-full.png'

# 1. Process Banner & OG Images
print('Loading banner from', src_banner)
im_banner = Image.open(src_banner).convert('RGB')
im_banner.save('assets/img/clinic-showcase-banner.jpg', 'JPEG', quality=95, optimize=True)
im_banner.save('assets/img/og-banner.jpg', 'JPEG', quality=95, optimize=True)

# Generate 1200x630 standard OG Image
og_w, og_h = 1200, 630
# Banner is 1024x576 (aspect ratio 1.777, whereas 1200/630 is 1.904)
# Scale banner so it fills width 1200, height = 1200 * 576 / 1024 = 675
# Then crop 22px top and 23px bottom to reach exactly 630px height without distorting!
scale_w = 1200
scale_h = int(1200 * 576 / 1024) # 675
im_scaled = im_banner.resize((scale_w, scale_h), Image.Resampling.LANCZOS)
top_crop = (scale_h - og_h) // 2 # ~22
bottom_crop = top_crop + og_h
im_og = im_scaled.crop((0, top_crop, og_w, bottom_crop))

im_og.save('assets/img/og-image.jpg', 'JPEG', quality=95, optimize=True)
im_og.save('og-image.jpg', 'JPEG', quality=95, optimize=True)
print('Saved assets/img/og-image.jpg and root og-image.jpg (1200x630)')

# 2. Process Favicons from Logo
print('Loading logo from', logo_full_path)
im_logo = Image.open(logo_full_path).convert('RGBA')

# Create square canvas on white background
w, h = im_logo.size
max_dim = max(w, h)
sq_logo = Image.new('RGBA', (max_dim, max_dim), (255, 255, 255, 255))
offset_x = (max_dim - w) // 2
offset_y = (max_dim - h) // 2
sq_logo.paste(im_logo, (offset_x, offset_y), im_logo)

# Generate sizes
sizes = {
    'assets/img/favicon-16x16.png': 16,
    'assets/img/favicon-32x32.png': 32,
    'assets/img/favicon-48x48.png': 48,
    'assets/img/favicon-64.png': 64,
    'assets/img/apple-touch-icon.png': 180,
    'apple-touch-icon.png': 180,
    'apple-touch-icon-precomposed.png': 180,
    'assets/img/icon-192.png': 192,
    'android-chrome-192x192.png': 192,
    'assets/img/icon-512.png': 512,
    'android-chrome-512x512.png': 512,
}

for path, size in sizes.items():
    resized = sq_logo.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(path, 'PNG', optimize=True)
    print(f'Generated {path} ({size}x{size})')

# Create multi-resolution favicon.ico
ico_16 = sq_logo.resize((16, 16), Image.Resampling.LANCZOS)
ico_32 = sq_logo.resize((32, 32), Image.Resampling.LANCZOS)
ico_48 = sq_logo.resize((48, 48), Image.Resampling.LANCZOS)
ico_16.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
ico_16.save('assets/img/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
print('Generated multi-res favicon.ico (16, 32, 48)')

print('All image assets and favicon suites generated successfully!')
