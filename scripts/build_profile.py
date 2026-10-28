"""Generate Samuel's copper profile, inspired by eduardo-toste's layout.

Artwork is generated locally from Samuel's public avatar and real public
GitHub contribution data. Run with --refresh to update source data.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
import json,re,sys,urllib.request
from PIL import Image,ImageOps,ImageFilter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';DATA=ROOT/'data'
BG,FG,ACCENT,MUTED,LINE='#0d1015','#d9d2c9','#dda16c','#91887e','#443429'
USER='samuelguedesss'


def get(url):
    request=urllib.request.Request(url,headers={'User-Agent':'samuel-profile-artwork'})
    return urllib.request.urlopen(request,timeout=30).read()


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__();self.days={};self.tip=None;self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and 'data-date' in a:
            self.days[a['id']]={'date':a['data-date'],'level':int(a['data-level'])}
        if tag=='tool-tip':self.tip=a.get('for');self.text=[]
    def handle_data(self,data):
        if self.tip:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=='tool-tip' and self.tip:
            if self.tip in self.days:
                value=''.join(self.text).strip();m=re.match(r'([\d,]+) contribution',value)
                if value.startswith('No contributions'):count=0
                elif m:count=int(m.group(1).replace(',',''))
                else:raise ValueError('Unrecognized contribution tooltip: '+value)
                self.days[self.tip]['count']=count
            self.tip=None


def refresh():
    DATA.mkdir(exist_ok=True)
    avatar=DATA/'avatar-source.png'
    if not avatar.exists():
        user=json.loads(get(f'https://api.github.com/users/{USER}'))
        avatar.write_bytes(get(user['avatar_url']))
    parser=CalendarParser();parser.feed(get(f'https://github.com/users/{USER}/contributions').decode())
    today=datetime.now(ZoneInfo('America/Sao_Paulo')).date();start=today-timedelta(days=364)
    days=sorted([v for v in parser.days.values() if start.isoformat()<=v['date']<=today.isoformat()],key=lambda d:d['date'])
    if len(days)!=365 or any('count' not in d for d in days):raise ValueError('Incomplete contribution calendar; keep previous artwork')
    (DATA/'contributions.json').write_text(json.dumps({'source':f'https://github.com/users/{USER}/contributions','updated':today.isoformat(),'days':days},indent=2)+'\n')


def txt(x,y,s,size=17,color=FG,bold=False,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{600 if bold else 400}" {extra}>{escape(s)}</text>'


def shell(w,h,c,title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}" font-family="Menlo, Consolas, monospace"><title>{escape(title)}</title><defs><linearGradient id="surface" x2="0" y2="1"><stop stop-color="#17181b"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs><style>@media(prefers-reduced-motion:reduce){{.scan{{clip-path:none}}.motion{{display:none}}}}</style><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#surface)" stroke="{LINE}"/>{c}</svg>'''


def bar(w,label,height=30,font=13):
    c=f'<path d="M1 {height}H{w-1}" stroke="{LINE}"/>'
    for x,col in [(20,ACCENT),(36,'#a37650'),(52,'#66513f')]:c+=f'<circle cx="{x}" cy="{height/2}" r="5" fill="{col}"/>'
    return c+txt(w/2,height*.64,label,font,MUTED,extra='text-anchor="middle"')


def save(name,w,h,c,title):
    (OUT/name).write_text(shell(w,h,c,title),encoding='utf-8')


def portrait():
    photo=Image.open(DATA/'avatar-source.png').convert('RGB')
    gray=ImageOps.autocontrast(photo.convert('L'))
    detail=gray.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(.35))
    small=gray.resize((92,66));edges=detail.resize((92,66));rgb=photo.resize((92,66))
    chars=' .,:;irsXA253hMHGS#9B&@';rows=[]
    for y in range(66):
        row=''
        for x in range(92):
            r,g,b=rgb.getpixel((x,y));l=small.getpixel((x,y));edge=edges.getpixel((x,y))
            # Remove pale wall; preserve the original portrait's silhouette.
            left,right=(25,51) if y<16 else ((21,69) if y<27 else (9,76))
            background=(max(r,g,b)-min(r,g,b)<26 and l>150) or y<8 or not left<=x<=right
            value=0 if background else min(1,(l/255)*.58+(edge/255)*1.6)
            row+=chars[round(value*(len(chars)-1))]
        rows.append(row.rstrip())
    c=bar(840,f'{USER}@github: ~/portrait.sh',46,19)
    c+='<defs><clipPath id="scan"><rect x="20" y="65" width="800" height="740"><animate class="motion" attributeName="height" from="0" to="740" dur="1.4s" fill="freeze"/></rect></clipPath></defs><g class="scan" clip-path="url(#scan)">'
    for i,s in enumerate(rows):c+=txt(34,81+i*10.7,s,13,ACCENT,extra='xml:space="preserve"')
    c+='</g><path d="M1 858H839" stroke="'+LINE+'"/>'
    c+=txt(22,885,'samuel@github:~$ whoami',18,MUTED)+txt(300,885,'Samuel Guedes',18,FG)
    c+=f'<rect x="455" y="870" width="9" height="18" fill="{ACCENT}"><animate class="motion" attributeName="opacity" values="1;1;.2;.2" keyTimes="0;.49;.5;1" dur="1.2s" repeatCount="indefinite"/></rect>'
    save('avi-ascii.svg',840,907,c,'Retrato ASCII de Samuel Guedes, gerado a partir do seu avatar público.')


def info():
    c=bar(620,f'{USER}@github: ~$ fastfetch',30,12)
    lines=[(58,26,'samuel@github',17,ACCENT,True),(80,26,'------------------------',15,MUTED,False)]
    fields=[(107,'Role','Full stack developer'),(132,'Focus','Back-end / APIs REST'),(157,'Edu','ADS - Impacta'),(182,'Tech','Informática - ETEC')]
    for y,k,v in fields:
        lines.extend([(y,26,k,17,ACCENT,True),(y,118,v,17,FG,False)])
    lines.append((222,26,'~ Stack',17,ACCENT,True))
    for y,k,v in [(248,'Lang','JavaScript / Java / SQL'),(274,'Back','Node.js / Express'),(300,'Data','MySQL / Sequelize'),(326,'Front','React / Material UI')]:
        lines.extend([(y,26,k,17,ACCENT,True),(y,118,v,17,FG,False)])
    lines.append((362,26,'~ Highlights',17,ACCENT,True))
    for y,s in [(389,'JWT e controle de acesso (RBAC)'),(416,'Fluxos de aprovação condicionais'),(443,'Chat e gestão de chamados')]:lines.append((y,26,'+ '+s,17,FG,False))
    for index,(y,x,s,size,color,bold) in enumerate(lines):
        c+='<g>'+txt(x,y,s,size,color,bold)+f'<animate class="motion" attributeName="opacity" from=".35" to="1" begin="{index*.035:.3f}s" dur=".3s" fill="freeze"/></g>'
    c+=f'<path d="M1 476H619" stroke="{LINE}"/>'+txt(20,496,'samuel@github:~$ fastfetch',14,MUTED)
    save('info-card.svg',620,506,c,'Informações de Samuel Guedes: full stack, foco em back-end, formação, tecnologias e projetos.')
    mobile=c.replace('font-size="17"','font-size="21"').replace('font-size="15"','font-size="18"')
    save('info-card-mobile.svg',620,506,mobile,'Informações de Samuel Guedes em versão para celular.')


def contributions():
    payload=json.loads((DATA/'contributions.json').read_text());days=payload['days']
    first=datetime.fromisoformat(days[0]['date']).date();first_sunday=first-timedelta(days=(first.weekday()+1)%7)
    w,h=869,265;c=bar(w,'samuel@github: ~/contributions --graph',30,12)
    colors=['#1a1b1e','#4a3020','#795033','#b87947','#e3ab76']
    last_month=None;months=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
    for d in days:
        day=datetime.fromisoformat(d['date']).date();week=(day-first_sunday).days//7;weekday=(day.weekday()+1)%7
        x,y=58+week*15,56+weekday*15
        if day.month!=last_month:
            c+=txt(x-3,44,months[day.month-1],10,MUTED);last_month=day.month
        title=f"{d['date']}: {d['count']} contribuições"
        c+=f'<rect x="{x-6}" y="{y-6}" width="12" height="12" rx="2.5" fill="{colors[d["level"]]}"><title>{escape(title)}</title><animate class="motion" attributeName="opacity" from=".3" to="1" begin="{week*.018:.3f}s" dur=".25s" fill="freeze"/></rect>'
    for y,label in [(74,'Seg'),(104,'Qua'),(134,'Sex')]:c+=txt(20,y,label,9,MUTED)
    total=sum(d['count'] for d in days)
    c+=txt(26,194,f'{total} contribuições nos últimos 365 dias',18,FG,True)
    c+=txt(26,222,'Atividade real do GitHub / atualizado em '+payload['updated'],12,MUTED)
    c+=txt(638,220,'menos',10,MUTED)
    for i,color in enumerate(colors):c+=f'<rect x="{677+i*17}" y="209" width="12" height="12" rx="2" fill="{color}"/>'
    c+=txt(767,220,'mais',10,MUTED)
    save('contrib-heatmap.svg',w,h,c,f'{total} contribuições de Samuel Guedes nos últimos 365 dias. Atualizado em {payload["updated"]}.')
    print('Actual public contributions:',total)


def main():
    OUT.mkdir(exist_ok=True)
    if '--refresh' in sys.argv or not (DATA/'contributions.json').exists():refresh()
    portrait();info();contributions()
    for p in OUT.glob('terminal-*.svg'):p.unlink()
    # Raw server-rendered source is not part of the repository.
    p=DATA/'contributions-source.html'
    if p.exists():p.unlink()
    (OUT/'README.md').write_text('# Artes do perfil\n\nLayout inspirado no perfil de [eduardo-toste](https://github.com/eduardo-toste), com arte e gerador próprios, os dados de Samuel Guedes e paleta preta/cobre do portfólio.\n\n- `avi-ascii.svg`: retrato a partir do avatar público de Samuel.\n- `info-card.svg`: informações em estilo fastfetch.\n- `contrib-heatmap.svg`: contribuições reais em tons de cobre.\n\nGerar: `python3 scripts/build_profile.py`. Atualizar dados públicos: acrescentar `--refresh`.\n',encoding='utf-8')


if __name__=='__main__':main()
