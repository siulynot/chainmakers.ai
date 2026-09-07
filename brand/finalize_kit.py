#!/usr/bin/env python3
"""Write documentation, verify deliverables, and package the brand handoff."""
from pathlib import Path
import csv
import hashlib
import json
import math
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile
import numpy as np
from PIL import Image
from build_kit import ROOT, COLORS, LAYOUTS, WIDTHS, save

save(ROOT / "README.md", """# Chainmakers.ai - Brand kit v1.0

Portfolio completo de la propuesta de logo creada el 7 de septiembre de 2026.

## Empieza aquí

- `Chainmakers-ai-Portfolio.pdf`: guía visual de 8 páginas.
- `svg/`: 24 maestros vectoriales, con letras y símbolo convertidos a trazados.
- `png/`: 186 versiones con transparencia real.
- `webp/`: 186 versiones transparentes con compresión sin pérdida.
- `web/`: favicons, ICO, Apple touch, iconos de aplicación y manifest.
- `social/`: Open Graph, avatar, cuadrado y banner; fondos claros y oscuros.
- `web-ready/brand/`: selección ligera para copiar a `public/brand/` del website.
- `integration/`: ejemplos HTML, CSS, React/TSX y guía de integración.
- `inventory.csv`: dimensiones, tamaño y checksum de cada archivo.
- `validation.json`: comprobaciones de integridad, transparencia y geometría.

## Composiciones y nombres

`horizontal`, `stacked` (vertical), `symbol` (símbolo) y `wordmark` (nombre).

Cada una incluye `color`, `reverse`, `graphite`, `white`, `cyan` y `black`.
Ejemplo: `chainmakers-horizontal-color-640w.png` tiene 640 píxeles de ancho.
La altura se calcula conservando la proporción. El SVG sirve para cualquier resolución.

| Composición | Anchos de PNG y WebP, en píxeles |
| --- | --- |
| Horizontal | 240, 320, 480, 640, 960, 1280, 1920, 2560, 3840 |
| Vertical | 256, 512, 1024, 2048, 4096 |
| Símbolo | 32, 48, 64, 128, 256, 512, 1024, 2048 |
| Nombre | 240, 320, 480, 640, 960, 1280, 1920, 2560, 3840 |

## Colores de producción

- Cian: `#0AA7ED`.
- Grafito: `#4B4F52`.
- Fondo oscuro: `#111820`.
- Blanco: `#FFFFFF`.
- Negro de una tinta: `#000000`.

Los valores de esta entrega normalizan el concepto generado a colores planos RGB/sRGB.
No son una afirmación sobre los valores de la guía histórica de Chainmakers.
El nombre del logo conserva sus formas mediante trazados; no requiere instalar una fuente.
La tipografía del website puede elegirse por separado. No se distribuyen archivos de fuentes.

## Uso

Usa `color` en fondos claros y `reverse` en fondos oscuros.
Los archivos `white` parecen vacíos sobre blanco: tienen contenido blanco transparente.
Deja alrededor un margen libre de al menos un cuarto de la altura del símbolo;
el padding del archivo no sustituye ese margen de diseño. Evita deformar o añadir efectos.
Como punto de partida, usa el horizontal desde 180 px y el símbolo desde 24 px.
Para 16 px utiliza el favicon suministrado. En pantallas de alta densidad, usa SVG
o una imagen con al menos dos veces el ancho de visualización.

Los JPG de `social/` tienen fondo sólido. Los PNG/WebP de `png/` y `webp/` son transparentes.
La transparencia fue comprobada en los archivos, no inferida de una cuadrícula visible.
Los SVG contienen trazados; no son PNG incrustados ni dependen de texto o fuentes externas.

## Origen y reproducción

`source/chainmakers-original-concept.png` conserva la propuesta mostrada en conversación.
El concepto se produjo con la herramienta integrada ImageGen. La fuente de las exportaciones
es su conversión vectorial de dos capas, normalizada a colores sólidos; no se ha usado una
fuente parecida para reescribir el nombre. El fondo del concepto no forma parte de los SVG.
Una prueba posterior de limpieza con ImageGen no produjo canal alfa real y fue descartada.
Los prompts se conservan en `source/PROMPTS.md`.

Para reconstruir los archivos: ejecutar `build_kit.py`, `build_portfolio.py` y
`finalize_kit.py`, en ese orden. Dependencias: Python 3 con Pillow, numpy y reportlab;
ImageMagick, potrace, librsvg y Poppler. El generador PDF usa Arial del sistema macOS.
La conversión vectorial conserva la silueta visual del concepto; no sustituye una revisión
de diseño previa a registrar la marca. Esta entrega se prepara para medios digitales;
una imprenta deberá aplicar su perfil de color al preparar producción física.
""")

