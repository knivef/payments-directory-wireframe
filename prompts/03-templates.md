# Prompt 03: Page templates

Builds the 17 templates plus hub and 404. Run the shared instructions once,
then each template block. You can run template blocks one at a time and review
each before the next.

---

## Shared instructions (paste first)

```
Build page templates for DIRECTORY_NAME. Read CLAUDE.md, docs/sitemap.md,
docs/cta-map.md, docs/seo-spec.md, data/taxonomy.json, assets/base.css and
scripts/render.py first.

How pages are made:
- Each page is one file in src/pages/. It starts with a meta block:
  <!--meta {"route": ..., "title": ..., "description": ..., "crumbs": [...],
  "jsonld": [...], "faq": "<key>", "band": true|false} -->
  and then the page body (no head, header or footer).
- scripts/render.py wraps it with the shared head, header, footer, cookie
  banner and auth modal, expands macros and writes site/<route>/index.html.
- Macros: {{crumbs}}, {{provider_rows}} or {{provider_rows:N}},
  {{category_cards}}, {{recent_cards}}, {{alt_cards}}, {{platform_map}},
  {{region_cards}}, {{industry_cards}}, {{facets}}, {{faq:<key>}},
  {{cta_band}}. Add a macro to render.py rather than hand-copying repeated
  markup into several pages.
- FAQ content lives only in data/faqs.json. {{faq:key}} renders it on the page
  and "faq": "key" in meta renders the matching FAQPage JSON-LD. Never type an
  FAQ answer into a page.
- Sample provider records live in data/providers.json. Use generic fictional
  names (Provider Alpha, Provider Beta). Never use a real company as a sample
  provider.
- Links to entities that are not built point at that template's sample page,
  with the intended slug in a query string, for example
  /providers/card-processing/?s=fraud-prevention. Reviewers see the real URL plan
  and nothing 404s.

Rules for every template:
- Exactly one H1. No skipped heading levels. If a block needs a heading for
  structure but not visually, use <h2 class="sr-only">.
- Every CTA gets a unique data-cta value from docs/cta-map.md.
- Primary CTA uses .btn--primary, secondary .btn--ghost. Never two primaries
  side by side.
- Any number, quote, customer name, price, licence or date we have not verified
  is a literal [BRACKETED PLACEHOLDER]. Section copy we have not written is a
  bracket describing what goes there and its length, for example
  "[Market overview, 150 to 200 words.]"
- Where we deliberately differ from the benchmark, add a .wf-note:
  "<b>Topic.</b> They do X. We do Y because Z."
- Mobile first. Test at 375px: no horizontal scroll.

After all templates: python3 scripts/render.py, then ./scripts/check.sh.
```

---

## Template blocks

Each block lists purpose, section order, CTAs, schema. Paste one at a time
after the shared instructions.

### T1. Home `/`

```
Template: Home. Purpose: route every visitor type (merchant browsing, merchant
in a hurry, provider) to the right next page within one scroll.
Sections in order:
1. Hero, two column: pill linking a new feature, H1 stating the job with one
   serif italic accent word, one-line subhead, search bar, primary CTA "Find a
   provider match" to /match/, secondary "Browse the directory". Right: product
   collage placeholder.
2. Stats strip (sr-only H2): providers with "+N this month", methods,
   countries, guides. All [N].
3. Browse by category: section head with "Submit your company" ghost button,
   {{category_cards}}.
4. Recently added: {{recent_cards}}, "View all".
5. Guides: {{region_cards}} carousel, then industries {{industry_cards}}.
6. How it works: tabs For merchants / For providers, 6 steps each.
7. Benefits split: merchants (primary CTA) and providers (ghost CTA).
8. Proof: placeholders only, with a note that the section is deleted unless
   real proof exists.
9. Journal (3 cards) and upcoming events (2 rows).
10. FAQ {{faq:home}} including ownership and "no guarantee" answers.
11. Platform map {{platform_map}}.
Then the default CTA band.
JSON-LD: Organization, WebSite with SearchAction, FAQPage via meta "faq".
```

### T2. Directory listing `/providers/`

