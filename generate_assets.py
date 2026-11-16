"""Generate the profile's own artwork; no external badge or tracking services."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random, html

OUT=Path(__file__).parent/'assets'
OUT.mkdir(exist_ok=True)
W,H=1200,360
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',n)
small=font(16);medium=font(21);large=font(88)
rng=random.Random(33)
stars=[(rng.randrange(W),rng.randrange(210),rng.randrange(1,3)) for _ in range(64)]
frames=[]
for frame in range(40):
    t=frame/40
    im=Image.new('RGB',(W,H),(8,11,23));d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/H
        d.line((0,y,W,y),fill=(int(8+7*a),int(11+4*a),int(23+18*a)))
    for x,y,r in stars:d.ellipse((x,y,x+r,y+r),fill=(58,75,111))
    glow=Image.new('RGB',(W,H));g=ImageDraw.Draw(glow)
    g.ellipse((750,-160,1270,330),outline=(98,40,140),width=25)
    g.ellipse((-180,170,280,630),outline=(0,95,107),width=20)
    im=Image.blend(im,glow.filter(ImageFilter.GaussianBlur(65)),.5);d=ImageDraw.Draw(im)
    # A smooth moving horizon grid, with no flashes or strobing.
    horizon=252
    d.line((0,horizon,W,horizon),fill=(40,88,106))
    for x in range(-W,W*2,100):d.line((W//2,horizon,x,H),fill=(27,49,78))
    for i in range(11):
        z=((i+t)/11)**2;y=horizon+int(z*(H-horizon))
        d.line((0,y,W,y),fill=(30,54,82))
    d.rounded_rectangle((50,35,305,65),radius=15,outline=(58,95,105),fill=(13,30,41))
    d.ellipse((64,46,72,54),fill=(87,242,197));d.text((83,42),'PLAYER / BUILDER / GRIM',font=small,fill=(148,210,207))
    d.text((49,89),'33GRIM33',font=large,fill=(229,243,249),stroke_width=0)
    d.text((55,193),'CODE. BUILD. RESPAWN.',font=medium,fill=(88,239,209))
    d.text((56,292),'RUST  /  PYTHON  /  TYPESCRIPT',font=small,fill=(162,176,207))
    # Quiet orbit animation around an abstract pixel controller.
    cx,cy=1000,135
    d.ellipse((cx-76,cy-76,cx+76,cy+76),outline=(76,61,127),width=2)
    a=t*math.tau;x=cx+76*math.cos(a);y=cy+76*math.sin(a)
    d.ellipse((x-5,y-5,x+5,y+5),fill=(126,119,255))
    d.rounded_rectangle((cx-52,cy-28,cx+52,cy+32),radius=17,fill=(24,35,56),outline=(111,130,166),width=2)
    d.rectangle((cx-30,cy-12,cx-23,cy+13),fill=(87,242,197));d.rectangle((cx-39,cy-3,cx-14,cy+4),fill=(87,242,197))
    d.ellipse((cx+17,cy-13,cx+28,cy-2),fill=(164,140,255));d.ellipse((cx+30,cy+1,cx+41,cy+12),fill=(87,242,197))
    d.line((55,335,1145,335),fill=(43,58,82))
    progress=55+int(t*1090);d.line((progress,335,min(progress+65,1145),335),fill=(87,242,197),width=2)
    frames.append(im)
frames[0].save(OUT/'banner-still.png')
frames[0].save(OUT/'banner.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)

def card(filename,kicker,title,lines,stack,accent):
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="205" viewBox="0 0 900 205" role="img" aria-label="{html.escape(title)}">
<rect x="1" y="1" width="898" height="203" rx="18" fill="#101728" stroke="#293550"/>
<rect x="1" y="28" width="4" height="66" rx="2" fill="{accent}"/>
<g font-family="'Segoe UI',Arial,sans-serif"><text x="30" y="35" fill="{accent}" font-size="12" letter-spacing="3">{html.escape(kicker)}</text>
<text x="30" y="73" fill="#e5f3f9" font-size="27" font-weight="700">{html.escape(title)}</text>'''
    for i,line in enumerate(lines):s+=f'<text x="30" y="{104+i*23}" fill="#bdcadc" font-size="16">{html.escape(line)}</text>'
    s+=f'<text x="30" y="178" fill="{accent}" font-size="13">{html.escape(stack)}</text><text x="855" y="75" fill="{accent}" font-size="29">&#8599;</text></g></svg>'
    (OUT/filename).write_text(s,encoding='utf-8')

card('attentiontwin.svg','01 / FEATURED BUILD','AttentionTwin',['A digital wellness app for focus sessions, better breaks and scrolling goals.','Local notification rules, an encrypted inbox and optional Gemini review.'],'REACT  /  TYPESCRIPT  /  JAVA  /  ANDROID','#57f2c5')
card('dev-pulse.svg','02 / DATA + DEVELOPER TOOLS','Dev Pulse',['A tech intelligence dashboard exploring 47M+ Hacker News posts.','DuckDB and Parquet meet a FastAPI, React and D3.js interface.'],'PYTHON  /  FASTAPI  /  REACT  /  D3.JS','#b7a1ff')
card('rust.svg','03 / LEARNING LAB','Rust projects',['A workspace for Rust projects and experiments.','Building, exploring and learning one project at a time.'],'RUST  /  EXPERIMENTS  /  DEVELOPER TOOLS','#ffb98a')
print('Generated',len(list(OUT.iterdir())),'profile assets.')
