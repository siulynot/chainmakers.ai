#!/usr/bin/env python3
"""Reproducible vector conversion and web exports of the approved logo concept.

Dependencies: Python 3, ImageMagick, potrace, librsvg, reportlab, Poppler.
The original bitmap is retained; all delivered logo variants are path-only SVGs.
"""
from pathlib import Path
import copy
import csv
import hashlib
import json
import math
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
TMP = ROOT / "_work"
SOURCE = ROOT / "source/chainmakers-original-concept.png"
SVGNS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVGNS)
COLORS = {
    "color": ("#4B4F52", "#0AA7ED"),
    "reverse": ("#FFFFFF", "#0AA7ED"),
    "graphite": ("#4B4F52", "#4B4F52"),
    "white": ("#FFFFFF", "#FFFFFF"),
    "cyan": ("#0AA7ED", "#0AA7ED"),
    "black": ("#000000", "#000000"),
}
LAYOUTS = {
    # viewBox and positioned components; each component has its original local canvas.
    "horizontal": (1720, 450, [("symbol", 40, 40, 1), ("wordmark", 535, 142.5, 1)]),
    "stacked": (1280, 860, [("symbol", 347.5, 70, 1.3), ("wordmark", 70, 625, 1)]),
    "symbol": (512, 512, [("symbol", 31, 71, 1)]),
    "wordmark": (1220, 245, [("wordmark", 40, 40, 1)]),
}
WIDTHS = {
    "horizontal": [240, 320, 480, 640, 960, 1280, 1920, 2560, 3840],
    "stacked": [256, 512, 1024, 2048, 4096],
    "symbol": [32, 48, 64, 128, 256, 512, 1024, 2048],
    "wordmark": [240, 320, 480, 640, 960, 1280, 1920, 2560, 3840],
}


def run(*args):
    subprocess.run([str(a) for a in args], check=True, capture_output=True)


def save(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def trace():
    TMP.mkdir(exist_ok=True)
    crops = {"symbol": "450x370+150+225", "wordmark": "1140x165+650+325"}
    thresholds = {
        "gray": "(max(r,max(g,b))-min(r,min(g,b)) < 0.14 && r < 0.65) ? 0 : 1",
        "blue": "(b-r > 0.25 && g-r > 0.15 && b > 0.6) ? 0 : 1",
    }
    groups = {}
    for component, crop in crops.items():
        groups[component] = {}
        for layer, expression in thresholds.items():
            mask = TMP / f"{component}-{layer}.pbm"
            vector = TMP / f"{component}-{layer}.svg"
            run("magick", SOURCE, "-crop", crop, "+repage", "-fx", expression,
                "-threshold", "50%", mask)
            run("potrace", mask, "--svg", "--output", vector,
                "--turdsize", "8", "--opttolerance", "0.2")
            tree = ET.parse(vector).getroot()
            group = tree.find(f"{{{SVGNS}}}g")
            groups[component][layer] = ET.tostring(group, encoding="unicode")
    return groups


def logo_content(layout, colorway, groups):
    out = []
    for component, x, y, scale in LAYOUTS[layout][2]:
        layers = []
        for layer, color in zip(("gray", "blue"), COLORS[colorway]):
            g = ET.fromstring(groups[component][layer])
            g.set("fill", color)
            layers.append(ET.tostring(g, encoding="unicode"))
        out.append(f'<g transform="translate({x} {y}) scale({scale})">{"".join(layers)}</g>')
    return "".join(out)


def svg_document(width, height, content, title="Chainmakers"):
    return (f'<svg xmlns="{SVGNS}" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{content}</svg>\n')


def masters(groups):
    for layout, (w, h, _) in LAYOUTS.items():
        for colorway in COLORS:
            save(ROOT / f"svg/{layout}/chainmakers-{layout}-{colorway}.svg",
                 svg_document(w, h, logo_content(layout, colorway, groups)))
    # A single monochrome shape for CSS masks, Safari pinned tabs, and one-color artwork.
    shutil.copyfile(ROOT / "svg/symbol/chainmakers-symbol-black.svg", ROOT / "web/safari-pinned-tab.svg")
    symbol = logo_content("symbol", "color", groups)
    adaptive = ('<style>.brand-gray{fill:#4B4F52}.brand-blue{fill:#0AA7ED}'
                '@media(prefers-color-scheme:dark){.brand-gray{fill:#FFFFFF}}</style>')
    symbol = symbol.replace('fill="#4B4F52"', 'class="brand-gray"').replace('fill="#0AA7ED"', 'class="brand-blue"')
    save(ROOT / "web/favicon.svg", svg_document(512, 512, adaptive + symbol))


def export_one(job):
    layout, colorway, width = job
    source = ROOT / f"svg/{layout}/chainmakers-{layout}-{colorway}.svg"
    stem = f"chainmakers-{layout}-{colorway}-{width}w"
    png = ROOT / f"png/{layout}/{stem}.png"
    webp = ROOT / f"webp/{layout}/{stem}.webp"
    png.parent.mkdir(parents=True, exist_ok=True)
    webp.parent.mkdir(parents=True, exist_ok=True)
    run("rsvg-convert", "--width", width, "--output", png, source)
    run("magick", png, "-strip", "-define", "webp:lossless=true", webp)


def exports():
    jobs = [(layout, colorway, width) for layout in LAYOUTS for colorway in COLORS for width in WIDTHS[layout]]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(export_one, jobs))
    print(f"Exported {len(jobs)} PNG and {len(jobs)} lossless WebP files", flush=True)