save(ROOT / "integration/INTEGRACION.md", """# Integración en Chainmakers.ai

## Website en el dominio raíz

1. Copia `web-ready/brand/` al directorio público del website como `brand/`.
   En React/Next/Vite normalmente se usa `public/brand/`.
2. Integra los elementos de `head.html` en el head del documento, sin duplicar metadatos.
3. Usa `Logo.tsx` si el website utiliza React, o los ejemplos de `logo.html` si es HTML.
4. Añade `brand.css` o traslada sus variables a la hoja de estilos existente.
5. Elige explícitamente el tema claro u oscuro según el fondo real del componente.

Los ejemplos no son una dependencia obligatoria: un `<img>` que apunte al SVG es suficiente.
`Logo.tsx` usa React/TSX estándar y debe compilarse con las herramientas del proyecto receptor.

## GitHub Pages bajo una subruta

Los ejemplos de integración usan `/brand/` para el futuro dominio raíz Chainmakers.ai.
Si se instalan bajo `https://siulynot.github.io/chainmakers.ai/`, usa
`/chainmakers.ai/brand/` como prefijo. `Logo.tsx` acepta `assetBase` para ese caso.
Actualiza también `id`, `start_url`, `scope` y rutas de iconos en el manifest.
El portfolio publicado incluye su propio manifest con rutas relativas para GitHub Pages.

## Archivos principales

- Cabecera clara: `svg/horizontal/chainmakers-horizontal-color.svg`.
- Cabecera oscura: `svg/horizontal/chainmakers-horizontal-reverse.svg`.
- Icono: `svg/symbol/chainmakers-symbol-color.svg`.
- Favicon moderno: `web/favicon.svg`, adaptable al tema del navegador.
- Favicon compatible: `web/favicon.ico`.
- Apple: `web/apple-touch-icon.png` (180 × 180, fondo blanco).
- Aplicación: 192 y 512 px; el icono `maskable` mantiene el símbolo dentro del área central segura.
- Compartir enlaces: `social/chainmakers-opengraph-dark.png` (1200 × 630).

La URL de Open Graph debe ser absoluta y corresponder al host publicado.
El manifest aporta identidad e iconos; por sí solo no proporciona funcionamiento sin conexión.
El prefijo de assets y el host se deben configurar en el proyecto donde se integren.
""")

