# Generates the app icon (Tamil letter அ — the first letter, as in Kural 1 — on the edition's brown)
# for iOS and Android. Run: python3 apps/icon/make_icons.py
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
APPS = os.path.dirname(HERE)
FONT = os.path.expanduser("~/.fonts/NotoSansTamil-Bold.ttf")
BROWN, PAPER = (0x8A, 0x4B, 0x00), (0xFF, 0xFD, 0xF8)

def draw(size, letter_scale=0.62, bg=True):
    img = Image.new("RGBA", (size, size), BROWN + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, int(size * letter_scale))
    box = d.textbbox((0, 0), "அ", font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((size - w) / 2 - box[0], (size - h) / 2 - box[1]), "அ", font=f, fill=PAPER)
    return img

master = draw(1024)
master.convert("RGB").save(os.path.join(HERE, "icon_1024.png"))
ios = os.path.join(APPS, "ios", "Thirukkural", "Assets.xcassets", "AppIcon.appiconset")
master.convert("RGB").save(os.path.join(ios, "AppIcon-1024.png"))
open(os.path.join(ios, "Contents.json"), "w").write(
    '{"images":[{"filename":"AppIcon-1024.png","idiom":"universal","platform":"ios","size":"1024x1024"}],'
    '"info":{"author":"xcode","version":1}}')

res = os.path.join(APPS, "android", "app", "src", "main", "res")
for name, px in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    d = os.path.join(res, f"mipmap-{name}"); os.makedirs(d, exist_ok=True)
    draw(px * 4).resize((px, px), Image.LANCZOS).save(os.path.join(d, "ic_launcher.png"))
    # adaptive foreground: 108dp canvas, letter kept inside the 66dp safe zone
    fg = px * 108 // 48
    draw(fg * 4, letter_scale=0.38, bg=False).resize((fg, fg), Image.LANCZOS).save(os.path.join(d, "ic_launcher_foreground.png"))
any_dir = os.path.join(res, "mipmap-anydpi-v26"); os.makedirs(any_dir, exist_ok=True)
open(os.path.join(any_dir, "ic_launcher.xml"), "w").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
    '    <background android:drawable="@color/ic_launcher_background"/>\n'
    '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>\n')
open(os.path.join(res, "values", "ic_launcher_background.xml"), "w").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#8A4B00</color>\n</resources>\n')
print("icons written")
