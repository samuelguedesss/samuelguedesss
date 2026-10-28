"""Build a continuous, responsive GitHub profile; Python 3 + Pillow.

Text stays visible and static. Only decorative orbit marks move, with
prefers-reduced-motion support. Each seamless slice remains a real link.
"""
from pathlib import Path
from html import escape
from PIL import ImageFont
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
BG, FG, COPPER, MUTED, RULE = '#090b0e', '#f2eee9', '#dfa16d', '#b8b1a9', '#3d3027'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
if not Path(FONT).exists():
    FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def t(x,y,label,size=24,color=FG,bold=False,mono=False):
    face='Menlo, Consolas, monospace' if mono else 'Arial, Helvetica, sans-serif'
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{600 if bold else 400}" font-family="{face}">{escape(label)}</text>'


def paragraph(label,x,y,width,size=24,leading=35,color=MUTED):
    f=ImageFont.truetype(FONT,size)
    words=label.split(); lines=[]; line=''
    for word in words:
        trial=(line+' '+word).strip()
        if f.getlength(trial)>width and line:
            lines.append(line);line=word
        else:
            line=trial
    if line:lines.append(line)
    return ''.join(t(x,y+i*leading,line,size,color) for i,line in enumerate(lines)),y+len(lines)*leading


def rule(w):
    return f'<path d="M44 1H{w-44}" stroke="{RULE}"/>'


