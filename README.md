# Chainmakers.ai

Corporate website for Chainmakers: an AI-native product and systems company building
software for real-world operations.

Published at https://siulynot.github.io/chainmakers.ai/ through GitHub Pages, from `main`.

The homepage explains the thesis, products, capabilities, Chainmakers Method, operating
provenance, AI infrastructure and the workflow-first contact path. Products shown in
production are ChainAccounts and MedReq. PermitVault is presented as building; it is an
operational capability being shaped into a product. The site keeps Chainmakers AEC and
ChainFinance out of the primary product grid until their documented phases advance.

The contact form does not store visitor data. It prepares a `mailto:` message to
`chainmakerspr@gmail.com` so the visitor reviews and sends it from their own email client.

The old logo gallery is preserved at `brand-portfolio.html`. The complete logo kit, PDF,
favicons and social assets remain under `brand/` and `downloads/`.

## Local checks

```sh
node --check app.js
node tools/check_inquiry.cjs
python3 tools/check_site.py
python3 -m http.server 4173
```

The site is dependency-free HTML, CSS and JavaScript. Update canonical/Open Graph URLs if
the GitHub Pages subdomain moves to a custom domain.
