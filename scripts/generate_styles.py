#!/usr/bin/env python3
"""Generate visually differentiated, deliberately simple PNG style references.

These are procedural FALLBACKS, not the high-detail AI-generated references
in the companion v0.2 ZIP, and not an official paper dataset.
"""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
def render(kind):
    rnd = random.Random(100 + ["ink_wash", "oil_impasto", "watercolor", "comic_cel", "cubism", "pixel_art"].index(kind))
    pix = kind == "pixel_art"
    S = 64 if pix else 512
    k = S / 512
    def pt(x, y): return (round(x*k), round(y*k))
    if kind == "ink_wash": palette = ("#f6f3e9", "#dad9d0", "#999e9b", "#202524", "#080908")
    elif kind == "oil_impasto": palette = ("#e85a24", "#ffb640", "#2583c3", "#134d86", "#10264c")
    elif kind == "watercolor": palette = ("#f3e9e3", "#e6b7c6", "#8ac9de", "#83b4a4", "#58819a")
    elif kind == "comic_cel": palette = ("#139bd8", "#ffdf6e", "#53b883", "#117bb6", "#162b43")
    elif kind == "cubism": palette = ("#c97845", "#dec087", "#70a6a9", "#246475", "#453f51")
    else: palette = ("#e26d9d", "#fac66c", "#72bfcb", "#337fb7", "#27376e")
    img = Image.new("RGB", (S, S), palette[0])
    d = ImageDraw.Draw(img)
    def polygon(verts, color, outline=None, width=1):
        p = [pt(*v) for v in verts]
        d.polygon(p, fill=color)
        if outline:
            d.line(p+[p[0]], fill=outline, width=max(1,round(width*k)), joint="curve")
    def rectangle(box, color, outline=None, width=1):
        d.rectangle((*pt(box[0],box[1]), *pt(box[2],box[3])), fill=color, outline=outline, width=max(1,round(width*k)))
    def ellipse(box, color):
        d.ellipse((*pt(box[0],box[1]), *pt(box[2],box[3])), fill=color)
    line = palette[4] if kind in ("comic_cel", "ink_wash") else None
    width = 7 if kind == "comic_cel" else 3
    ellipse((354, 60, 455, 160), palette[1])
    polygon([(0,300),(143,90),(245,293)], palette[2], line, width)
    polygon([(120,300),(299,71),(512,315)], palette[3], line, width)
    polygon([(0,298),(512,298),(512,512),(0,512)], palette[2])
    polygon([(0,377),(180,346),(321,387),(512,352),(512,512),(0,512)], palette[3])
    for x,y,size in [(58,280,58),(120,267,67),(443,275,66),(486,289,63)]:
        polygon([(x-size*.5,y+58),(x,y-size),(x+size*.5,y+58)], palette[4])
        rectangle((x-6,y+48,x+6,y+91),palette[4])
    rectangle((197,294,316,393),palette[1],line,width)
    polygon([(181,299),(257,231),(332,299)],palette[4],line,width)
    rectangle((240,343,269,393),palette[3],line,width)
    rectangle((214,323,240,348),palette[2],line,width)
    for j in range(9):
        y=397+j*11
        d.line([pt(0,y),pt(512,y+4*(j%2))],fill=palette[1],width=max(1,round((3 if pix else 2)*k)))
    if kind == "cubism":
        for i in range(62):
            x=rnd.randrange(512); y=rnd.randrange(512)
            vertices=[(x,y),(x+rnd.randint(-110,100),y+rnd.randint(-80,110)),(x+rnd.randint(-110,100),y+rnd.randint(-100,80))]
            polygon(vertices, rnd.choice(palette[1:]), outline=palette[4] if i%7==0 else None)
    elif kind == "oil_impasto":
        d=ImageDraw.Draw(img,"RGBA")
        colors=[(255,237,108,180),(0,65,163,160),(254,99,17,160),(22,129,200,160)]
        for i in range(2600):
            x=rnd.randrange(S); y=rnd.randrange(S)
            dx=rnd.randrange(4,26);dy=rnd.randrange(-5,7)
            d.line([(x,y),(min(S-1,x+dx),max(0,min(S-1,y+dy)))], fill=rnd.choice(colors),width=rnd.randint(1,4))
    elif kind == "watercolor":
        blurred=img.filter(ImageFilter.GaussianBlur(radius=4))
        img=Image.blend(img,blurred,.67)
        d=ImageDraw.Draw(img,"RGBA")
        for i in range(260):
            x=rnd.randrange(S);y=rnd.randrange(S);r=rnd.randrange(4,32)
            d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,rnd.randrange(5,23)))
        img=Image.blend(img,Image.new("RGB",(S,S),"#fffaf4"),.13)
    elif kind == "ink_wash":
        img=img.convert("L").convert("RGB")
        d=ImageDraw.Draw(img,"RGBA")
        for i in range(380):
            x=rnd.randrange(S);y=rnd.randrange(S)
            d.line([(x,y),(x+rnd.randrange(-16,17),y+rnd.randrange(-18,19))],fill=(10,10,10,rnd.randrange(10,60)),width=rnd.randrange(1,4))
    elif kind == "comic_cel":
        for i in range(400):
            x=rnd.randrange(0,S,11);y=rnd.randrange(S//2,S,11)
            d.ellipse((x,y,x+2,y+2), fill="#0e4563")
    if pix:
        img=img.resize((512,512),Image.Resampling.NEAREST)
    return img

def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Disabled to protect curated artwork references")
    args=ap.parse_args()
    if args.force:
        raise SystemExit("Refusing --force: the repository includes curated artworks. Use install_style_artworks.py to refresh from documented sources.")
    target=ROOT/"data/styles"
    target.mkdir(parents=True,exist_ok=True)
    for name in ["ink_wash","oil_impasto","watercolor","comic_cel","cubism","pixel_art"]:
        p=target/f"{name}.png"
        if p.exists() and not args.force:
            print(f"Keeping existing style: {p}")
            continue
        render(name).save(p)
        print(f"Generated fallback: {p}")
if __name__=="__main__":
    main()