def svg(w,h,content,title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><style>text{{text-rendering:optimizeLegibility}}.orbit{{transform-box:fill-box;transform-origin:center;animation:turn 24s linear infinite}}@keyframes turn{{to{{transform:rotate(360deg)}}}}@media(prefers-reduced-motion:reduce){{.orbit{{animation:none}}}}</style>
<rect width="{w}" height="{h}" fill="{BG}"/>{content}</svg>'''


def save(name,w,h,c,title,mobile):
    (OUT/f'{name}{"-mobile" if mobile else ""}.svg').write_text(svg(w,h,c,title),encoding='utf-8')


def intro(mobile):
    w=600 if mobile else 1000
    body=27 if mobile else 25
    c=t(44,49,'[ sg. ]',27,COPPER,mono=True)
    c+=t(w-228,46,'Software engineer',16,MUTED)
    c+=f'<path d="M44 78H{w-44}" stroke="{RULE}"/>'
    name=72 if mobile else 84
    c+=t(44,182,'Samuel',name,bold=True)+t(44,266,'Guedes.',name,COPPER,True)
    # The orbit never contains, clips or moves any lettering.
    cx,cy,r=(475,201,62) if mobile else (783,222,136)
    for radius in [r,r*.73,r*.48]:
        c+=f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{RULE}"/>'
    c+=f'<g class="orbit"><circle cx="{cx}" cy="{cy-r}" r="4" fill="{COPPER}"/><circle cx="{cx}" cy="{cy+r}" r="4" fill="{COPPER}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="none"/></g>'
    c+=t(cx-28,cy+12,'{ }',36,COPPER,mono=True)
    c+=t(44,332,'Por trás da interface.',36 if mobile else 39,FG,True)
    c+=t(44,377,'APIs, dados e regras de negócio.',body,MUTED)
    c+=t(44,432,'Full stack com foco em back-end',21 if mobile else 22,COPPER)
    c+=f'<path d="M44 476H{w-44}" stroke="{RULE}"/>'
    c+=t(44,531,'Sobre mim',32,FG,True)
    p,y=paragraph('Conecto interfaces a regras de negócio: quem pode acessar, como uma aprovação avança e como os dados chegam à pessoa certa.',44,580,w-88,body,38)
    c+=p
    p,y=paragraph('Estudo Análise e Desenvolvimento de Sistemas na Impacta e tenho formação técnica em Informática pela ETEC.',44,y+24,w-88,body,38)
    c+=p
    save('profile-intro',w,y+58,c,'Samuel Guedes. Desenvolvedor full stack com foco em back-end. Sobre mim e formação.',mobile)


def project(mobile,helpdesk=False):
    w=600 if mobile else 1000
    c=rule(w)
    c+=t(44,53,'Sistema de chamados' if helpdesk else 'Sistema de aprovação de compras',22,COPPER)
    title=['Help Desk Ticket','System'] if helpdesk else ['Purchase Approval','System']
    c+=t(44,114,title[0],42,FG,True)+t(44,164,title[1],42,FG,True)
    body=27 if mobile else 25
    desc=('Chamados com acesso por perfil, aprovação financeira e chat integrado com polling HTTP.' if helpdesk else 'Aprovações em até três etapas, com fluxo condicional por valor e isolamento por departamento.')
    p,y=paragraph(desc,44,216,w-88,body,38)
    c+=p
    tags=['React · Node.js · Express','JWT · MySQL'] if helpdesk else ['React · Node.js · Express','Sequelize · MySQL']
    if mobile:
        for i,s in enumerate(tags):c+=t(44,y+27+i*34,s,23,COPPER)
        y+=72
    else:
        c+=t(44,y+29,' · '.join(tags),22,COPPER);y+=42
    c+=t(44,y+42,'Abrir repositório e documentação',24,FG)
    c+=f'<path d="M{w-86} {y+26}l14 14-14 14" fill="none" stroke="{COPPER}" stroke-width="2"/>'
    save('profile-helpdesk' if helpdesk else 'profile-purchase',w,y+86,c,('Help Desk Ticket System — chamados, chat e permissões.' if helpdesk else 'Purchase Approval System — fluxo de aprovação e regras de negócio.')+' Clique para abrir o repositório.',mobile)


def stack(mobile):
    w=600 if mobile else 1000
    c=rule(w)+t(44,61,'Tecnologias que conectam tudo',31 if mobile else 34,FG,True)
    y=120
    rows=[('Back-end','Node.js · Express · JavaScript · Java'),('Dados','MySQL · SQL · Sequelize'),('Interface','React · Material UI · HTML · CSS'),('Fundamentos','Git · APIs REST · JWT · RBAC')]
    for label,value in rows:
        if mobile:
            c+=t(44,y,label,26,COPPER)
            p,ny=paragraph(value,44,y+39,w-88,25,34,FG);c+=p;y=ny+34
        else:
            c+=t(44,y,label,24,COPPER)+t(270,y,value,24,FG);y+=55
    c+=f'<path d="M44 {y+4}H{w-44}" stroke="{RULE}"/>'
    c+=t(44,y+65,'Vamos conectar ideias a sistemas.',29 if mobile else 34,FG,True)
    c+=t(44,y+106,'Projetos, trajetória e contato no meu portfólio.',22 if mobile else 24,MUTED)
    save('profile-stack',w,y+150,c,'Stack: Node.js, Express, JavaScript, Java, MySQL, SQL, Sequelize, React, Material UI, HTML, CSS, Git, APIs REST, JWT e RBAC. Conheça meu portfólio.',mobile)


def contact(label,filename):
    # Three linked slices form a single footer, including on phones.
    c=f'<rect x="0" y="0" width="333" height="140" fill="#17130f"/>'
    c+=t(36,82,label,36,COPPER)
    c+='<path d="M282 66l10 10-10 10" fill="none" stroke="#dfa16d" stroke-width="2"/>'
    (OUT/f'{filename}.svg').write_text(svg(333,140,c,label),encoding='utf-8')


def main():
    for mobile in [False,True]:
        intro(mobile);project(mobile);project(mobile,True);stack(mobile)
    for label,name in [('Portfólio','link-portfolio'),('LinkedIn','link-linkedin'),('E-mail','link-email')]:contact(label,name)
    alt={
        'profile-intro':'Samuel Guedes. Desenvolvedor full stack com foco em back-end, APIs REST e bancos de dados. Estudo ADS na Impacta e tenho formação técnica em Informática pela ETEC.',
        'profile-purchase':'Purchase Approval System. Aprovações em até três etapas, fluxo condicional por valor e isolamento por departamento. React, Node.js, Express, Sequelize e MySQL. Abrir repositório.',
        'profile-helpdesk':'Help Desk Ticket System. Chamados com controle de acesso por perfil, aprovação financeira e chat com polling HTTP. React, Node.js, Express, JWT e MySQL. Abrir repositório.',
        'profile-stack':'Back-end: Node.js, Express, JavaScript e Java. Dados: MySQL, SQL e Sequelize. Interface: React, Material UI, HTML e CSS. Fundamentos: Git, APIs REST, JWT e RBAC. Conheça meu portfólio.'}
    portfolio='https://portifolio-samuel-svm7.vercel.app/'
    links=[('profile-intro',portfolio),('profile-purchase','https://github.com/samuelguedesss/purchase-approval-system'),('profile-helpdesk','https://github.com/samuelguedesss/helpdesk-ticket-system'),('profile-stack',portfolio)]
    parts=['<!-- Original, continuous artwork. Regenerate: python3 scripts/build_profile.py -->\n<p align="center">']
    for name,url in links:
        parts.append(f'<a href="{url}"><picture><source media="(max-width: 600px)" srcset="./assets/{name}-mobile.svg"><img align="top" src="./assets/{name}.svg" width="100%" alt="{alt[name]}"></picture></a>')
    for label,name,url in [('Portfólio','link-portfolio',portfolio),('LinkedIn','link-linkedin','https://www.linkedin.com/in/samuel-fguedes/'),('E-mail','link-email','mailto:samuelguedes473@gmail.com')]:
        parts.append(f'<a href="{url}"><img align="top" src="./assets/{name}.svg" width="33.33%" alt="{label}"></a>')
    parts.append('</p>\n')
    # No inter-image whitespace: prevents inline baseline gaps and hard breaks.
    (ROOT/'README.md').write_text(''.join(parts),encoding='utf-8')
    (OUT/'README.md').write_text('# Artes do perfil\n\nComposição contínua em preto e cobre, com versões para celular e computador. Os links permanecem separados por seção; o texto é estático e somente os pontos orbitais se movem. A preferência por movimento reduzido é respeitada.\n\nPara regenerar: `python3 scripts/build_profile.py` (Pillow).\n',encoding='utf-8')
    # Remove only generated files from the superseded design.
    for name in ['profile-cover.gif','profile-cover.png','purchase-approval.gif','purchase-approval.svg','helpdesk.gif','helpdesk.svg','stack.svg','footer.svg']:
        p=OUT/name
        if p.exists():p.unlink()
    print('Generated desktop/mobile sections and linked footer.')


if __name__=='__main__':main()
