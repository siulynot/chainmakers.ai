from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
import zipfile
ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.anchors=[];self.ids=[];self.h1=0;self.script=False;self.schema=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1':self.h1+=1
        if attrs.get('id'):self.ids.append(attrs['id'])
        if tag=='script' and attrs.get('type')=='application/ld+json':self.script=True
        for key in ['href','src']:
            value=attrs.get(key,'')
            if value.startswith('#'):
                if len(value)>1:self.anchors.append(value[1:])
            elif value and not urlsplit(value).scheme:self.links.append(unquote(urlsplit(value).path))
    def handle_data(self,data):
        if self.script:self.schema.append(data)
    def handle_endtag(self,tag):
        if tag=='script':self.script=False
for filename in ['index.html','brand-portfolio.html']:
    source=(ROOT/filename).read_text();p=Parser();p.feed(source)
    assert p.h1==1 and len(p.ids)==len(set(p.ids)),filename
    for anchor in p.anchors:assert anchor in p.ids,(filename,anchor)
    for link in p.links:assert (ROOT/link).is_file(),(filename,link)
    if filename=='index.html':
        for section in ['servicios','soluciones','metodo','nosotros','contacto']:assert section in p.ids
        for phrase in ['Consultoría administrativa','ChainAccounts','MedReq','EN FASE DE DISEÑO','EN FASE DE PROPUESTA','mailto:chainmakerspr@gmail.com']:assert phrase in source
        for phrase in ['BRAND PORTFOLIO','Descargar brand kit','372','Lourdes','Pedro Irizarry','SOC 2 certified','HIPAA certified']:assert phrase not in source
        for item in p.schema:assert json.loads(item)['email']=='chainmakerspr@gmail.com'
    print(f'PASS: {filename}: {len(p.links)} local assets, {len(p.anchors)} anchors, one h1')
manifest=json.loads((ROOT/'site.webmanifest').read_text())
assert manifest['scope']=='./'
for icon in manifest['icons']:assert (ROOT/icon['src']).is_file()
with zipfile.ZipFile(ROOT/'downloads/Chainmakers-ai-Brand-Kit-v1.zip') as z:assert z.testzip() is None
print('PASS: service content, product stages, structured data, relative manifest and preserved brand ZIP')
