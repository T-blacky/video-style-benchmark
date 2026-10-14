#!/usr/bin/env python3
"""Install curated REAL reference artworks, replacing the six low-detail placeholders.

Data is downloaded from Wikimedia Commons, resized to 768x768 for consistent
model input while retaining each painting's distinctive original texture.
Not an official benchmark from UniVST, FreeViS or TokenFlow.

Requires: pip install requests Pillow
"""
from __future__ import annotations
import hashlib
import io
import json
import time
from pathlib import Path
from urllib.parse import quote

import requests
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "styles"
ARTWORKS = {
    "ink_wash": "Landscape_attributed_to_Sesshu_Toyo,_Honolulu_Museum_of_Art.JPG",
    "oil_impasto": "Vincent_van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
    "watercolor": "Winslow_Homer_-_Gloucester_Harbor_(1873,_watercolour).jpg",
    "comic_cel": "Little_Nemo_in_Slumberland_(1908-07-26)_panels_11_to_15.jpg",
    "cubism": "Juan_Gris_-_Cubist_Still_Life_(1915).jpg",
    "pixel_art": "Landscape_pixel_art.png",
}
HEADERS = {
    "User-Agent": "VideoStyleBenchmarkReferenceFetcher/1.1 (research data preparation; https://github.com/T-blacky/video-style-benchmark)",
    "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
}

def download(name: str) -> Image.Image:
    canonical = ARTWORKS[name]
    title = "File:" + canonical
    sess = requests.Session()
    sess.headers.update(HEADERS)
    options = []
    try:
        resp = sess.get("https://commons.wikimedia.org/w/api.php", params={
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url", "iiurlwidth": "960", "titles": title,
        }, timeout=30)
        resp.raise_for_status()
        pages = resp.json()["query"]["pages"].values()
        for page in pages:
            for info in page.get("imageinfo", []):
                if info.get("thumburl"):
                    options.append(info["thumburl"])
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Commons API fallback for {name}: {e}", flush=True)

    # Derive the standard Wikimedia thumbnail URL as independent fallback.
    digest = hashlib.md5(canonical.encode("utf-8")).hexdigest()
    encoded = quote(canonical, safe="(),")
    ext = canonical.rsplit(".", 1)[-1].lower()
    suffix = ".png" if ext == "svg" else ""
    thumb = ("https://upload.wikimedia.org/wikipedia/commons/thumb/"
             f"{digest[0]}/{digest[:2]}/{encoded}/960px-{encoded}{suffix}")
    options.append(thumb)
    options.append("https://commons.wikimedia.org/wiki/Special:Redirect/file/" + quote(canonical) + "?width=960")
    errors = []
    for url in list(dict.fromkeys(options)):
        for attempt in range(2):
            try:
                r = sess.get(url, timeout=80, allow_redirects=True)
                r.raise_for_status()
                if not r.headers.get("Content-Type", "").startswith("image/"):
                    raise ValueError(f"Not an image: {r.headers.get('Content-Type')}")
                im = Image.open(io.BytesIO(r.content))
                im.load()
                if min(im.size) < 40:
                    raise ValueError(f"Image unexpectedly small: {im.size}")
                print(f"Downloaded {name}: {im.size} via {r.url}", flush=True)
                return im.convert("RGB")
            except (requests.RequestException, ValueError, OSError) as e:
                errors.append(f"{url}: {e}")
                time.sleep(2)
    raise RuntimeError("All image sources failed for " + name + ":\n" + "\n".join(errors))

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hashes = []
    for name in ARTWORKS:
        im = download(name)
        # Preserve image content (no center-crop of paintings/scrolls).
        # For references with a different aspect ratio, neutral mat/pad to square.
        if name == "pixel_art":
            # Downsample *before* NEAREST upscaling, preserving visible pixel clusters.
            im.thumbnail((192, 192), Image.Resampling.NEAREST)
            im = ImageOps.pad(im, (768, 768), Image.Resampling.NEAREST, color=(244, 240, 228))
        else:
            im = ImageOps.pad(im, (768, 768), Image.Resampling.LANCZOS, color=(245, 242, 234))
        path = OUT / f"{name}.png"
        im.save(path, optimize=True)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.append(digest)
        print(f"Saved {path.relative_to(ROOT)} ({path.stat().st_size} bytes; SHA256 {digest[:12]})", flush=True)
    if len(set(hashes)) != len(hashes):
        raise ValueError("Style images accidentally identical")
    print("Installed six authentic and visually distinct style references.", flush=True)

if __name__ == "__main__":
    main()
