# PayAtlas teardown

Source: https://payatlas.com, reviewed 2026-10-07. Live homepage, robots.txt, the
sitemap index and all 21 sub-sitemaps, and 14 page templates were fetched and
read. Counts below are what the site published on that date.

This document describes what PayAtlas does and why it works. It is reference
material for our own directory, not a spec to copy. Our spec lives in
`sitemap.md`, `seo-spec.md` and `cta-map.md`.

---

## 1. What the product is

PayAtlas is a payments industry directory with three revenue paths layered on
top of a free catalogue.

| Layer | Who it serves | How it makes money |
|---|---|---|
| Atlas (catalogue) | Merchants searching for a PSP | Free. Drives traffic and leads. |
| Assist (concierge) | Merchants who want a done-for-you match | Paid, "on request". 1 request, "3+ guaranteed solutions", KYC support, dedicated manager. Stated main focus: high-risk. |
| Provider program | PSPs and vendors | Free profile with Verified badge. "Plus" tier marked Soon: 10 match results per inquiry, one reroll, verified partner connections. |
| Content and data | Everyone, mostly via search | Indirect. Feeds the first three. |

Ownership: the footer links to Corefy, a payment orchestration company. That
matters for trust positioning. A directory owned by a vendor in the same market
has an obvious neutrality question, and PayAtlas never addresses it on page.
**Our opportunity:** state ownership and ranking rules openly.

The site shows a "beta" tag next to the logo and publishes a roadmap, a
changelog and a public product feedback board. It reads as a product under
active construction rather than a finished media site.

---

## 2. Information architecture

### 2.1 Primary navigation

Five mega menus, then two utility items on the right.

| Menu | Contents |
|---|---|
| **Atlas** | 5 service categories with about 70 sub-services in total. Feature card "Paytech Atlas" linking `/ecosystem`. "Browse all companies". |
| **Insights** | Direct link to data visualisations (heat maps). |
| **Community** | Experts, Journal, Events, Glossary, Discussions, Jobs, Connect (marked New). |
| **Solutions** | Navigator (guided search), Provider Comparison, For Providers, For Merchants. |
| **Resources** | Countries (13 regions), Industries (20 verticals, about 90 sub-industries), Payment Methods (11 categories), Financial Regulators (5 types), MCC codes, Associations, Currencies, Licenses (Soon), Certificates (Soon). Company links: About, Docs, Feedback, Roadmap, Changelog, Brand Assets, Trust Badges. |
| Right side | "Find a Provider" (primary CTA, goes to Navigator), account icon (opens auth modal). |

The mega menus are also the single biggest internal linking device on the site.
Every page carries several hundred links into the category, country and
industry hubs.

### 2.2 Service taxonomy (the "Atlas")

| Category | Companies | Example sub-services |
|---|---|---|
| Merchant Services | 1,156 | Card processing, merchant accounts, acquiring, BNPL, APMs, crypto, subscriptions, real-time, payouts, invoices |
| Payment Technologies | 367 | Orchestration, fraud, AML/KYC, 3DS, tokenisation, reconciliation, PCI DSS, open banking, white label |
| Business Support | 403 | Legal, compliance, consulting, onboarding, IBAN accounts, accounting, insurance, cybersecurity, funding |
| Asset Management | 644 | FX, wallets, card issuing, embedded finance, remittance, neobanks, cross-border |
| Development & Production | 35 | Software, AI/ML, blockchain, e-commerce, e-wallet, marketing, design |

A company can sit in several categories, so category counts sum to more than
the 1,440 total.

### 2.3 Sitemap

Sitemap index at `/sitemap.xml` with one sub-sitemap per entity type, each with
lastmod. About 4,000 indexable URLs.

