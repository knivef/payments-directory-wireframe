# Sitemap and information architecture

Our directory, working name `[DIRECTORY NAME]`. Broad PSP scope, same breadth as
PayAtlas. This is the target IA for the real build. The wireframe builds one
sample page per template; every link to an unbuilt entity points at that
template's sample page.

## Primary navigation

| Item | Type | Contents |
|---|---|---|
| Providers | Mega menu | 5 service categories, each listing its sub-services. Footer link "Browse all providers". Feature card: "Not sure where to start? Use the match tool". |
| Compare | Link | `/compare/` |
| Guides | Mega menu | Countries (by region), Industries (by vertical), Payment methods, Regulators, MCC codes, Glossary |
| Community | Mega menu | Journal, Events, (later) Discussions, Jobs |
| For providers | Link | `/for-providers/` |
| Right side | Buttons | "Sign in" (ghost, opens auth modal), "Find a provider" (primary, `/match/`) |

Rule: no more than five top-level items. Everything else lives in the footer.

## Footer

Five columns: Providers (5 categories), Guides (6 reference types), Tools (Match,
Compare, Assist, Trust badges), Company (About, How we rank, Ownership, Roadmap,
Contact), Legal (Terms, Privacy, Cookies, Disclaimer). Newsletter band above.
Ownership and ranking links sit in the footer on every page. That is the
neutrality signal PayAtlas lacks.

## URL map

Clean slugs, trailing slash, no numeric IDs unless two entities collide.

| Template | URL pattern | Indexable | Target volume at launch | Wireframe sample |
|---|---|---|---|---|
| Home | `/` | yes | 1 | `/` |
| Directory listing | `/providers/` | yes | 1 | `/providers/` |
| Service category landing | `/providers/{service}/` | yes | about 70 | `/providers/card-processing/` |
| Service by country (phase 2) | `/providers/{service}/{country}/` | yes, only with 5+ providers | gated | none |
| Provider profile | `/provider/{slug}/` | yes | all published | `/provider/provider-alpha/` |
| Compare index | `/compare/` | yes | 1 | `/compare/` |
| Compare pair | `/compare/{a}-vs-{b}/` | yes, alphabetical order, one canonical per pair | top 150 pairs | `/compare/provider-alpha-vs-provider-beta/` |
| Match tool | `/match/` | yes (landing), results noindex | 1 | `/match/` |
| Assist (concierge) | `/assist/` | yes | 1 | `/assist/` |
| Provider program | `/for-providers/` | yes | 1 | `/for-providers/` |
| Country index | `/countries/` | yes | 1 | `/countries/` |
| Country guide | `/countries/{country}/` | yes | about 200 | `/countries/brazil/` |
| Industry vertical | `/industries/{vertical}/` | yes | about 20 | `/industries/igaming/` |
| Sub-industry | `/industries/{vertical}/{sub}/` | yes | about 90 | uses vertical template |
| Payment method | `/payment-methods/{slug}/` | yes | about 280 | `/payment-methods/pix/` |
| Glossary term | `/glossary/{term}/` | yes | about 270 | `/glossary/3ds/` |
| MCC code | `/mcc/{code}/` | yes | about 930 | `/mcc/5967/` |
| Regulator | `/regulators/{slug}/` | yes | about 300 | uses glossary shell |
| Journal article | `/journal/{slug}/` | yes | editorial | `/journal/sample-guide/` |
| Events index | `/events/` | yes | 1 | `/events/` |
| Account, search results, filters with query strings | `/account/`, `?q=`, `?filter=` | no | | |
| UGC (discussions, jobs) | `/community/...` | noindex until 20+ quality posts | | |

## Sitemap files

`/sitemap.xml` is an index pointing at one file per template: `pages.xml`,
`providers.xml`, `services.xml`, `compare.xml`, `countries.xml`,
`industries.xml`, `payment-methods.xml`, `glossary.xml`, `mcc.xml`,
`regulators.xml`, `journal.xml`, `events.xml`. Each URL carries lastmod from the
record's real last-reviewed date, never the deploy date.

## Taxonomy

Service categories (same split as PayAtlas, which matches how buyers search):

1. Merchant services: card processing, merchant accounts, acquiring, APMs, crypto payments, BNPL, subscriptions and billing, payouts, real-time payments, invoicing
2. Payment technology: orchestration, fraud prevention, AML and KYC, 3DS, tokenisation, reconciliation, PCI DSS, open banking, white label
3. Business support: legal, compliance and licensing, consulting, onboarding, IBAN accounts, accounting, insurance
4. Money movement: FX, wallets, card issuing, embedded finance, remittance, neobanks, cross-border
5. Build partners: software development, e-commerce development, blockchain development, marketing

The machine-readable version is `data/taxonomy.json`.

## Internal linking rules

- Every provider profile links to each of its service category pages, its HQ country guide and three alternatives.
- Every service category page links to its top 10 providers, three related categories and the top three compare pairs in that category.
- Every country, industry and payment method guide ends in a "Providers that support {X}" list linking to filtered category pages and the match tool.
- Glossary terms are auto-linked once per page on first mention inside guides.
