"""Original terminal profile artwork. Python 3 + Pillow; no network needed.

Text remains readable throughout the one-time entry transition. The cursor
is the only looping animation. Motion preferences are respected.
"""
from pathlib import Path
from html import escape
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
BG,FG,COPPER,MUTED,RULE='#0b0e12','#e4dfd8','#dda16c','#aaa59d','#3b2d23'
FONT='/System/Library/Fonts/Menlo.ttc'
if not Path(FONT).exists():FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'


def text(x,y,s,size=18,color=FG,bold=False):
    return f'<text x="{x}" y="{y}" font-family="Menlo, Consolas, monospace" font-size="{size}" font-weight="{600 if bold else 400}" fill="{color}">{escape(s)}</text>'


def para(s,x,y,width,size=18,leading=29,color=MUTED):
    f=ImageFont.truetype(FONT,size);lines=[];line=''
    for word in s.split():
        trial=(line+' '+word).strip()
        if f.getlength(trial)>width and line:lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    return ''.join(text(x,y+i*leading,line,size,color) for i,line in enumerate(lines)),y+len(lines)*leading


def prompt(x,y,command,size=19):
    return text(x,y,'$',size,COPPER)+text(x+24,y,command,size,FG)


def svg(w,h,c,title,edges=True):
    frame=f'<path d="M1 0V{h}M{w-1} 0V{h}" stroke="{RULE}"/>' if edges else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>text{{text-rendering:optimizeLegibility}}.enter{{animation:enter .65s ease-out both}}.cursor{{animation:cursor 1.2s steps(2,end) infinite}}.boot{{stroke-dasharray:1000;animation:boot 1s ease-out both}}@keyframes enter{{from{{transform:translateY(5px)}}to{{transform:translateY(0)}}}}@keyframes cursor{{50%{{opacity:.2}}}}@keyframes boot{{from{{stroke-dashoffset:1000}}to{{stroke-dashoffset:0}}}}@media(prefers-reduced-motion:reduce){{.enter,.cursor,.boot{{animation:none}}}}</style><rect width="{w}" height="{h}" fill="{BG}"/>{frame}{c}</svg>'''


def save(name,w,h,c,title,edges=True):
    (OUT/f'{name}.svg').write_text(svg(w,h,c,title,edges),encoding='utf-8')


def overview(mobile):
    w=600 if mobile else 1000
    c=f'<path d="M1 43V15Q1 1 15 1H{w-15}Q{w-1} 1 {w-1} 15V43Z" fill="#17191d" stroke="{RULE}"/>'
    for x,color in [(24,'#dda16c'),(44,'#94714f'),(64,'#554637')]:c+=f'<circle cx="{x}" cy="22" r="5" fill="{color}"/>'
    c+=text(101,27,'samuel@github: ~ / portfolio',14 if mobile else 16,MUTED)
    c+=f'<path class="boot" d="M1 43H{w-1}" stroke="{COPPER}" stroke-opacity=".6"/>'
    c+='<g class="enter">'+prompt(28,90,'whoami',23 if mobile else 20)
    c+=f'<rect class="cursor" x="{139 if mobile else 128}" y="{72 if mobile else 74}" width="10" height="20" fill="{COPPER}"/>'
    c+=text(28,136,'Samuel Guedes',35 if mobile else 36,FG,True)
    c+=text(28,173,'Full stack / back-end',23 if mobile else 19,COPPER)
    c+=prompt(28,230 if mobile else 226,'cat about.md',23 if mobile else 20)
    bio='Desenvolvo APIs e aplicações web com autenticação, permissões e regras de negócio.'
    if mobile:
        p,y=para(bio,28,271,w-56,23,33);c+=p
        p,y=para('ADS na Impacta. Técnico em Informática pela ETEC.',28,y+9,w-56,22,32);c+=p
        c+=prompt(28,y+38,'cat stack.yml',23);y+=81
        for key,value in [('backend','Node.js / Express / JavaScript / Java'),('data','MySQL / SQL / Sequelize'),('frontend','React / MUI / HTML / CSS')]:
            c+=text(28,y,key+':',21,COPPER)
            p,ny=para(value,48,y+31,w-76,21,31,FG);c+=p;y=ny+12
        c+=prompt(28,y+32,'ls ~/projects',23)
        h=y+58
    else:
        p,y=para(bio,28,264,534,18,29);c+=p
        p,y=para('ADS na Impacta. Técnico em Informática pela ETEC.',28,y+10,534,18,29);c+=p
        c+=f'<path d="M603 207V377" stroke="{RULE}"/>'
        c+=prompt(633,226,'cat stack.yml',20)
        for yy,key,value in [(265,'backend','Node.js / Express / JavaScript'),(314,'data','MySQL / SQL / Sequelize'),(363,'frontend','React / MUI / HTML / CSS')]:
            c+=text(633,yy,key+':',16,COPPER)+text(633,yy+24,value,16,FG)
        c+=prompt(28,434,'ls ~/projects',20)
        h=465
    c+='</g>'
    save('terminal-overview'+('-mobile' if mobile else ''),w,h,c,'Terminal de Samuel Guedes: whoami, sobre mim, formação e tecnologias.')


def project(mobile,helpdesk):
    w=300 if mobile else 500;x=20 if mobile else 28
    name='helpdesk' if helpdesk else 'purchase-approval'
    c=text(x,29,'[dir] '+name,18 if mobile else 19,COPPER)
    titles=['Help Desk','Ticket System'] if helpdesk else ['Purchase Approval','System']
    for y,s in [(66,titles[0]),(96,titles[1])]:c+=text(x,y,s,23 if mobile else 25,FG,True)
    desc='Chamados com acesso por perfil, chat e aprovação financeira.' if helpdesk else 'Aprovações condicionais e permissões por departamento.'
    p,y=para(desc,x,133,w-2*x,19 if mobile else 17,27);c+=p
    if mobile:
        c+=text(x,257,'Node.js / React',17,COPPER)+text(x,281,'JWT / MySQL' if helpdesk else 'Sequelize / MySQL',17,COPPER)
        y=320
    else:
        c+=text(x,213,'Node.js / React / JWT / MySQL' if helpdesk else 'Node.js / React / Sequelize / MySQL',16,COPPER);y=251
    c+=text(x,y,'[ abrir repositório ]',19 if mobile else 17,FG)
    # Only the outside edge belongs to the terminal frame.
    c+=f'<path d="M{w-1 if helpdesk else 1} 0V{350 if mobile else 278}" stroke="{RULE}"/>'
    save(('terminal-helpdesk' if helpdesk else 'terminal-purchase')+('-mobile' if mobile else ''),w,350 if mobile else 278,c,('Help Desk Ticket System' if helpdesk else 'Purchase Approval System')+'. Abrir repositório.',False)


def contact(label,name,left=False,right=False):
    for mobile in [False,True]:
        w,h=(200,88) if mobile else (333,86)
        c=f'<rect y="0" width="{w}" height="{h}" fill="#141619"/><path d="M0 1H{w}M0 {h-1}H{w}" stroke="{RULE}"/>'
        c+=text(20,52,'[ '+label+' ]',21 if mobile else 20,COPPER)
        if left:c+=f'<path d="M1 0V{h}" stroke="{RULE}"/>'
        if right:c+=f'<path d="M{w-1} 0V{h}" stroke="{RULE}"/>'
        save(name+('-mobile' if mobile else ''),w,h,c,label,False)


def picture(name,alt,width='100%'):
    return f'<picture><source media="(max-width:600px)" srcset="./assets/{name}-mobile.svg"><img align="top" src="./assets/{name}.svg" width="{width}" alt="{alt}"></picture>'


def main():
    OUT.mkdir(exist_ok=True)
    for mobile in [False,True]:
        overview(mobile)
        for helpdesk in [False,True]:project(mobile,helpdesk)
    contact('portfólio','terminal-portfolio',True)
    contact('linkedin','terminal-linkedin')
    contact('e-mail','terminal-email',right=True)
    portfolio='https://portifolio-samuel-svm7.vercel.app/'
    parts=['<!-- Original terminal artwork. Regenerate: python3 scripts/build_profile.py -->\n<p align="center">']
    parts.append('<a href="'+portfolio+'">'+picture('terminal-overview','Samuel Guedes. Full stack com foco em back-end. Desenvolvo APIs e aplicações web com autenticação, permissões e regras de negócio. ADS na Impacta. Técnico em Informática pela ETEC. Node.js, Express, JavaScript, Java, MySQL, SQL, Sequelize, React, Material UI, HTML e CSS.')+'</a>')
    for name,repo,alt in [('terminal-purchase','purchase-approval-system','Purchase Approval System. Aprovações condicionais e permissões por departamento. Node.js, React, Sequelize e MySQL. Abrir repositório.'),('terminal-helpdesk','helpdesk-ticket-system','Help Desk Ticket System. Acesso por perfil, chat com polling HTTP e aprovação financeira. Node.js, React, JWT e MySQL. Abrir repositório.')]:
        parts.append(f'<a href="https://github.com/samuelguedesss/{repo}">'+picture(name,alt,'50%')+'</a>')
    for name,url,alt in [('terminal-portfolio',portfolio,'Portfólio'),('terminal-linkedin','https://www.linkedin.com/in/samuel-fguedes/','LinkedIn'),('terminal-email','mailto:samuelguedes473@gmail.com','E-mail')]:parts.append(f'<a href="{url}">'+picture(name,alt,'33.33%')+'</a>')
    parts.append('</p>\n');(ROOT/'README.md').write_text(''.join(parts),encoding='utf-8')
    (OUT/'README.md').write_text('# Artes do perfil\n\nTerminal original em preto e cobre: comandos, apresentação, tecnologias, projetos e contatos clicáveis. Versões próprias para computador e celular. Transição de entrada suave, texto sempre visível e cursor animado, respeitando a preferência por movimento reduzido.\n\nRegenerar: `python3 scripts/build_profile.py` (Pillow).\n',encoding='utf-8')
    for pattern in ['compact-*.svg','link-*.svg']:
        for p in OUT.glob(pattern):p.unlink()
    print('Terminal desktop/mobile artwork generated.')


if __name__=='__main__':main()
