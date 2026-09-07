# Chainmakers.ai — Brand portfolio

Portfolio estático con explorador de logos y descargas del paquete de marca.

## Publicación

GitHub Pages: https://siulynot.github.io/chainmakers.ai/

La fuente de Pages es la rama `main`, carpeta raíz. `.nojekyll` permite servir
directamente los archivos estáticos. No se necesitan dependencias ni un build de Node.

Este repositorio publica el portfolio de identidad, no un website corporativo con
funciones comerciales. No modifica la configuración DNS del dominio chainmakers.ai.

## Estructura

- `index.html`, `styles.css`, `app.js`: galería adaptable a móvil, selección de composición,
  color, fondo de vista previa, formato y resolución; copia de códigos de color.
- `brand/`: 24 maestros SVG, 186 PNG, 186 WebP, iconos, social, integración y fuentes de exportación.
- `downloads/`: paquete ZIP completo y guía PDF.
- `site.webmanifest`: rutas relativas, compatibles con el subdirectorio de GitHub Pages.
- `og.png`: tarjeta social específica del portfolio, creada con ImageGen.

Todos los assets son locales; no hay fuentes, analítica ni dependencias de terceros.
Los SVG contienen trazados reales; los PNG/WebP del logo tienen transparencia.
La comprobación de los assets está en `brand/validation.json` y los checksums en `brand/SHA256SUMS.txt`.

## Validación y vista local

```sh
node --check app.js
python3 tools/check_site.py
python3 -m http.server 4173
```

Abrir http://localhost:4173/. El website funciona sin compilación.
La galería requiere JavaScript para cambiar variantes; los enlaces de descarga
principal, PDF y ZIP siguen disponibles sin JavaScript.

Para cambiar al dominio personalizado, configurar primero DNS/Pages y actualizar
canonical y Open Graph al host efectivo. No se incluye CNAME hasta esa configuración.
