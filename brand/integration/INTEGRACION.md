# Integración en Chainmakers.ai

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