save(ROOT / "integration/head.html", """<!-- Para Chainmakers.ai en la raíz del dominio. Ajusta el prefijo si usas una subruta. -->
<link rel="icon" href="/brand/web/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/brand/web/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/brand/web/apple-touch-icon.png">
<link rel="mask-icon" href="/brand/web/safari-pinned-tab.svg" color="#0AA7ED">
<link rel="manifest" href="/brand/web/site.webmanifest">
<meta name="theme-color" content="#111820">
<meta property="og:title" content="Chainmakers">
<meta property="og:type" content="website">
<meta property="og:url" content="https://chainmakers.ai/">
<meta property="og:image" content="https://chainmakers.ai/brand/social/chainmakers-opengraph-dark.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo de Chainmakers en blanco y cian sobre fondo oscuro">
<meta name="twitter:card" content="summary_large_image">
""")
save(ROOT / "integration/logo.html", """<!-- Variante para fondo claro -->
<a href="/" aria-label="Chainmakers, inicio">
  <img class="chainmakers-logo" src="/brand/svg/horizontal/chainmakers-horizontal-color.svg"
       alt="Chainmakers" width="1720" height="450">
</a>
<!-- Para fondo oscuro, cambia color.svg por reverse.svg. -->
""")
save(ROOT / "integration/brand.css", """:root {
  --chainmakers-cyan: #0AA7ED;
  --chainmakers-graphite: #4B4F52;
  --chainmakers-dark: #111820;
  --chainmakers-white: #FFFFFF;
}
.chainmakers-logo { display: block; width: 240px; max-width: 100%; height: auto; }
@media (max-width: 600px) { .chainmakers-logo { width: 180px; } }
""")
save(ROOT / "integration/Logo.tsx", """type LogoProps = {
  theme?: 'light' | 'dark';
  variant?: 'horizontal' | 'stacked' | 'symbol' | 'wordmark';
  assetBase?: string;
  className?: string;
  width?: number;
};
const dimensions = {
  horizontal: [1720, 450], stacked: [1280, 860],
  symbol: [512, 512], wordmark: [1220, 245],
} as const;

export function ChainmakersLogo({ theme = 'light', variant = 'horizontal',
  assetBase = '/brand', className, width = 240 }: LogoProps) {
  const color = theme === 'dark' ? 'reverse' : 'color';
  const [w, h] = dimensions[variant];
  return <img
    src={`${assetBase.replace(/\\/$/, '')}/svg/${variant}/chainmakers-${variant}-${color}.svg`}
    alt="Chainmakers" width={width} height={width * h / w}
    className={className} style={{ display: 'block', maxWidth: '100%', height: 'auto' }}
  />;
}
""")

save(ROOT / "source/PROMPTS.md", """# Origen de la imagen

Modo utilizado: herramienta integrada ImageGen; no se utilizó el CLI/API de fallback.

## Concepto original

Use case: logo-brand. Create one polished new logo concept for Chainmakers, a business
consulting and software company. The supplied existing logo is a brand reference, not an
exact edit target. Evolve its cyan and gray palette and geometric C/M connection idea into
a simpler, elegant, memorable interlocking monogram, with clean negative space and
consistent geometric stroke widths. Pair the icon with exact wordmark text 'Chainmakers'
in refined medium-weight contemporary sans serif, carefully kerned, readable. Horizontal
centered lockup, icon left, wordmark right, ample white background margin. Dark graphite
gray and the original cyan blue, flat solid fills. The mark should feel precise,
established and practical. Vector-like crisp edges, no gradients, no shadows, no 3D,
no mockup, no slogan, no extra text, no presentation board. Deliver a single high
resolution logo on white.

## Prueba de limpieza posterior, descartada como maestro

Use case: precise-object-edit / logo-brand. Prepare the attached Chainmakers logo as a
clean production master. Edit target is the supplied image. Preserve the exact CM
interlocking monogram silhouette, exact relative proportions of symbol and wordmark,
and exact 'Chainmakers' lettering shapes and spacing. Remove ALL paper/background
texture, all subtle shading and gradients, and all background pixels. Render only the
logo on genuinely transparent background with clean antialiased edges. Exactly two
perfectly uniform solid colors: graphite #4B4F52 for the C symbol and 'Chain', cyan
#0AA7ED for the M symbol and 'makers'. Preserve clear transparent negative spaces and
gaps between the two symbol shapes. Keep original horizontal composition with modest
safe transparent margin. No added text, no slogan, no extra shapes, no mockup, no
perspective, no shadows. Highest useful resolution, wide horizontal canvas. This is
an exact cleanup of the provided logo, not a redesign.

La prueba no produjo alfa real; no forma parte de los assets entregados. Se convirtió
el concepto original a trazados con potrace. Las versiones finales y los formatos ráster
se exportan desde los mismos SVG para mantener colores, forma y proporciones consistentes.
""")

# Lightweight subset for the website, independent of the large-resolution library.
for layout in LAYOUTS:
    for cw in ["color", "reverse"]:
        rel = Path(f"svg/{layout}/chainmakers-{layout}-{cw}.svg")
        dst = ROOT / "web-ready/brand" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
for folder in ["web", "social"]:
    for src in (ROOT / folder).iterdir():
        if folder == "social" and ("opengraph" not in src.name or "@2x" in src.name or src.suffix != ".png"):
            continue
        dst = ROOT / "web-ready/brand" / folder / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src,dst)

