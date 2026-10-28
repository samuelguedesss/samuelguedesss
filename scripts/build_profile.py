"""Generate original profile artwork: python3 scripts/build_profile.py.

Requires Pillow (scripts/requirements.txt). No network or credentials needed.
"""
from pathlib import Path
import math
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ASSETS = Path(__file__).resolve().parents[1] / "assets"
ASSETS.mkdir(exist_ok=True)
BG, PANEL, COPPER, TEXT, MUTED, LINE = "#080A0D", "#101317", "#DFA16D", "#F3EEE8", "#AFA9A3", "#37302A"
W, H = 1200, 520


def font(size, mono=False, bold=False):
    names = (["/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"] if mono else
             [f"/System/Library/Fonts/Supplemental/Arial{' Bold' if bold else ''}.ttf",
              f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf"])
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    raise RuntimeError("Install Arial/Menlo or DejaVu Sans/Mono to regenerate artwork.")


F = {k: font(*v) for k, v in {
    "logo": (25, True, False), "meta": (12, True, False), "name": (69, False, True),
    "headline": (27, False, False), "body": (18, False, False), "chip": (14, True, False),
    "terminal": (13, True, False), "core": (46, True, False),
}.items()}


def ease(value):
    return 1 - (1 - max(0, min(1, value))) ** 3


def cover(t, still=False):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 48):
        d.line((x, 0, x, H), fill="#121519")
    for y in range(0, H, 48):
        d.line((0, y, W, y), fill="#121519")
    glow = Image.new("RGB", (W, H), "black")
    ImageDraw.Draw(glow).ellipse((735, 65, 1145, 465), fill="#382215")
    im = ImageChops.add(im, glow.filter(ImageFilter.GaussianBlur(65)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, W-2, H-2), radius=24, outline="#3E3025", width=2)
    d.text((44, 27), "[ sg. ]", font=F["logo"], fill=COPPER)
    d.text((174, 35), "FULL STACK / BACK-END FOCUS", font=F["meta"], fill=MUTED)
    d.text((986, 35), "SAMUEL GUEDES", font=F["meta"], fill=MUTED)
    d.line((44, 76, 1156, 76), fill=LINE)
    d.text((46, 114), "Samuel", font=F["name"], fill=TEXT)
    d.text((46, 186), "Guedes.", font=F["name"], fill=COPPER)
    d.text((49, 282), "Por trás da interface.", font=F["headline"], fill=TEXT)
    d.text((49, 320), "APIs, dados e regras de negócio.", font=F["body"], fill=MUTED)
    cx, cy = 948, 258
    for radius, col in [(168,"#493327"),(136,"#8C6040"),(100,"#443025")]:
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=col,width=1)
    angle = (0 if still else t * math.tau / 8) - math.pi/2
    for a, rad in [(angle,168),(angle+math.pi,136)]:
        x,y=cx+math.cos(a)*rad,cy+math.sin(a)*rad
        d.ellipse((x-4,y-4,x+4,y+4),fill=COPPER)
    d.line((cx-184,cy,cx-163,cy),fill=COPPER,width=2)
    d.line((cx+163,cy,cx+184,cy),fill=COPPER,width=2)
    d.rounded_rectangle((cx-49,cy-49,cx+49,cy+49),radius=24,fill="#171513",outline="#B07C52",width=2)
    d.text((cx-40,cy-31), "{ }",font=F["core"],fill=COPPER)
    for i,(label,x,y) in enumerate([("API",861,102),("SQL",1056,287),("JWT",800,322)]):
        p=1 if still else ease((t-i*.22)/.75)
        if p<=0:
            continue
        chip=Image.new("RGBA",(90,60),(0,0,0,0))
        cd=ImageDraw.Draw(chip)
        cd.rounded_rectangle((1,1,86,53),radius=13,fill=PANEL,outline="#785236",width=1)
        cd.text((28,18),label,font=F["chip"],fill=COPPER)
        chip.putalpha(chip.getchannel("A").point(lambda a:round(a*p)))
        im.paste(chip,(x,round(y+22*(1-p))),chip)
    for i,(label,width) in enumerate([("REST APIs",144),("JWT / RBAC",158),("MySQL",120)]):
        p=1 if still else ease((t-.35-i*.15)/.65)
        if p<=0:
            continue
        x=[49,205,375][i]
        layer=Image.new("RGBA",(width,45),(0,0,0,0))
        ld=ImageDraw.Draw(layer)
        ld.rounded_rectangle((0,0,width-1,39),radius=8,fill="#171615",outline="#58402D")
        ld.text((14,11),label,font=F["chip"],fill=COPPER)
        layer.putalpha(layer.getchannel("A").point(lambda a:round(a*p)))
        im.paste(layer,(x,round(378+18*(1-p))),layer)
    d=ImageDraw.Draw(im)
    d.line((44,459,1156,459),fill=LINE)
    d.text((49,480),"samuel@dev:~$",font=F["terminal"],fill=COPPER)
    command="building useful systems"
    count=len(command) if still else min(len(command),int(max(0,t-.35)*20))
    d.text((179,480),command[:count],font=F["terminal"],fill=MUTED)
    if still or int(t*2)%2==0:
        x=179+d.textlength(command[:count],font=F["terminal"])
        d.rectangle((x+3,481,x+9,494),fill=COPPER)
    d.text((887,480),"JAVA / NODE.JS / SQL",font=F["meta"],fill=MUTED)
    return im