```
Template: Directory listing. Purpose: filterable list of every provider.
Breadcrumb. Section head: H1 "Payment providers directory", "[N] providers ·
updated [DATE]", and a provider promo card on the right ("Are you a
provider?"). Two column: filter rail {{facets}} (Filters toggle on mobile) and
results: sr-only H2, result count, sort select (Most complete, Highest rated,
Newest, A to Z), a note explaining default order and labelled featured rows,
{{provider_rows}}, "Show more" plus crawlable ?page=2 links.
CTAs per row: "Request intro" (opens auth modal), "View profile".
JSON-LD: CollectionPage, ItemList, BreadcrumbList.
```

### T3. Service category landing `/providers/{service}/`

```
Template: Service category, sample card processing. This is our main SEO
advantage over the benchmark, whose equivalent is a blocked query string.
Breadcrumb Home / Providers / Category / Service. Pill with parent category,
H1 "{Service} providers", subhead with [N], primary "Get matched for
{service}", secondary "Compare top providers", note explaining the SEO
rationale and the phase 2 service by country rule.
Filter rail plus top 5 {{provider_rows:5}} and "See all [N]".
Below: two column buyer guide (H2 "How to choose a {service} provider" with
H3s on pricing models, coverage, industry fit, a "questions to ask" table, then
{{faq:category}}) and an aside with related services, popular comparisons and
glossary links.
JSON-LD: CollectionPage, ItemList, FAQPage, BreadcrumbList.
```

### T4. Provider profile `/provider/{slug}/`

```
Template: Provider profile. Purpose: everything a merchant needs to shortlist
or reject this provider, with the source of every fact visible.
Breadcrumb. Head: 88px logo tile, H1 name, verified badge, rating, domain, HQ;
primary "Request intro" (auth modal), ghost "Compare".
Sticky anchor tabs: About, Services, Coverage, Payment methods, Reviews,
Contacts, Alternatives.
Main column sections (each an H2 block): About with media placeholder;
Services offered and Industries served as linked tags; Coverage map
placeholder with regions and settlement currencies; Payment methods and
features table with a Source column (provider submitted, editor verified,
public sources, not confirmed); Reviews with summary, one review with provider
reply, "Write a review" (auth); Contacts blurred behind "Sign in to view";
Alternatives {{alt_cards}}.
Sticky aside: key facts (HQ, founded, licences, last verified, listed since),
then "Suggest a correction" and "Claim this profile".
JSON-LD: Organization for the provider (aggregateRating only with 3+ real
reviews), BreadcrumbList.
```

### T5. Compare index `/compare/`

```
Template: Compare index. Centred hero, H1, two provider inputs with VS badge
and "Compare" submit (wireframe navigates to the sample pair). H2 "Popular
comparisons" with 3 pair cards. Note on pair publishing rules.
JSON-LD: CollectionPage, BreadcrumbList.
```

### T6. Compare pair `/compare/{a}-vs-{b}/`

```
Template: Compare pair. Centred: two logo tiles with VS badge, H1 "A vs B",
subhead. Verdict banner, "Short answer" in one or two sentences that is also
the meta description, with "Read the summary". Sticky anchor tabs: Coverage,
Features, Reviews, Summary, Alternatives, FAQ.
Sections: Coverage table plus two map placeholders; Features table; Reviews
side by side; Summary as two "Choose A if / Choose B if" cards, each with its
own "Request intro" CTA; Alternatives {{alt_cards}}; FAQ {{faq:compare}}.
House rule: at least one table row where each provider wins or ties.
JSON-LD: WebPage, ItemList of the two, FAQPage, BreadcrumbList.
```

### T7. Match tool `/match/`

```
Template: Match tool (no CTA band). Narrow column. H1 "Tell us about your
business", promise of no sign up. data-stepper form with a 4 segment progress
bar and 4 fieldsets: (1) what you sell, radio chips from industries;
(2) country of incorporation select and customer markets input;
(3) settlement currencies, checkbox chips including stablecoins;
(4) payment methods chips and an optional monthly volume band.
Back, Next and an always-visible primary "Find providers".
Inline CTA box "Prefer a human?" to /assist/. Note: results show without sign
up, results URLs noindex.
JSON-LD: WebApplication (free Offer), BreadcrumbList.
```

### T8. Assist `/assist/`

