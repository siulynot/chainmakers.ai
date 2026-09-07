from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.anchors=[];self.ids=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='h1':self.h1+=1
  if attrs.get('id'):self.ids.append(attrs['id'])
  for key in ('href','src'):
   value=attrs.get(key,'')
   if value.startswith('#'):
    if len(value)>1:self.anchors.append(value[1:])
   elif value and not urlsplit(value).scheme:self.links.append(unquote(urlsplit(value).path))
p=Parser();source=(ROOT/'index.html').read_text();p.feed(source)
assert p.h1==1 and len(p.ids)==len(set(p.ids))
for anchor in p.anchors:assert anchor in p.ids,anchor
for link in p.links:assert (ROOT/link).is_file(),link
for phrase in ['Products built by Chainmakers','ChainAccounts','MedReq','PermitVault','The Chainmakers Method','Bring us a','workflow-form']:assert phrase in source
for phrase in ['BRAND PORTFOLIO','Download brand kit','chainmakers logo gallery']:assert phrase not in source
assert (ROOT/'brand-portfolio.html').is_file()
manifest=json.loads((ROOT/'site.webmanifest').read_text());assert manifest['scope']=='./'
for item in manifest['icons']:assert (ROOT/item['src']).is_file()
with zipfile.ZipFile(ROOT/'downloads/Chainmakers-ai-Brand-Kit-v1.zip') as z:assert z.testzip() is None
print(f'PASS: {len(p.links)} local assets, {len(p.anchors)} anchors, one h1, service content and brand ZIP')
