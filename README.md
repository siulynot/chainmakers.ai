# Chainmakers.ai

Website corporativo de Chainmakers LLC: consultoría administrativa, desarrollo de software,
automatización con IA e integración de sistemas, desde Puerto Rico.

Publicado en https://siulynot.github.io/chainmakers.ai/ mediante GitHub Pages, rama `main`, raíz.
El dominio personalizado no se ha configurado.

## Contenido

- Servicios: consultoría administrativa, software, automatización e integración.
- Productos en operación: ChainAccounts y MedReq.
- Iniciativas en definición: Chainmakers AEC (diseño) y ChainFinance (propuesta).
- Método de trabajo, presentación de empresa y contacto.

El contenido comercial se preparó a partir del mapa empresarial, los contextos de producto
y los alcances de trabajo documentados, revisados el 7 de septiembre de 2026. La agrupación
de capacidades en cuatro servicios es editorial. No se publican propuestas confidenciales,
datos de clientes, precios internos, casos inventados ni certificaciones no verificadas.

## Contacto

El formulario prepara un correo dirigido a `chainmakerspr@gmail.com` en la aplicación
del visitante. La persona revisa y envía el mensaje. El sitio no transmite ni almacena
los campos en un servidor, y no muestra una confirmación falsa de envío.
El enlace directo de correo también funciona sin JavaScript.

## Desarrollo

HTML, CSS y JavaScript sin dependencias de terceros ni compilación.

```sh
node --check app.js
node tools/check_inquiry.cjs
python3 tools/check_site.py
python3 -m http.server 4173
```

## Recursos de marca

El paquete de logos, los favicons y las descargas se conservan en `brand/` y `downloads/`.
La galería anterior se mantiene en `brand-portfolio.html` como recurso secundario.
`og.png` es la tarjeta social del website de servicios, generada con ImageGen.

Antes de configurar un dominio propio, actualizar canonical y las URLs de Open Graph
al dominio efectivo. El manifest usa rutas relativas para funcionar bajo GitHub Pages.
