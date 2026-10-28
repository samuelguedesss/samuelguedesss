"""Generate compact original profile artwork (Python 3 + Pillow).

Desktop and mobile layouts keep the same compact hierarchy. Text is static;
only decorative orbit marks move, respecting reduced-motion preferences.
"""
from pathlib import Path
from html import escape
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
BG,FG,COPPER,MUTED,RULE='#0d1015','#ece8e3','#d6a276','#b7b2ac','#302923'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
if not Path(FONT).exists(): FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def text(x,y,s,size=20,color=FG,bold=False):
    return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{600 if bold else 400}" fill="{color}">{escape(s)}</text>'


def paragraph(s,x,y,width,size=20,leading=29):
    f=ImageFont.truetype(FONT,size); lines=[];line=''
    for word in s.split():
        candidate=(line+' '+word).strip()
        if f.getlength(candidate)>width and line:lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    return ''.join(text(x,y+i*leading,s,size,MUTED) for i,s in enumerate(lines)),y+len(lines)*leading


def svg(w,h,c,title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>.orbit{{transform-box:fill-box;transform-origin:center;animation:spin 30s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}@media(prefers-reduced-motion:reduce){{.orbit{{animation:none}}}}</style><rect width="{w}" height="{h}" fill="{BG}"/>{c}</svg>'''


def save(name,w,h,c,title):
    (OUT/(name+'.svg')).write_text(svg(w,h,c,title),encoding='utf-8')


def line(w,y):return f'<path d="M32 {y}H{w-32}" stroke="{RULE}"/>'


def overview(mobile):
    w=600 if mobile else 1000
    c=text(32,61 if mobile else 70,'Samuel Guedes',43 if mobile else 46,FG,True)
    c+=text(32,99 if mobile else 106,'Full stack · foco em back-end',22 if mobile else 20,COPPER)
    cx,cy,r=(520,75,38) if mobile else (901,84,49)
    for rad in [r,r*.7]:c+=f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="#6c4c34"/>'
    c+=f'<g class="orbit"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="none"/><circle cx="{cx}" cy="{cy-r}" r="3" fill="{COPPER}"/><circle cx="{cx}" cy="{cy+r}" r="3" fill="{COPPER}"/></g>'
    c+=text(cx-17,cy+8,'{ }',24,COPPER)
    c+=line(w,142)
    c+=text(32,184,'Sobre mim',26 if mobile else 23,FG,True)
    bio='Desenvolvo aplicações web com foco em APIs REST, autenticação e regras de negócio.'
    if mobile:
        p,y=paragraph(bio,32,222,w-64,25,34);c+=p
        p,y=paragraph('ADS na Impacta · Técnico em Informática pela ETEC.',32,y+12,w-64,23,32);c+=p
        c+=line(w,y+8);c+=text(32,y+46,'Tecnologias',26,FG,True);y+=84
        for label,value in [('Back-end','Node.js · Express · JavaScript · Java'),('Dados','MySQL · SQL · Sequelize'),('Interface','React · Material UI · HTML · CSS')]:
            c+=text(32,y,label,22,COPPER)
            p,ny=paragraph(value,32,y+29,w-64,23,31);c+=p;y=ny+13
        c+=line(w,y+2)+text(32,y+41,'Projetos em destaque',26,FG,True)
        h=y+63
    else:
        p,y=paragraph(bio,32,220,540,20,29);c+=p
        p,y=paragraph('Estudo ADS na Impacta e tenho formação técnica em Informática pela ETEC.',32,y+10,540,20,29);c+=p
        c+=f'<path d="M620 177V330" stroke="{RULE}"/>'
        c+=text(657,184,'Tecnologias',23,FG,True)
        for yy,label,value in [(220,'Back-end','Node.js · Express · JavaScript · Java'),(269,'Dados','MySQL · SQL · Sequelize'),(318,'Interface','React · Material UI · HTML · CSS')]:
            c+=text(657,yy,label,17,COPPER)+text(657,yy+23,value,17,MUTED)
        c+=line(w,369)+text(32,409,'Projetos em destaque',23,FG,True)
        h=438
    save('compact-overview'+('-mobile' if mobile else ''),w,h,c,'Samuel Guedes. Full stack com foco em back-end. Sobre mim, formação e tecnologias.',)


def project(mobile,helpdesk):
    w=300 if mobile else 500
    x=20 if mobile else 32
    title=['Help Desk','Ticket System'] if helpdesk else ['Purchase Approval','System']
    c=text(x,32,'Chamados e suporte' if helpdesk else 'Aprovação de compras',16,COPPER)
    c+=text(x,73,title[0],26 if mobile else 28,FG,True)+text(x,105,title[1],26 if mobile else 28,FG,True)
    desc='Acesso por perfil, chat e aprovação financeira.' if helpdesk else 'Fluxo condicional e permissões por departamento.'
    p,y=paragraph(desc,x,144,w-2*x,21 if mobile else 19,29);c+=p
    if mobile:
        c+=text(x,y+15,'React · Node.js',18,COPPER)+text(x,y+41,'JWT · MySQL' if helpdesk else 'Sequelize · MySQL',18,COPPER);y+=45
    else:c+=text(x,y+18,'React · Node.js · JWT · MySQL' if helpdesk else 'React · Node.js · Sequelize · MySQL',17,COPPER);y+=25
    baseline=306 if mobile else 234
    c+=text(x,baseline,'Ver repositório',20 if mobile else 18,FG)
    c+=f'<path d="M{w-x-18} {baseline-14}l9 9-9 9" fill="none" stroke="{COPPER}" stroke-width="2"/>'
    # Equal stage sizes keep the pair aligned at each breakpoint.
    save(('compact-helpdesk' if helpdesk else 'compact-purchase')+('-mobile' if mobile else ''),w,330 if mobile else 255,c,('Help Desk Ticket System' if helpdesk else 'Purchase Approval System')+'. Clique para abrir o repositório.')


def contact(label,name):
    c=f'<path d="M0 1H333" stroke="{RULE}"/>'
    c+=text(32,51,label,25,COPPER)
    save(name,333,85,c,label)
    save(name+'-mobile',200,80,'<path d="M0 1H200" stroke="'+RULE+'"/>'+text(22,49,label,25,COPPER),label)


def picture(name,alt,width='100%'):
    return f'<picture><source media="(max-width:600px)" srcset="./assets/{name}-mobile.svg"><img align="top" src="./assets/{name}.svg" width="{width}" alt="{alt}"></picture>'


def main():
    OUT.mkdir(exist_ok=True)
    for mobile in [False,True]:
        overview(mobile)
        for helpdesk in [False,True]:project(mobile,helpdesk)
    for label,name in [('Portfólio','link-portfolio'),('LinkedIn','link-linkedin'),('E-mail','link-email')]:contact(label,name)
    portfolio='https://portifolio-samuel-svm7.vercel.app/'
    parts=['<!-- Original compact profile. Regenerate: python3 scripts/build_profile.py -->\n<p align="center">']
    parts.append('<a href="'+portfolio+'">'+picture('compact-overview','Samuel Guedes. Desenvolvedor full stack com foco em back-end, APIs REST, autenticação e regras de negócio. ADS na Impacta e Técnico em Informática pela ETEC. Back-end: Node.js, Express, JavaScript e Java. Dados: MySQL, SQL e Sequelize. Interface: React, Material UI, HTML e CSS.')+'</a>')
    for name,repo,alt in [('compact-purchase','purchase-approval-system','Purchase Approval System. Fluxo condicional e permissões por departamento. React, Node.js, Sequelize e MySQL. Abrir repositório.'),('compact-helpdesk','helpdesk-ticket-system','Help Desk Ticket System. Controle de acesso, chat por polling HTTP e aprovação financeira. React, Node.js, JWT e MySQL. Abrir repositório.')]:
        parts.append(f'<a href="https://github.com/samuelguedesss/{repo}">'+picture(name,alt,'50%')+'</a>')
    for name,url,alt in [('link-portfolio',portfolio,'Portfólio'),('link-linkedin','https://www.linkedin.com/in/samuel-fguedes/','LinkedIn'),('link-email','mailto:samuelguedes473@gmail.com','E-mail')]:
        parts.append(f'<a href="{url}">'+picture(name,alt,'33.33%')+'</a>')
    parts.append('</p>\n');(ROOT/'README.md').write_text(''.join(parts),encoding='utf-8')
    (OUT/'README.md').write_text('# Artes do perfil\n\nApresentação compacta em preto e cobre: introdução, sobre mim, tecnologias, dois projetos lado a lado e contatos. Versões próprias para computador e celular. Texto estático, movimento apenas nas órbitas.\n\nRegenerar: `python3 scripts/build_profile.py` (Pillow).\n',encoding='utf-8')
    for p in OUT.glob('profile-*.svg'):p.unlink()
    print('Generated compact desktop and mobile layouts.')


if __name__=='__main__':main()