| Sub-sitemap | URLs | URL pattern |
|---|---|---|
| companies | 1,361 | `/company/{slug}-{id}` |
| mcc-codes | 931 | `/mcc-codes/{code}-{slug}` |
| regulators | 319 | `/regulator/{slug}-{id}` |
| payment-methods | 278 | `/payment-method/{slug}-{id}` |
| glossaries | 273 | `/glossary/{slug}-{id}` |
| countries | 205 | `/countries/{name}-{iso2}` |
| associations | 123 | `/association/{slug}-{id}` |
| compare | 121 | `/compare/{a}-vs-{b}-{idA}-{idB}` |
| currencies | 118 | `/currency/{slug}-{id}` |
| industries | 113 | `/industry-vertical/{slug}-{id}` and `/industry/{slug}-{id}` |
| events | 101 | `/event/{slug}-{id}` |
| docs + categories | 39 | `/docs/{category}/{slug}` |
| releases | 34 | `/roadmap/{slug}-{id}` |
| general | 33 | Static pages |
| articles | 21 | `/journal/article/...` and `/journal/guide/...` |
| insights | 12 | `/insights/{slug}` |
| product-feedbacks | 11 | `/feedback/{slug}-{id}` |
| discussions | 5 | `/discussion/{slug}-{id}` |
| jobs | 1 | `/job/{slug}-{id}` |

Reading: the company profiles are the product, but more than half of the
indexable surface is programmatic reference content (MCC, regulators, methods,
glossary, countries, currencies, associations). That reference layer is the
long-tail SEO engine. Editorial content (21 articles) is thin by comparison.

### 2.4 robots.txt

```
Allow: /company  /events  /my/login  /my/registration
Disallow: /backoffice  /my  /atlas?  /*?returnUrl=*
```

Every filtered catalogue URL (`/atlas?services=card-processing-services`) is
blocked. The site has no indexable "card processing providers" page. Those are
the highest commercial-intent queries in the space. **This is the single
largest SEO gap and our clearest win.**

---

## 3. Page templates

Each template below lists its section order and heading skeleton as rendered.

### 3.1 Homepage `/`

13 sections, in order:

1. **Hero.** Pill "New · Explore Insights". H1 "Find Your Payment Service Partner *Match*" (accent word in serif italic). One-line subhead. Primary CTA "Find a Provider Match", secondary "Explore Atlas for free". Right side: collage of floating provider cards and logos over a globe.
2. **Stats strip.** 1,440 payment providers (+8 in last 30 days), 285 methods, 214 countries, 72 industries. Live counts, a freshness signal.
3. **Browse PSPs by category.** 5 cards (icon, name, one-line description, "N companies"). "Submit company" ghost button beside H2.
4. **Recently added companies.** 8 small logo cards (name, domain, country), "View all". Another freshness signal.
5. **Knowledge base.** H2 "Your guides into Paytech". Horizontal carousel of region cards with photography, then a carousel of industry cards with icons. "See all" on each.
6. **Community.** Featured articles (4 to 5 cards with date and read time), featured events (date tiles, city).
7. **For Authors.** Three CTAs: Start Discussion, Write Article, Add Event.
8. **Benefits.** Two columns, For merchants (4 points) and For providers (4 points), each with its own CTA.
9. **How it works.** Tabs For Merchants / For Providers, six steps: Explore, Find, Decide, Connect, Onboard, Review.
10. **Success stories.** "Join 400+ companies using PayAtlas". Logos and quotes.
11. **FAQ.** 5 questions focused on the Assist service.
12. **Assist CTA band.** "Get onboard with the right payment partner".
13. **Platform map.** All 5 categories with 10 sub-services each, as a link grid.

Then a closing CTA band ("Get connected with the right company for you"), a
provider-side band, newsletter signup, footer, floating feedback widget and a
cookie banner.

Heading notes: one H1, then H2 per section. An H2 reads "Statisic" (typo). One
event title is wrongly marked up as H2 inside the events list.

### 3.2 Catalogue listing `/atlas`

- H1 "Providers Atlas", line "1440 providers are already in the catalogue".
- Right promo card: "List your company, browse real merchant requests".
- Left filter rail: searchable checkbox facets with counts (Payment methods, Target regions, Services, Industries, and more). Collapses to a "Filters" button on mobile.
- Result header: "1440 companies", last-updated date, sort ("Popular first").
- Result rows: logo, name, rating and review count, domain, country, two-line blurb, "Connect" (secondary) and "Details" buttons.
- "Show more" pagination (no numbered pages).
- Below results: SEO block "Choosing a Card Processing Provider" and FAQ, which changes with the selected service.
- Schema: ItemList.