```
Template: Assist concierge landing (no CTA band). Hero: pill, H1 with serif
accent word, subhead aimed at merchants who have been declined, primary "Book a
call" (anchors to the form), ghost "See how it works". Three steps. Four
"what is included" cards. Package price card with [PRICE] and placeholder
inclusions. Note: we never promise approval. FAQ {{faq:assist}} including
pricing and commission disclosure placeholders. Booking form: name, work email,
website, needs.
JSON-LD: Service, FAQPage.
```

### T9. Provider program `/for-providers/`

```
Template: Provider program (no CTA band). Hero with primary "Create free
profile", ghost "Talk to sales". Three steps (claim, complete, verify). Pricing:
Free $0 card and Plus [PRICE] card; featured placements always labelled. Note
that the paid tier must be decided before build. Trust badges section with
preview placeholder (backlink engine). FAQ {{faq:providers}}. Sales form.
JSON-LD: Service with an Offer per tier, FAQPage.
```

### T10. Country index `/countries/`

```
Template: Country index. H1, subhead, country search. H2 "By region" with
{{region_cards}}. H2 "All countries" as a link grid grouped by region (only
the sample country is built, others carry ?c=slug).
JSON-LD: CollectionPage, BreadcrumbList.
```

### T11. Country guide `/countries/{country}/`, sample Brazil

```
Template: Country guide. Two column: sticky table of contents on the left,
article on the right. Region pill, H1 "Accepting payments in {Country}",
answer-first summary, byline (author, reviewer, last reviewed, read time).
Fixed H2 skeleton: Market overview (4 stat scorecard), How customers pay
(methods table linking method pages; H3 conversion patterns), Payment
providers in {Country} ({{provider_rows:3}} and "See all"), Regulation and
licensing, Onboarding checklist, Sources. End with inline CTA "Find providers
for {Country}" and "Suggest an edit" plus share links.
JSON-LD: Article with author, reviewedBy, dateModified, about Country.
```

### T12. Industry guide `/industries/{vertical}/`, sample iGaming

```
Template: Industry guide. Same two column shell as T11; the TOC aside also
lists sub-industries as tags. Pill shows risk tier. Fixed H2 skeleton:
Business model and payment flows, Payment methods that fit (table with fit and
why), Risk profile (scorecard plus H3 red flags), Licensing by region (table),
KYB checklist, Providers that support {industry} ({{provider_rows:3}}), CTA.
JSON-LD: Article.
```

### T13. Payment method `/payment-methods/{slug}/`, sample Pix

```
Template: Payment method. Two column, article plus sticky fact box (type,
operator, launched, countries, currency, recurring) and related links. H1,
answer-first summary, byline. H2s: How it works, Coverage and adoption
(scorecard), Fees and settlement, Providers that support {method}. Note: lead
with merchant needs, push history to the fact box.
JSON-LD: Article.
```

### T14. Glossary term `/glossary/{term}/`, sample 3DS

```
Template: Glossary. Under 500 words. H1 the term, definition box first, H2 How
it works, H2 Why it matters for merchants, H2 Related terms as tags. Aside:
providers offering this as a service, with a browse link.
JSON-LD: DefinedTerm in a DefinedTermSet.
```

### T15. MCC code `/mcc/{code}/`, sample 5967

```
Template: MCC. Single column. Pill, H1 "MCC {code}: {name}", key-value box
(code, network group, risk level, common businesses). H2s: Why processors
treat it as {risk}, Onboarding requirements, Providers that accept MCC {code}.
Note: thin codes with no provider data stay noindex.
JSON-LD: Article.
```

### T16. Journal article `/journal/{slug}/`

```
Template: Journal article. Centred single column. Pill, H1, byline, lead image
placeholder, intro, section H2s, inline CTA to the match tool, author bio card.
JSON-LD: Article with Person author, datePublished, dateModified.
```

### T17. Events `/events/`

```
Template: Events. Section head with H1 and "Submit an event" ghost button.
Tabs Upcoming / Past, each panel with an sr-only H2. Event rows: date tile,
name, city, topic. Note: past events redirect to the next edition.
JSON-LD: ItemList of Event.
```

### Extra: Hub `/hub/` and 404

```
Hub (no CTA band): H1 "Wireframe hub", explanation, a link list of every
template with its URL pattern, a list of pages not built (About, How we rank,
Ownership, legal), and where the docs live. Footer company and legal links
point here.
404 (route "/404/", rendered to site/404.html, no CTA band): H1 "Page not
found", search bar, three recovery links.
```