def canvas_logo(groups, layout, colorway, canvas_w, canvas_h, x, y, width, background):
    native_w = LAYOUTS[layout][0]
    content = f'<rect width="{canvas_w}" height="{canvas_h}" fill="{background}"/>'
    content += f'<g transform="translate({x} {y}) scale({width/native_w})">{logo_content(layout,colorway,groups)}</g>'
    return svg_document(canvas_w, canvas_h, content)


def web_assets(groups):
    web = ROOT / "web"
    for size in [16, 32, 48, 64, 96, 128, 192, 256, 512]:
        run("rsvg-convert", "--width", size, "--output", web / f"favicon-{size}.png",
            ROOT / "svg/symbol/chainmakers-symbol-color.svg")
    run("magick", *[web / f"favicon-{n}.png" for n in [16, 32, 48, 64, 256]], web / "favicon.ico")
    # Full-bleed opaque app icon backgrounds; artwork inside the central safe area.
    for name, fraction, background, colorway in [
        ("app-icon", .84, "#FFFFFF", "color"),
        ("maskable-icon", .62, "#111820", "reverse"),
    ]:
        size = 512
        mark_w = size * fraction
        origin = (size - mark_w) / 2
        src = web / f"{name}.svg"
        save(src, canvas_logo(groups,"symbol",colorway,size,size,origin,origin,mark_w,background))
        for pixels in [192, 512]:
            run("rsvg-convert", "--width", pixels, "--output", web / f"{name}-{pixels}.png", src)
    run("rsvg-convert", "--width", 180, "--output", web / "apple-touch-icon.png", web / "app-icon.svg")
    manifest = {
        "id": "/", "name": "Chainmakers", "short_name": "Chainmakers",
        "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#FFFFFF", "theme_color": "#111820",
        "icons": [
            {"src": f"/brand/web/{name}-{size}.png", "sizes": f"{size}x{size}", "type": "image/png", "purpose": purpose}
            for name, purpose in [("app-icon", "any"), ("maskable-icon", "maskable")]
            for size in [192, 512]
        ],
    }
    save(web / "site.webmanifest", json.dumps(manifest, indent=2) + "\n")
    for theme, bg, cw in [("light", "#FFFFFF", "color"), ("dark", "#111820", "reverse")]:
        social = ROOT / "social"
        # Clean logo artwork only; the web team can supply page-specific copy.
        specs = [("opengraph",1200,630,"horizontal",1020),
                 ("square",1080,1080,"stacked",900),
                 ("avatar",800,800,"symbol",650),
                 ("banner",1920,640,"horizontal",1450)]
        for name, w, h, layout, lw in specs:
            lh = lw * LAYOUTS[layout][1] / LAYOUTS[layout][0]
            src = social / f"chainmakers-{name}-{theme}.svg"
            save(src, canvas_logo(groups,layout,cw,w,h,(w-lw)/2,(h-lh)/2,lw,bg))
            for factor in ([1, 2] if name == "opengraph" else [1]):
                suffix = "@2x" if factor == 2 else ""
                out = social / f"chainmakers-{name}-{theme}{suffix}.png"
                run("rsvg-convert", "--width", w*factor, "--output", out, src)
                run("magick", out, "-strip", "-quality", "94", out.with_suffix(".jpg"))


def main():
    (ROOT / "web").mkdir(parents=True, exist_ok=True)
    groups = trace()
    save(ROOT / "source/vector-components.json", json.dumps(groups, indent=2))
    masters(groups)
    print("Path-only SVG masters created", flush=True)
    exports()
    web_assets(groups)
    print("Web and social assets created", flush=True)


if __name__ == "__main__":
    main()
