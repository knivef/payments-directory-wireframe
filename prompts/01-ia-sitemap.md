# Prompt 01: Information architecture and sitemap

Produces the URL map, navigation, footer and service taxonomy. Everything later
reads from these, so get them approved before any HTML.

---

```
Design the information architecture for DIRECTORY_NAME, a SCOPE payments
provider directory. Use docs/deconstruction.md sections 2 and 3 as the
benchmark. Do not copy their structure blindly. Keep what serves search intent,
fix what the teardown flags as weak.

## Part A: entity types and URL map

List every entity type the directory will publish. For each, give:
- Template name
- URL pattern (clean slugs, trailing slash, no numeric IDs unless two records collide)
- Indexable yes or no, and the rule that decides it (for example "only with 5+ providers")
- Expected page count at launch (estimate, labelled as an estimate)
- Which sample page the wireframe will build

Must include at minimum: home, directory listing, service category landing
(one per service, crawlable path, not a query string), provider profile,
compare index, compare pair, match tool, concierge/assist landing, provider
program with pricing, country index, country guide, industry guide, payment
method, glossary term, MCC code, journal article, events, 404.

Decide and document:
- Which URLs are noindex (account, search results, filter combinations, thin UGC)
- Compare pair canonical rule (alphabetical, b-vs-a redirects to a-vs-b)
- Phase 2 combinations, such as /providers/{service}/{country}/, and the
  threshold for publishing them

## Part B: navigation

Top nav: five items maximum, plus "Sign in" (ghost) and one primary CTA on the
right. Specify which items are mega menus and the exact columns and links in
each. The providers mega menu must include a feature card that pushes to the
match tool.

Mobile: a drawer with one collapsible group per category, then guides,
community, compare, for providers, sign in.

## Part C: footer

Five link columns plus a brand column. The Company column must include "How we
rank" and "Ownership". These answer the neutrality question the benchmark
leaves open.

## Part D: taxonomy

Write data/taxonomy.json with: categories (slug, name, icon key, one-line blurb,
services[]), regions[], countries_sample[], industries[], payment_methods[],
guides[] (name, href, blurb). Use 5 categories and 4 to 10 services each.
Counts are placeholders, never invented figures.

## Part E: internal linking rules

Write the rules that guarantee every hub is within two clicks of every page,
and that every guide ends in a commercial path (category page or match tool).

## Output

1. docs/sitemap.md with Parts A, B, C, E as tables
2. data/taxonomy.json (Part D), valid JSON

Then stop and list the three IA decisions you are least sure about.
```