### 3.3 Company profile `/company/{slug}-{id}`

- Breadcrumb Home / Atlas / Name. Large logo tile. H1 name, domain link. "Connect" CTA top right.
- Sticky tab anchors: About, Focus Areas, Reviews, Supported Features, Contacts, Alternatives.
- Correction loop: "Saw an error? Suggest change · Claim profile".
- About: description plus meta sidebar (HQ country, last updated, on site since).
- Focus areas: services offered, industries served, regions covered (with map).
- Reviews (star rating, write a review). Supported features: payment methods and capability flags. Contacts (gated). Alternatives (related cards).
- Closing CTA "Ready to integrate a specific service or payment feature?".
- Title formula: `{Name}: Reviews, Payment Methods & Alternatives | PayAtlas`.
- Schema: FinancialService, BreadcrumbList.

### 3.4 Comparison `/compare/{a}-vs-{b}`

- Two logos with a "vs" badge, H1 "PayPal vs Stripe", subhead.
- Generated verdict banner: "X takes 2 of 3 categories, a broader currency mix and more payment methods". "Read summary" link.
- Tabs: Coverage, Features, Reviews, Alternatives, FAQ.
- Side-by-side columns with rating, world coverage map, feature rows.
- "Comparison Summary", "Choose a Payment Provider That Fits Your Business", alternatives grid (8 cards), FAQ.
- Schema: Organization, WebSite, BreadcrumbList, WebPage, ItemList x2, FAQPage. The richest markup on the site.
- Weakness: meta description is a copy of the title.

### 3.5 Country guide `/countries/{name}-{iso}`

Long-form, generated to a fixed skeleton:

- H1 "{Country} Payments Guide"
- H2 Market Potential (e-commerce overview, growth drivers, consumer behaviour, trends, merchant opportunity scorecard, "PayAtlas Take")
- H2 Payments Landscape (methods in use, conversion and UX patterns, fraud and chargeback risks)
- H2 PSP Landscape (market overview, PSP types, selection factors, notable PSPs)
- H2 Compliance and Regulatory (regulators and licensing)
- Share buttons, comments.
- Title: `Accepting Payments in {Country}: PSPs, Compliance & Fees`.
- Schema: Organization, BreadcrumbList, WebPage, Article.

The index `/countries` groups by 13 regions with photography cards.

### 3.6 Industry vertical and sub-industry

Two levels: `/industry-vertical/gambling-betting` (20 verticals) and
`/industry/online-casinos` (about 90). Same skeleton: Introduction, Business
Model, Market Size and Trends, Payment Methods Fit, PSP and Provider Ecosystem
(mainstream, high-risk, banks, APMs, white label), Geography Insights, Risk
Profile, Compliance (regulators, licenses table, regional differences), Red
Flags, KYB and Onboarding checklist.

Title: `Payments for {Industry}: Methods, Risks & Providers | PayAtlas`.

### 3.7 Reference entities

All use one long-form article shell with a fixed H2 skeleton per type:

| Type | Skeleton highlights | Title pattern |
|---|---|---|
| Payment method | Identity and history, geography and coverage, usage, users and segments | `{Method}: Coverage, Adoption & Payment Details` |
| Regulator | Jurisdiction, regulated entities, licenses, licensing process with timelines and costs, compliance, merchant and PSP relevance, red flags | `{Regulator}: Licensing, Oversight & Scope` |
| MCC code | Payment benchmarks, risk and compliance, onboarding checklist, regulation, network definitions | `{code} {name}` (no brand) |
| Glossary term | Core explanation, merchant relevance, industry context, comparisons, outlook, expert tips, related terms | `{term}` (no brand) |
| Currency, association | Similar shells | |

Every reference page carries share buttons and a comment form.

### 3.8 Tools and landing pages

