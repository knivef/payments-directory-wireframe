# Payments directory wireframe

Internal wireframe of a broad payments provider directory, benchmarked against
payatlas.com. Not for indexing.

- **Start here:** `docs/deconstruction.md`, the full PayAtlas teardown
- **Specs:** `docs/sitemap.md`, `docs/seo-spec.md`, `docs/cta-map.md`, `docs/ads-spec.md` (v2)
- **Versions:** `main` is v1 (no ads). `v2` adds banner, margin, in-content and sponsored listing ads.
- **Rebuild from scratch:** run `prompts/00-orchestrator.md` in Claude Code
- **Browse the wireframe:** `/hub/` on the deployed site

## Local

```bash
python3 scripts/render.py
./scripts/check.sh
python3 -m http.server 4321 --directory site
```

See `CLAUDE.md` for structure and house rules.
