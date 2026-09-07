"""Validate static local links, all export selections, and Pages-relative icons."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.paths=[];self.ids=[];self.anchors=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        for name in ['href','src']:
            url=attrs.get(name,'')
            if url.startswith('#'):
                if len(url)>1:self.anchors.append(url[1:])
            elif url and not urlsplit(url).scheme:self.paths.append(unquote(urlsplit(url).path))
parser=Links();parser.feed((ROOT/'index.html').read_text())
assert len(parser.ids)==len(set(parser.ids)), 'Duplicate HTML IDs'
for anchor in parser.anchors:assert anchor in parser.ids,anchor
for path in parser.paths:assert (ROOT/path).is_file(),path
sizes={'horizontal':[240,320,480,640,960,1280,1920,2560,3840], 'stacked':[256,512,1024,2048,4096], 'symbol':[32,48,64,128,256,512,1024,2048], 'wordmark':[240,320,480,640,960,1280,1920,2560,3840]}
colors=['color','reverse','graphite','white','cyan','black']
count=0
for layout,widths in sizes.items():
    for color in colors:
        svg=ROOT/f'brand/svg/{layout}/chainmakers-{layout}-{color}.svg'
        ET.parse(svg);count+=1
        for width in widths:
            for ext in ['png','webp']:
                assert (ROOT/f'brand/{ext}/{layout}/chainmakers-{layout}-{color}-{width}w.{ext}').is_file()
                count+=1
manifest=json.loads((ROOT/'site.webmanifest').read_text())
assert manifest['start_url']=='./' and manifest['scope']=='./'
for icon in manifest['icons']:
    assert not icon['src'].startswith('/') and (ROOT/icon['src']).is_file()
with zipfile.ZipFile(ROOT/'downloads/Chainmakers-ai-Brand-Kit-v1.zip') as archive:
    assert archive.testzip() is None
assert not (ROOT/'CNAME').exists(), 'Domain must not be configured before DNS approval'
print(f'PASS: {len(parser.paths)} static links, {len(parser.anchors)} anchors, {count} logo downloads, relative manifest, and ZIP integrity')