- **Navigator** `/navigator/search`: H1 "Tell us about your search", 4 numbered steps (industry, country of incorporation, settlement currencies, processing methods), "Find providers". Schema WebApplication.
- **Assist** `/assist`: merchant concierge sales page. Problem, "for every business type", four promises, 3 steps, package card ("On Request"), case studies, FAQ, CTA "Get started".
- **Provider program** `/provider-program`: H1 "Showcase, connect, and grow with your ideal merchants", 3-step onboarding, profile showcase, pricing (Free $0 and Plus "Soon"), partner quotes, FAQ, "Get free profile" and "Contact sales".
- **Insights** `/insights/{slug}`: interactive heat maps (card share, bank transfer share, e-wallet share by country) with a 9-question FAQ. Schema Map and FAQPage. A good linkable-asset play.
- **Trust badges** `/badges`: embeddable badges for providers to put on their sites. A backlink engine.

---

## 4. Design system

| Element | Observed |
|---|---|
| Primary font | Haskoy, geometric sans, 400 and 600, self-hosted woff2, preloaded |
| Accent font | Romek, serif, regular and italic. Used for H2s and one italic accent word in the H1 |
| Type scale | Desktop H1 64, H2 48, H3 32, H4 24, H5 21. Mobile H1 40, H2 32, H3 25. Body 14, large body 18, small 12 |
| Base | White page, light grey card surfaces, 1px light borders |
| Primary action | Near-black green `#27332f` fill, white text, 8px radius, 8px 16px padding, 14px semibold |
| Brand accent | Purple scale `#26187a` to `#f3ebff`, key value `#8066ff` |
| Gradient | Purple to deep teal `#091f1f`, used on hero art and feature cards |
| Cards | 12 to 16px radius, thin border, no heavy shadow |
| Imagery | Real photography for regions, 3D style logo tiles in hero, icon set for industries |

Recurring patterns:

- Pill eyebrow above each H2 ("Atlas", "Community", "Benefits", "FAQ").
- "See all" or "View all" ghost button aligned right of the H2.
- Horizontal scroll carousels for regions and industries.
- Logo-first cards everywhere. Logos carry the visual weight.
- Floating feedback bubble bottom right, cookie banner bottom left with "Customize".
- Sticky header, mega menus on hover or click.

Overall feel: calm, airy SaaS, closer to a product than a media site. Density
rises sharply on reference pages, which are wall-of-text articles.

---

## 5. SEO

### 5.1 What they do well

- Sitemap index split per entity, every file with lastmod.
- Self-referencing canonical on every page checked.
- Unique, templated titles and descriptions per entity type, written around search intent ("Accepting Payments in Albania: PSPs, Compliance & Fees").
- JSON-LD on every template except the homepage, chosen per type (FinancialService, Article, FAQPage, WebApplication, Map, ItemList, DefinedTerm).
- Breadcrumbs with BreadcrumbList schema.
- OG image 1200x630 per page, twitter large card.
- hreflang en plus x-default (ready for localisation).
- Performance basics: font and hero image preloads with srcset, deferred non-critical CSS, modulepreload for JS.
- Massive internal linking via mega menu, footer and "Alternatives" blocks.
- Programmatic long tail: 931 MCC pages, 273 glossary terms, 319 regulators, 121 comparisons.
- Linkable assets: heat maps and trust badges.

### 5.2 Gaps and mistakes

| Issue | Impact | What we do instead |
|---|---|---|
| Filtered category URLs blocked, no static category pages | Misses "card processing providers", "crypto payment gateways", "high risk merchant account" queries | Static, indexable `/providers/{service}/` landing pages with intro, list and FAQ |
| No JSON-LD on homepage | No Organization or WebSite (SearchAction) signals | Organization + WebSite with SearchAction |
| H2 typo "Statisic", event title as H2 | Sloppy outline | Heading lint in `check.sh` |
| Compare meta description duplicates title | Lower CTR | Generated description with the verdict line |
| Glossary and MCC titles have no brand suffix, MCC title lacks intent words | Weaker CTR | `MCC {code}: {name}, Risk & Payment Guide · [DIRECTORY NAME]` |
| Numeric IDs in slugs | Less readable URLs, harder to type | Clean slugs, ID only on collision |
| Thin UGC indexed (5 discussions, 1 job, feedback posts) | Quality signal drag | noindex UGC until threshold |
| English only | Leaves non-English markets | Plan hreflang from day one |
| Reference articles appear machine generated at scale | Helpful content risk | Named author, reviewer, sources and last-reviewed date on every guide |

