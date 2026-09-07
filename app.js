"use strict";
(() => {
  const layouts = {
    horizontal: { label: "Horizontal", view: [1720, 450], sizes: [240,320,480,640,960,1280,1920,2560,3840] },
    stacked: { label: "Vertical", view: [1280, 860], sizes: [256,512,1024,2048,4096] },
    symbol: { label: "Símbolo", view: [512, 512], sizes: [32,48,64,128,256,512,1024,2048] },
    wordmark: { label: "Nombre", view: [1220, 245], sizes: [240,320,480,640,960,1280,1920,2560,3840] }
  };
  const colors = { color: "Principal", reverse: "Inversa", graphite: "Grafito", white: "Blanco", cyan: "Cian", black: "Negro" };
  const state = { layout: "horizontal", color: "color", background: "light", format: "svg", size: 1280 };
  const preview = document.querySelector("#logo-preview");
  const img = document.querySelector("#preview-image");
  const format = document.querySelector("#file-format");
  const size = document.querySelector("#file-size");
  const download = document.querySelector("#download-logo");
  const pressed = (selector, key, value) => document.querySelectorAll(selector).forEach(button => button.setAttribute("aria-pressed", String(button.dataset[key] === value)));

  function render() {
    const layout = layouts[state.layout];
    const stem = `chainmakers-${state.layout}-${state.color}`;
    img.src = `brand/svg/${state.layout}/${stem}.svg`;
    img.dataset.layout = state.layout;
    img.width = layout.view[0]; img.height = layout.view[1];
    img.alt = `Logo ${layout.label.toLowerCase()} de Chainmakers, versión ${colors[state.color].toLowerCase()}`;
    document.querySelector("#preview-label").textContent = `${layout.label} / ${colors[state.color]}`.toUpperCase();
    preview.dataset.background = state.background;
    preview.classList.toggle("grid-dark", ["white","reverse"].includes(state.color));
    pressed("button[data-layout]", "layout", state.layout);
    pressed("[data-color]", "color", state.color);
    pressed("[data-bg]", "bg", state.background);
    size.replaceChildren();
    size.disabled = state.format === "svg";
    if (state.format === "svg") {
      size.add(new Option("Cualquier tamaño", "vector"));
      download.href = `brand/svg/${state.layout}/${stem}.svg`;
      document.querySelector("#file-description").textContent = "Vectorial · fondo transparente. Escala sin perder nitidez.";
    } else {
      if (!layout.sizes.includes(state.size)) state.size = layout.sizes.includes(1024) ? 1024 : 1280;
      layout.sizes.forEach(width => size.add(new Option(`${width} px de ancho`, String(width), false, width === state.size)));
      download.href = `brand/${state.format}/${state.layout}/${stem}-${state.size}w.${state.format}`;
      const height = Math.ceil(state.size * layout.view[1] / layout.view[0]);
      document.querySelector("#file-description").textContent = `${state.size} × ${height} px · fondo transparente${state.format === "webp" ? " · sin pérdida" : ""}.`;
    }
    download.download = download.href.split("/").pop();
    download.replaceChildren(document.createTextNode(`Descargar ${state.format.toUpperCase()} `));
    const arrow = document.createElement("span"); arrow.setAttribute("aria-hidden", "true"); arrow.textContent = "↓"; download.append(arrow);
  }

  document.querySelectorAll("button[data-layout]").forEach(button => button.addEventListener("click", () => { state.layout = button.dataset.layout; render(); }));
  document.querySelectorAll("button[data-color]").forEach(button => button.addEventListener("click", () => {
    state.color = button.dataset.color;
    state.background = ["reverse","white","cyan"].includes(state.color) ? "dark" : "light";
    render();
  }));
  document.querySelectorAll("button[data-bg]").forEach(button => button.addEventListener("click", () => { state.background = button.dataset.bg; render(); }));
  format.addEventListener("change", () => { state.format = format.value; render(); });
  size.addEventListener("change", () => { state.size = Number(size.value); render(); });
  document.querySelectorAll("[data-copy]").forEach(button => button.addEventListener("click", async () => {
    const hex = button.dataset.copy;
    const status = document.querySelector("#copy-status");
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(hex);
      status.textContent = `${hex} copiado. Listo para tu diseño.`;
    } catch { status.textContent = `Copia este valor: ${hex}`; }
  }));
  render();
})();