def svg_document(width, height, title, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title>
<defs><radialGradient id="glow"><stop stop-color="#DFA16D" stop-opacity=".12"/><stop offset="1" stop-color="#DFA16D" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="{PANEL}" stroke="{LINE}"/>
<ellipse cx="{width-50}" cy="40" rx="210" ry="180" fill="url(#glow)"/>
<g font-family="Arial, Helvetica, sans-serif" fill="{TEXT}">{content}</g></svg>'''


def text(x,y,label,size=16,fill=TEXT,mono=False,weight=400):
    family=' font-family="Menlo, Consolas, monospace"' if mono else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"{family}>{escape(label)}</text>'


def project(filename, title, subtitle, lines, tags, nodes):
    content=text(30,37,subtitle,11,COPPER,True)
    content+=text(30,82,title[0],30,weight=600)+text(30,117,title[1],30,weight=600)
    for i,line in enumerate(lines):
        content+=text(30,153+i*23,line,16,MUTED)
    content+='<path d="M46 229H510" fill="none" stroke="#785236"/>'
    for x,label in zip([30,205,380],nodes):
        content+=f'<rect x="{x}" y="209" width="150" height="40" rx="8" fill="#191714" stroke="#785236"/>'
        content+=text(x+12,234,label,12,COPPER,True)
    content+='<path d="M30 274H530" stroke="#37302A"/>'
    content+=text(30,302,tags,11,MUTED,True)+text(30,335,"Ver código e documentação",14,COPPER)
    (ASSETS/filename).write_text(svg_document(560,358,' '.join(title),content),encoding="utf-8")
    # GIF cards retain their animation inside GitHub's image proxy.
    card=Image.new('RGB',(560,358),PANEL)
    d=ImageDraw.Draw(card)
    d.rounded_rectangle((1,1,558,356),radius=18,outline=LINE)
    d.text((30,25),subtitle,font=font(11,True),fill=COPPER)
    for y,label in [(53,title[0]),(88,title[1])]:
        d.text((30,y),label,font=font(30,bold=True),fill=TEXT)
    for i,line in enumerate(lines):
        d.text((30,138+i*23),line,font=font(16),fill=MUTED)
    d.line((46,229,510,229),fill='#785236')
    for x,label in zip([30,205,380],nodes):
        d.rounded_rectangle((x,209,x+150,249),radius=8,fill='#191714',outline='#785236')
        d.text((x+12,222),label,font=font(12,True),fill=COPPER)
    d.line((30,274,530,274),fill=LINE)
    d.text((30,291),tags,font=font(11,True),fill=MUTED)
    d.text((30,321),'Ver código e documentação',font=font(14),fill=COPPER)
    palette=card.quantize(colors=96)
    frames=[]
    for i in range(60):
        p=ease((i/10-(.2 if filename=='helpdesk.svg' else 0))/.8)
        base=Image.new('RGB',card.size,BG)
        base.paste(Image.blend(Image.new('RGB',card.size,BG),card,p),(0,round((1-p)*16)))
        if i>12:
            draw=ImageDraw.Draw(base)
            x=184+(i-13)%18/17*17
            draw.ellipse((x-2,227,x+2,231),fill=COPPER)
            x+=175
            draw.ellipse((x-2,227,x+2,231),fill=COPPER)
        frames.append(base.quantize(palette=palette,dither=Image.Dither.NONE))
    frames[0].save(ASSETS/filename.replace('.svg','.gif'),save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)


def build():
    cover(0,still=True).save(ASSETS/"profile-cover.png",optimize=True)
    palette=cover(0,still=True).quantize(colors=128)
    frames=[cover(i/10).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(80)]
    frames[0].save(ASSETS/"profile-cover.gif",save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)
    project("purchase-approval.svg",["Purchase Approval","System"],"REGRAS DE NEGÓCIO",
            ["Aprovações em até três etapas.","Permissões por perfil e departamento."],
            "REACT / NODE.JS / SEQUELIZE / MYSQL",["Requisição","Aprovação","Financeiro"])
    project("helpdesk.svg",["Help Desk","Ticket System"],"SUPORTE CONECTADO",
            ["Chamados, chat e notificações.","Acesso por perfil e aprovação financeira."],
            "REACT / EXPRESS / JWT / MYSQL",["Chamado","Atendimento","Resolução"])
    stack=''
    for y,label,value in [(42,"Back-end","Node.js · Express · JavaScript · Java"),(85,"Dados","MySQL · SQL · Sequelize"),(128,"Interface","React · Material UI · HTML · CSS"),(171,"Fundamentos","Git · APIs REST · JWT · RBAC")]:
        stack+=text(30,y,label,16,COPPER)+text(225,y,value,16,TEXT)
    (ASSETS/"stack.svg").write_text(svg_document(1120,202,"Minha stack de desenvolvimento",stack),encoding="utf-8")
    footer=text(32,44,"Vamos conectar ideias a sistemas.",23,TEXT,weight=500)
    footer+=text(32,77,"portifolio-samuel-svm7.vercel.app",14,COPPER,True)+text(981,62,"[ sg. ]",25,COPPER,True)
    (ASSETS/"footer.svg").write_text(svg_document(1120,108,"Conheça meu portfólio",footer),encoding="utf-8")
    for p in sorted(ASSETS.iterdir()):
        print(f"{p.name}: {p.stat().st_size:,} bytes")


if __name__=="__main__":
    build()
