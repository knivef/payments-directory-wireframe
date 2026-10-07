# CLAUDE.md

Repo context. Read before any task here.

## What this repo is

An internal wireframe of a broad payments provider directory, benchmarked
against payatlas.com. Three deliverables live together:

1. `docs/`: the PayAtlas teardown and our IA, SEO and CTA specs
2. `prompts/`: a five-stage prompt chain that builds the wireframe from scratch
3. `site/`: the rendered wireframe, 17 templates plus hub and 404, served by Vercel

Working brand name is the literal placeholder `[DIRECTORY NAME]`.

## Layout

```
docs/deconstruction.md   PayAtlas teardown: model, IA, sitemap, templates, design, SEO, CTAs, gaps
docs/sitemap.md          Our URL map, nav, footer, taxonomy, linking rules
docs/seo-spec.md         Title and description formulas, JSON-LD per template, robots, E-E-A-T
docs/cta-map.md          Every CTA by template and intent, data-cta names, auth gating
prompts/00..05           Orchestrator, IA, design system, templates, SEO pass, QA and deploy
data/*.json              Taxonomy, fictional sample providers, FAQ source of truth
src/pages/*.html         Page bodies with a meta block. One file per template.
scripts/render.py        Wraps bodies with shared chrome, expands macros, writes site/
scripts/check.sh         Health check. Run before every push.
scripts/bootstrap.sh     One-time commit, GitHub repo create, Vercel deploy
assets/                  tokens.css, base.css, site.js (copied into site/ on render)
site/                    Rendered output. Committed. Never edit by hand.
```

## Rules

**Edit src, not site.** Change `src/pages`, `data`, `assets` or
`scripts/render.py`, then run `python3 scripts/render.py`. `check.sh` fails if
site/ is stale.

**Tokens only in tokens.css.** base.css reads tokens and never defines one or
hardcodes a hex colour. The allowlist is in `check.sh` section 4.

**FAQs come from data/faqs.json only.** The page accordion and the FAQPage
JSON-LD both render from it, so they cannot drift.

**No build step on Vercel.** render.py runs locally; site/ is committed.
No framework, no package manager. If a task seems to need one, stop and ask.

## House rules

- No em dashes anywhere. No double hyphen as punctuation.
- No invented facts: counts, prices, customers, quotes, licences, dates stay as
  literal `[BRACKETED PLACEHOLDERS]` until verified.
- Sample providers are fictional (Provider Alpha, Beta...). Never use a real
  company as sample data.
- No AI register: seamless, robust, unlock, empower, leverage, landscape,
  "in today's", "designed to", "tailored to".
- Comparison tables include at least one row where each side wins or ties.
- Delete a proof section rather than ship placeholder proof at launch.
- The whole wireframe is noindex (vercel.json header plus meta robots). Keep it.

## Preview

```bash
python3 scripts/render.py && python3 -m http.server 4321 --directory site
```

Open http://localhost:4321/hub/ for the template index. The yellow notes
explain each decision against the benchmark; toggle them bottom right.

## Before every push

```bash
./scripts/check.sh
```
