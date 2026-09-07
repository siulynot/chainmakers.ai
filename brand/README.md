# Chainmakers.ai - Brand kit v1.0

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
