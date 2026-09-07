#!/usr/bin/env python3
"""Build the visual handoff PDF from the delivered assets."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
W, H = 1200, 800
INK, BLUE, PAPER, MUTED, LINE, DARK = "#202A33", "#0AA7ED", "#F4F7F9", "#65737F", "#DEE5E9", "#111820"
FONT = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("BrandText", str(FONT / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("BrandBold", str(FONT / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("BrandItalic", str(FONT / "Arial Italic.ttf")))
C = canvas.Canvas(str(ROOT / "Chainmakers-ai-Portfolio.pdf"), pagesize=(W, H))
C.setTitle("Chainmakers.ai | Portfolio y guía de marca")
C.setAuthor("Chainmakers")
C.setSubject("Logos, variantes, exportaciones web y guía de aplicación")


def rect(x, y, w, h, fill, stroke=None, radius=0):
    C.setFillColor(HexColor(fill))
    if stroke:
        C.setStrokeColor(HexColor(stroke))
    if radius:
        C.roundRect(x, y, w, h, radius, fill=1, stroke=bool(stroke))
    else:
        C.rect(x, y, w, h, fill=1, stroke=bool(stroke))


def text(x, y, value, size=16, color=INK, bold=False):
    C.setFillColor(HexColor(color))
    C.setFont("BrandBold" if bold else "BrandText", size)
    C.drawString(x, y, value)


def lines(x, y, values, size=16, color=MUTED, gap=24, bold=False):
    for i, value in enumerate(values):
        text(x, y - i * gap, value, size, color, bold)


def image(path, x, y, w, h):
    C.drawImage(str(path), x, y, width=w, height=h, preserveAspectRatio=True, anchor="c", mask="auto")


def logo(layout, cw, x, y, w, h):
    sizes = {"horizontal": 1920, "stacked": 2048, "symbol": 1024, "wordmark": 1920}
    image(ROOT / f"png/{layout}/chainmakers-{layout}-{cw}-{sizes[layout]}w.png", x, y, w, h)


def page(title, number, subtitle="", dark=False):
    bg = DARK if dark else "#FFFFFF"
    fg = "#FFFFFF" if dark else INK
    rect(0, 0, W, H, bg)
    text(64, 750, "CHAINMAKERS.AI", 12, BLUE, True)
    text(850, 750, "PORTFOLIO DE MARCA  /  V1.0", 11, MUTED if not dark else "#A9B4BE")
    text(64, 681, title, 40, fg, True)
    if subtitle:
        text(64, 643, subtitle, 17, MUTED if not dark else "#A9B4BE")
    C.setStrokeColor(HexColor(LINE if not dark else "#2C3843"))
    C.line(64, 53, 1136, 53)
    text(64, 30, "Chainmakers  /  Archivos para diseño y desarrollo web", 10, MUTED)
    text(1050, 30, f"2026   /   {number:02d}", 10, MUTED)


def finish():
    C.showPage()


def cover():
    rect(0, 0, W, H, DARK)
    text(64, 746, "CHAINMAKERS.AI", 13, BLUE, True)
    text(861, 746, "IDENTIDAD VISUAL  /  V1.0", 12, "#A9B4BE")
    rect(64, 674, 52, 5, BLUE)
    logo("horizontal", "reverse", 100, 320, 1000, 270)
    text(68, 205, "Portfolio de marca", 46, "#FFFFFF", True)
    text(70, 160, "Un sistema de archivos listo para construir Chainmakers.ai.", 21, "#A9B4BE")
    text(70, 78, "04 COMPOSICIONES", 11, "#FFFFFF", True)
    text(290, 78, "06 VARIANTES DE COLOR", 11, "#FFFFFF", True)
    text(563, 78, "SVG + PNG + WEBP", 11, "#FFFFFF", True)
    text(970, 78, "07 / 09 / 2026", 11, BLUE, True)
    finish()


def family():
    page("La familia del logo", 2, "Una misma identidad en cuatro composiciones complementarias.")
    cards = [
        (64, 350, "horizontal", "01  Horizontal", "Cabecera del website, documentos y firmas."),
        (616, 350, "wordmark", "02  Nombre", "Espacios estrechos y aplicaciones secundarias."),
        (64, 80, "stacked", "03  Vertical", "Portadas, piezas cuadradas y presentaciones."),
        (616, 80, "symbol", "04  Símbolo", "Favicon, avatar e icono de aplicación."),
    ]
    for x, y, layout, label, desc in cards:
        rect(x, y, 520, 248, PAPER, radius=12)
        text(x + 24, y + 214, label, 15, INK, True)
        logo(layout, "color", x + 28, y + 52, 464, 145)
        text(x + 24, y + 22, desc, 12, MUTED)
    finish()


def variants():
    page("Versiones de color", 3, "Elige la variante según el fondo y el tipo de aplicación.")
    data = [
        ("color", "Principal", "Grafito + cian sobre fondo claro", "#FFFFFF"),
        ("reverse", "Inversa", "Blanco + cian sobre fondo oscuro", DARK),
        ("graphite", "Grafito", "Una tinta de la paleta", PAPER),
        ("white", "Blanco", "Una tinta sobre fondo oscuro", DARK),
        ("cyan", "Cian", "Aplicaciones de acento", DARK),
        ("black", "Negro", "Una tinta negra", "#FFFFFF"),
    ]
    for i, (cw, label, desc, bg) in enumerate(data):
        x, y = 64 + (i % 3) * 365, 345 - (i // 3) * 263
        rect(x, y, 342, 240, bg, LINE if bg != DARK else None, 10)
        fg = "#FFFFFF" if bg == DARK else INK
        text(x + 22, y + 204, label, 17, fg, True)
        logo("horizontal", cw, x + 18, y + 81, 306, 85)
        text(x + 22, y + 30, desc, 12, "#A9B4BE" if bg == DARK else MUTED)
    finish()


def applications():
    page("Aplicaciones para el website", 4, "Ejemplos visuales de cabecera, enlace compartido y avatar.")
    for y, bg, cw in [(493,"#FFFFFF","color"), (380,DARK,"reverse")]:
        rect(64,y,1072,92,bg,LINE if cw == "color" else None,10)
        logo("horizontal",cw,86,y+14,255,64)
        fg = INK if cw == "color" else "#D8E0E6"
        for x, title in [(612,"Servicios"),(732,"Productos"),(863,"Contacto")]:
            text(x,y+40,title,14,fg)
        rect(971,y+25,141,43,BLUE,radius=7)
        text(1002,y+40,"Hablemos",14,DARK,True)
    text(64,337,"ENLACES COMPARTIDOS",11,MUTED,True)
    image(ROOT / "social/chainmakers-opengraph-dark.png",64,76,480,252)
    text(614,337,"AVATAR / ICONO",11,MUTED,True)
    image(ROOT / "social/chainmakers-avatar-light.png",614,99,230,230)
    image(ROOT / "web/maskable-icon-512.png",892,137,154,154)
    text(887,108,"Icono adaptable",12,MUTED)
    finish()


def sizes():
    page("Resoluciones y formatos", 5, "Los SVG escalan sin límite de resolución. Los ráster salen de esos mismos trazados.")
    xcols = [82, 278, 992]
    rect(64,540,1072,46,DARK,radius=6)
    for x,v in zip(xcols,["COMPOSICIÓN","ANCHOS INCLUIDOS EN PNG Y WEBP","VARIANTES"]):
        text(x,558,v,12,"#FFFFFF",True)
    rows = [
        ("Horizontal", "240 / 320 / 480 / 640 / 960 / 1280 / 1920 / 2560 / 3840 px", "6 colores"),
        ("Vertical", "256 / 512 / 1024 / 2048 / 4096 px", "6 colores"),
        ("Símbolo", "32 / 48 / 64 / 128 / 256 / 512 / 1024 / 2048 px", "6 colores"),
        ("Nombre", "240 / 320 / 480 / 640 / 960 / 1280 / 1920 / 2560 / 3840 px", "6 colores"),
    ]
    for i,row in enumerate(rows):
        y=483-i*61
        rect(64,y-10,1072,59,PAPER if i%2==0 else "#FFFFFF")
        for x,v in zip(xcols,row):
            text(x,y+13,v,14,INK,x==82)
    for x,title,desc in [
        (64,"SVG",["Archivo principal para web y diseño.","Trazados editables, sin fuentes externas.","24 maestros transparentes."]),
        (430,"PNG",["Transparencia real y compatibilidad amplia.","186 exportaciones de logo.","Adecuado para slides y documentos."]),
        (796,"WebP",["Transparencia y compresión sin pérdida.","186 exportaciones de logo.","Alternativa ráster para el website."]),
    ]:
        text(x,227,title,29,INK,True)
        lines(x,190,desc,15,gap=26)
    text(64,80,"El sufijo 640w indica 640 píxeles de ancho; la altura conserva siempre la proporción.",14,MUTED)
    finish()


def icons():
    page("Iconos y tarjetas sociales", 6, "Archivos separados para cada espacio de uso.")
    rect(64,309,512,280,PAPER,radius=12)
    text(88,549,"Iconos de navegador",20,INK,True)
    for i,n in enumerate([16,32,48,64,96]):
        x=90+i*93
        image(ROOT / f"web/favicon-{n}.png",x+(80-n)/2,401,n,n)
        text(x+17,369,f"{n} px",12,MUTED)
    text(88,331,"SVG adaptable + ICO con varias resoluciones",14,INK)
    rect(603,309,533,280,DARK,radius=12)
    text(627,549,"Iconos de aplicación",20,"#FFFFFF",True)
    image(ROOT / "web/apple-touch-icon.png",640,364,135,135)
    image(ROOT / "web/maskable-icon-512.png",854,364,135,135)
    text(645,331,"Apple · 180 px",13,"#A9B4BE")
    text(850,331,"Maskable · 192 / 512 px",13,"#A9B4BE")
    specs = [
        ("Open Graph", "1200 × 630 / 2400 × 1260", "Vista previa de enlaces"),
        ("Cuadrado", "1080 × 1080", "Publicación o portada cuadrada"),
        ("Avatar", "800 × 800", "Perfil y directorios"),
        ("Banner", "1920 × 640", "Composición panorámica de marca"),
    ]
    for i,(name,dimensions,usage) in enumerate(specs):
        y=251-i*43
        text(66,y,name,16,INK,True)
        text(265,y,dimensions,16,INK)
        text(682,y,usage,15,MUTED)
    text(64,73,"Las piezas sociales incluyen versiones claras y oscuras, en SVG, PNG y JPG.",14,MUTED)
    finish()


def rules():
    page("Color y reglas de uso", 7, "Valores de producción para esta versión del sistema de marca.")
    for i,(label,hx) in enumerate([("Cian","#0AA7ED"),("Grafito","#4B4F52"),("Fondo oscuro",DARK),("Blanco","#FFFFFF")]):
        x=64+i*274
        rect(x,462,250,124,hx,LINE if hx=="#FFFFFF" else None,9)
        text(x,430,label,18,INK,True)
        text(x,406,hx,14,MUTED)
    rect(64,130,510,239,PAPER,radius=12)
    text(88,334,"Espacio y tamaño",21,INK,True)
    lines(88,294,["Deja alrededor al menos 1/4 de la altura", "del símbolo. Aumenta el aire en portadas.", "", "Horizontal: desde 180 px de ancho.", "Símbolo: desde 24 px; favicon aparte."],16,gap=29)
    text(622,334,"Conserva la identidad",21,INK,True)
    lines(622,294,["Mantén proporciones y colores del archivo.","Usa la versión inversa en fondos oscuros.","Elige un fondo uniforme y con buen contraste.","Evita estirar, añadir efectos o recolorear letras.","El nombre del logo ya está convertido a trazados."],16,gap=32)
    text(64,81,"Paleta RGB / sRGB para uso digital. Para imprenta, pide conversión con el perfil de la imprenta.",14,MUTED)
    finish()


def handoff():
    page("Listo para diseño y desarrollo", 8, "El paquete completo y una selección ligera para integrar al website.")
    rect(64,146,515,448,DARK,radius=12)
    text(90,552,"QUÉ ABRIR PRIMERO",12,BLUE,True)
    lines(90,506,["Chainmakers-ai-Portfolio.pdf","README.md","integration/INTEGRACION.md"],20,"#FFFFFF",gap=43,bold=True)
    text(90,329,"PARA EL EQUIPO WEB",12,BLUE,True)
    lines(90,287,["Copia web-ready/brand/ a public/brand/.","Integra el favicon y los metadatos del ejemplo.","Usa el SVG horizontal en la cabecera.","Elige color o reverse según el fondo."],16,"#D1DAE2",gap=32)
    text(630,553,"Incluido en la entrega",24,INK,True)
    items=[
        ("01","Maestros SVG y ráster transparentes"),
        ("02","Favicons, Apple y manifest de iconos"),
        ("03","Tarjetas sociales claras y oscuras"),
        ("04","Ejemplos HTML, CSS y componente TSX"),
        ("05","Inventario, checksums y validación"),
        ("06","Concepto original y scripts de exportación"),
    ]
    for i,(n,label) in enumerate(items):
        y=495-i*51
        text(631,y,n,13,BLUE,True)
        text(671,y,label,16,INK)
    text(64,86,"Alcance: activos y guía visual. La publicación de Chainmakers.ai se realiza desde el proyecto del website.",14,MUTED)
    finish()


for section in [cover,family,variants,applications,sizes,icons,rules,handoff]:
    section()
C.save()
print(ROOT / "Chainmakers-ai-Portfolio.pdf")
