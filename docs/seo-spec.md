# SEO spec

Applies to the wireframe now and to the real build later. `[DIRECTORY NAME]` is
the brand placeholder. `{x}` marks a templated value.

## Global head

Every page carries, in this order: charset, viewport, title, meta description,
canonical (absolute, trailing slash), hreflang `en` and `x-default`, OG title,
description, image (1200x630), url, type, site_name, twitter card
`summary_large_image`, font preload, stylesheet, JSON-LD.

The wireframe sets `noindex, nofollow` via `vercel.json` header for the whole
deployment. It is an internal review site and should never be indexed.

## Titles and descriptions per template

Titles under 60 characters where possible. Descriptions 140 to 160 characters,
always containing the primary keyword and a reason to click.

| Template | Title formula | Description formula | Primary keyword pattern |
|---|---|---|---|
| Home | `[DIRECTORY NAME]: Find and Compare Payment Providers` | Compare {N} payment providers by service, country and industry. Free to search, with match help when you need it. | payment provider directory |
| Listing | `Payment Providers Directory: Compare {N} PSPs · [DIRECTORY NAME]` | Filter {N} PSPs by service, country, industry and payment method. See coverage, reviews and alternatives. | payment service providers list |
| Service category | `Best {Service} Providers in {Year} · [DIRECTORY NAME]` | Compare {count} {service} providers. Coverage, pricing model, supported industries and real reviews, updated {month}. | {service} providers |
| Provider profile | `{Name} Review: Services, Coverage & Alternatives` | {Name} offers {top services} in {region}. See supported payment methods, industries, reviews and {N} alternatives. | {name} review |
| Compare pair | `{A} vs {B}: Fees, Coverage & Features Compared` | Verdict line. Example: "{A} covers more countries, {B} supports more payment methods. Full side-by-side comparison." | {a} vs {b} |
| Compare index | `Compare Payment Providers Side by Side · [DIRECTORY NAME]` | | payment provider comparison |
| Match | `Find a Payment Provider in 4 Steps · [DIRECTORY NAME]` | | find payment provider |
| Assist | `Payment Provider Matching Service · [DIRECTORY NAME]` | | psp matching service |
| For providers | `List Your Payment Company · [DIRECTORY NAME]` | | list payment company |
| Country guide | `Accepting Payments in {Country}: Methods, PSPs & Rules` | | accept payments in {country} |
| Industry | `Payment Processing for {Industry}: Risks & Providers` | | {industry} payment processing |
| Payment method | `{Method}: How It Works, Coverage & Providers` | | {method} payment provider |
| Glossary | `What Is {Term}? Payments Glossary · [DIRECTORY NAME]` | | what is {term} |
| MCC | `MCC {code}: {Name}, Risk Level & Requirements` | | mcc {code} |
| Journal | `{Headline}` | | per article |

## Heading rules

- Exactly one H1 per page, matching search intent, not a slogan.
- No skipped levels (H2 to H4 is a fail).
- H2s on programmatic pages follow the fixed skeleton for that template, so pages are consistent and easy to audit.
- No headings used for styling. Event titles, card names and stat numbers are not headings unless they head a section.

## Structured data per template

| Template | JSON-LD types |
|---|---|
| Home | Organization, WebSite with SearchAction |
| Listing | CollectionPage, ItemList, BreadcrumbList |
| Service category | CollectionPage, ItemList, FAQPage, BreadcrumbList |
| Provider profile | Organization (the provider) with aggregateRating only when 3+ real reviews, BreadcrumbList |
| Compare pair | WebPage, ItemList (the two providers), FAQPage, BreadcrumbList |
| Match | WebApplication, BreadcrumbList |
| Assist | Service, FAQPage |
| For providers | Service with Offer per tier, FAQPage |
| Country, industry, payment method, MCC | Article with author, reviewedBy, dateModified, BreadcrumbList |
| Glossary | DefinedTerm inside DefinedTermSet, BreadcrumbList |
| Journal | Article (author Person), BreadcrumbList |
| Events index | ItemList of Event |

FAQ copy on the page and in FAQPage JSON-LD come from the same source. They must
match word for word.

## Content quality signals (E-E-A-T)

Every guide-type page shows: author, reviewer, last reviewed date, sources list.
Every provider profile shows: last verified date, data source (provider
submitted, editor verified, or public sources), and a "Suggest a correction"
link. A public "How we rank" page explains ordering and any paid placement.

## robots.txt (real build)

```
User-agent: *
Disallow: /account/
Disallow: /*?q=
Disallow: /*?sort=
Allow: /providers/
Sitemap: https://{domain}/sitemap.xml
```

Unlike PayAtlas, service categories are real paths, not query strings, so they
stay crawlable while filter combinations stay blocked.

## Internal linking

See `sitemap.md`, section "Internal linking rules". Mega menu plus footer give
every page a path to every hub within two clicks.

## Performance budget

LCP under 2.5s and CLS under 0.1 on listing and profile at 4G mobile. One web
font family plus one accent face, preloaded. No layout shift from the cookie
banner (overlay, not push).
