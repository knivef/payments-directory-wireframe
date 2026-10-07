# Prompt 00: Orchestrator

Runs the whole chain for a payments directory wireframe, with an approval gate
after every stage. Paste the block below into Claude Code at the repo root.

Inputs you fill before running:

- `DIRECTORY_NAME`: working brand name, or leave as `[DIRECTORY NAME]`
- `BENCHMARK_URL`: the directory you are benchmarking (default https://payatlas.com)
- `SCOPE`: broad PSP directory, or a narrower angle (crypto, high-risk, a region)

---

```
You are building an internal HTML/CSS wireframe of a payments provider directory
called DIRECTORY_NAME, benchmarked against BENCHMARK_URL. Scope: SCOPE.

Read CLAUDE.md first. Then read docs/deconstruction.md in full. It is the
teardown of the benchmark and the reason for most decisions below.

Run these stages in order. After each one, stop, show me a short summary of
what changed and what you need me to decide, and wait for "go".

Stage 1. prompts/01-ia-sitemap.md
  Output: docs/sitemap.md, data/taxonomy.json
Stage 2. prompts/02-design-system.md
  Output: assets/tokens.css, assets/base.css, assets/site.js
Stage 3. prompts/03-templates.md
  Output: data/providers.json, data/faqs.json, src/pages/*.html, rendered site/
Stage 4. prompts/04-seo-pass.md
  Output: titles, descriptions, JSON-LD and internal links on every page,
  docs/seo-spec.md and docs/cta-map.md reconciled with what was built
Stage 5. prompts/05-qa-deploy.md
  Output: QA report, commit, GitHub push, Vercel deploy (ask before push and deploy)

Rules for every stage:
- House rules in CLAUDE.md are non-negotiable. No em dashes. No double hyphen
  as punctuation. No invented numbers, customers, quotes or licences: use a
  literal [BRACKETED PLACEHOLDER] instead.
- Plain HTML and CSS, rendered by scripts/render.py. No framework, no
  package manager, no build step on Vercel.
- Run ./scripts/check.sh at the end of stages 2, 3, 4 and 5. Do not hand back
  a stage with a failing check.
- When the benchmark does something we deliberately do differently, add a
  <span class="wf-note"> on the page saying what they do, what we do, and why.
```
