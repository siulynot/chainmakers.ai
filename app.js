"use strict";
function buildInquiry(data) {
  const recipient = "chainmakerspr@gmail.com";
  const subject = `Consulta de servicios: ${data.interest}`;
  const body = `Hola, Chainmakers.\n\nSoy ${data.name}.${data.company ? ` Mi empresa es ${data.company}.` : ""}\n\nMe interesa: ${data.interest}\n\n${data.message}\n\nGracias.`;
  return `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
if (typeof module !== "undefined") module.exports = { buildInquiry };
if (typeof document !== "undefined") {
  const form = document.querySelector("#contact-form");
  const interest = document.querySelector("#contact-interest");
  document.querySelector("#prepare-inquiry").disabled = false;
  document.querySelectorAll("[data-interest]").forEach(link => link.addEventListener("click", () => { interest.value = link.dataset.interest; }));
  form.addEventListener("submit", event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const fields = Object.fromEntries(["name","company","interest","message"].map(key => [key, String(data.get(key) || "").trim()]));
    if (!fields.name || fields.message.length < 10) {
      document.querySelector("#contact-status").textContent = "Escribe tu nombre y al menos 10 caracteres sobre tu proyecto.";
      return;
    }
    window.location.href = buildInquiry(fields);
    document.querySelector("#contact-status").textContent = "Revisa tu aplicación de correo para enviar la consulta. Si no se abrió, escríbenos a chainmakerspr@gmail.com.";
  });
}
