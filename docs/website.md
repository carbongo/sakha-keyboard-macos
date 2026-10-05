# Website

Landing page at https://sakha-kb.vercel.app, plus `/ru` and `/sah` (Vercel project `sakha-kb`, Git-connected, production branch `main`).

- Every language is a full static page (works with `curl`, no JS needed for text). Language switch = links + `hreflang` alternates.
- `tools/build-site.py` renders `tools/site-template.html` with its per-language strings table into `site/index.html`, `site/ru/index.html`, `site/sah/index.html`. A key missing in any language fails the build. Version comes from `build.py`'s `VERSION`.
- Shared static files: `site/style.css`, `site/app.js`, `site/favicon.svg`. Paths are absolute (`/layouts/…`).
- `vercel.json` copies `docs/layouts/*.svg` into `site/layouts/` at build time (gitignored).
- Preview: `cp -R docs/layouts site/layouts && python3 -m http.server -d site`.
- Text mirrors the READMEs; ru/sah reuse their wording. New Sakha phrases need the owner's review.