# Verification reads image data only; creation/export is handled by the SVG pipeline.
checks = []
vectors = sorted((ROOT / "svg").rglob("*.svg"))
assert len(vectors) == 24
for path in vectors:
    tree = ET.parse(path).getroot()
    tags = {node.tag.split("}")[-1] for node in tree.iter()}
    assert "path" in tags and not tags.intersection({"image","text","script","foreignObject"}), path
checks.append("24 SVG maestros con trazados; sin bitmap incrustado, texto o fuentes externas")

for layout in LAYOUTS:
    w,h,_ = LAYOUTS[layout]
    for cw in COLORS:
        for width in WIDTHS[layout]:
            for ext in ["png","webp"]:
                path = ROOT / ext / layout / f"chainmakers-{layout}-{cw}-{width}w.{ext}"
                with Image.open(path) as im:
                    assert im.width == width and abs(im.height-width*h/w) <= 1, path
                    assert "A" in im.getbands(), path
                    alpha = im.getchannel("A")
                    assert alpha.getextrema() == (0,255), path
                    assert im.getpixel((0,0))[-1] == 0, path
                    assert alpha.getbbox() is not None, path
                    bbox = alpha.getbbox()
                    assert bbox[0] > 0 and bbox[1] > 0 and bbox[2] < im.width and bbox[3] < im.height, path
checks.append("186 PNG y 186 WebP: dimensiones correctas, alfa real, contenido y márgenes sin recorte")

for size in [192,512]:
    with Image.open(ROOT / f"web/maskable-icon-{size}.png") as im:
        arr = np.array(im.convert("RGB"))
        mask = np.max(np.abs(arr.astype(int)-np.array([17,24,32])),axis=2)>5
        y,x=np.where(mask)
        radius=np.sqrt((x-(size-1)/2)**2+(y-(size-1)/2)**2).max()
        assert radius <= .4*size, (size,radius)
checks.append("Símbolo de iconos maskable dentro del círculo central de radio 40%")
with Image.open(ROOT / "web/favicon.ico") as im:
    assert im.ico.sizes() == {(16,16),(32,32),(48,48),(64,64),(256,256)}
checks.append("ICO válido con 16, 32, 48, 64 y 256 px")
manifest=json.loads((ROOT / "web/site.webmanifest").read_text())
for item in manifest["icons"]:
    assert (ROOT / item["src"].removeprefix("/brand/")).is_file()
checks.append("Todas las rutas de iconos del manifest resuelven en la selección web-ready")
checks.append("PDF de 8 páginas renderizado e inspeccionado visualmente")
save(ROOT / "validation.json", json.dumps({"status":"passed","date":"2026-09-07","checks":checks},ensure_ascii=False,indent=2)+"\n")

files = [p for p in ROOT.rglob("*") if p.is_file() and not {"_work","__pycache__"}.intersection(p.relative_to(ROOT).parts)
         and p.name not in {"inventory.csv","SHA256SUMS.txt"} and p.suffix != ".zip"]
rows=[]
for p in sorted(files):
    dims=""
    if p.suffix.lower() in {".png",".webp",".jpg",".ico"}:
        with Image.open(p) as im:
            dims=f"{im.width}x{im.height}"
    elif p.suffix==".svg":
        dims=ET.parse(p).getroot().attrib.get("viewBox","")
    rows.append([str(p.relative_to(ROOT)),p.suffix.lstrip("."),dims,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
with (ROOT / "inventory.csv").open("w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f)
    writer.writerow(["file","format","dimensions_or_viewBox","bytes","sha256"])
    writer.writerows(rows)
save(ROOT / "SHA256SUMS.txt", "\n".join(f"{r[4]}  {r[0]}" for r in rows)+"\n")
archive = ROOT.parent / "Chainmakers-ai-Brand-Kit-v1.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files+[ROOT/"inventory.csv",ROOT/"SHA256SUMS.txt"]):
        z.write(p,Path("Chainmakers-ai-Brand-Kit-v1")/p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
print(json.dumps({"files":len(files)+2,"zip":str(archive),"zip_mb":round(archive.stat().st_size/1024**2,2),"checks":checks},ensure_ascii=False))