---

## 6. CTAs

### 6.1 Inventory by intent

| Intent | CTA text | Where |
|---|---|---|
| Merchant, high intent | Find a Provider Match · Find a Provider · Find My Partner · Help me to find the best provider | Hero, header, closing bands, benefits |
| Merchant, concierge | Get started · Get started with Assist | Assist band, Assist page |
| Merchant, per provider | Connect · Request info | Every listing row, profile header, compare page |
| Merchant, browse | Explore Atlas for free · View all · See all · Details · View profile · Read summary · Show more | Hero secondary, section headers, cards |
| Provider acquisition | Submit company · Claim profile · Get free profile · Become a partner · List your company · Contact sales | Category section, profile pages, listing promo, provider page |
| Data quality | Suggest change · Report missing info · Write a review | Profile pages |
| Community | Start Discussion · Write Article · Add Event · Post (comments) | For Authors band, reference pages |
| Retention | Newsletter signup · Share (LinkedIn, X, Facebook) | Footer band, articles |

### 6.2 Patterns

- Primary is always the dark filled button, secondary is a ghost or light grey button. Never two primaries side by side.
- Every content page ends in a commercial CTA ("Choose a Payment Provider That Fits Your Business"), so informational traffic is pushed to the Navigator or Assist.
- "Connect" opens an auth modal for logged-out users. Lead capture happens at the moment of highest intent.
- Supply-side CTAs (claim, submit) sit on demand-side pages. Every provider who finds their own profile is a sign-up prompt.

---

## 7. Criteria not in the brief that matter

| Area | Observation | Implication for us |
|---|---|---|
| Trust and provenance | "Last updated", "On site since", Verified badge, suggest-change and claim loops | Directory value is data accuracy. Show freshness on every record. |
| Neutrality | Owned by a vendor in the space, not disclosed on page | Publish ownership, ranking method and paid placement rules |
| Monetisation surfaces | Assist (paid), provider Plus tier, featured placement implied | Decide early. Pricing pages shape the IA. |
| Auth gating | Contacts and Connect behind login | Pick what is gated. Gating too much hurts SEO and trust. |
| UGC | Reviews, discussions, comments, articles, events | Needs moderation, spam controls (they use Cloudflare Turnstile) and noindex rules |
| Analytics | GA4, PostHog, cookie manager | Consent first. Plan event names for every CTA now. |
| Legal | "Main focus is the high-risk sector", "we don't guarantee they will open MID" | Disclaimer copy and terms needed before launch |
| Transparency | Roadmap, changelog, public feedback board | Cheap trust builders for an early product |
| Backlinks | Trust badges, heat maps, comparisons | Build at least one linkable asset at launch |
| Mobile | Filter rail becomes a drawer, carousels swipe | Design the listing and profile at 375px first |
| Accessibility | Heading skips, icon-only buttons | Lint headings, label icon buttons |
| Performance | Preloads, deferred CSS, webp srcset | Budget: LCP under 2.5s on listing and profile |

---

## 8. Takeaways for our build

1. Copy the model, not the look: free catalogue, paid concierge, provider tiers, programmatic reference content.
2. Win where they are blocked: indexable service category pages and country by service pages (`/providers/crypto/brazil/`).
3. Lead with trust: ownership disclosure, ranking method, data freshness, named reviewers.
4. Fix the cheap things they got wrong: homepage schema, heading hygiene, compare descriptions, clean slugs, noindex thin UGC.
5. Start with fewer, deeper templates. 17 templates cover everything PayAtlas does; the wireframe in this repo builds all 17.
