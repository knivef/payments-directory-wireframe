# Prompt 04: SEO pass

Runs over every built page after templates are approved. Fixes metadata,
schema and links in one sweep so they are consistent.

---

```
Run the SEO pass on DIRECTORY_NAME's wireframe. Read docs/seo-spec.md and
docs/deconstruction.md section 5 (what the benchmark does well and badly).

For every file in src/pages/:

1. Title: apply the formula for its template from docs/seo-spec.md. Under 60
   characters where possible. Brand suffix only where the formula has one.
2. Description: 140 to 160 characters, primary keyword plus a reason to click.
   Never a copy of the title (a benchmark mistake). On compare pairs, reuse the
   verdict line.
3. Breadcrumbs: every page except home and 404 has a "crumbs" list in its meta.
   render.py turns it into visible breadcrumbs and BreadcrumbList JSON-LD.
4. JSON-LD: match the template's types in the seo-spec table. Homepage must have
   Organization plus WebSite with SearchAction (the benchmark has none). Only
   add aggregateRating where 3+ real reviews exist. Any FAQ uses "faq" in meta,
   never hand-written FAQPage.
5. Headings: one H1 that matches search intent, not a slogan. No skipped
   levels. Fix typos in headings (the benchmark ships "Statisic").
6. Internal links: apply the rules in docs/sitemap.md. Every provider profile
   links its service pages, HQ country and alternatives. Every guide ends in a
   commercial path. Every hub reachable in two clicks via nav or footer.
7. E-E-A-T: every guide-type page shows author, reviewer, last reviewed date
   and sources, as placeholders until real.

Then:
- Reconcile docs/seo-spec.md and docs/cta-map.md with what is actually built.
  If a page deviates from the spec for a good reason, update the spec and say
  why. Do not leave them disagreeing.
- Draft robots.txt and a sitemap index for the real build in docs/seo-spec.md.
  Do NOT add them to site/: the wireframe stays noindex.

python3 scripts/render.py, then ./scripts/check.sh. Report: a table of route,
title length, description length, JSON-LD types, H1 text.
```
