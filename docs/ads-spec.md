# Ads spec (v2)

Version 2 adds banner and margin advertising to the directory. Source of truth
for slots, page plan and policy is `data/ads.json`; this document explains the
reasoning. `scripts/render.py` refuses to build a page whose ads do not match
the plan, and `scripts/check.sh` section 6 re-checks the rendered HTML.

## Model

Direct-sold sponsors only. Payment companies buy slots by service category,
country, industry or run of site, on monthly terms. No ad network, no
programmatic backfill, no third-party ad scripts.

Why direct-sold: the audience is merchants choosing a payment provider, which is
worth far more to PSPs than to a generic network buyer. Network ads also bring
random creative (loans, crypto casinos) next to compliance content, which costs
more trust than it earns. Benchmark note: no display ads were seen on the 14
PayAtlas templates reviewed; it monetises through Assist and provider tiers.
Ads are a revenue line we would add on top.

## Slots

| Slot | Desktop | Mobile | Where | Auto-placed |
|---|---|---|---|---|
| Top banner (leaderboard) | 728 × 90 | 320 × 50 | Band under the header, above breadcrumbs | yes |
| Margin skyscrapers | 160 × 600, pair | not shown | Fixed in the left and right page margins, outside the 1200px column, screens 1560px and wider | yes |
| Billboard | 970 × 250 | 300 × 250 | Between sections on home and country index | macro |
| In-article banner | 728 × 90 | 300 × 250 | Between H2 sections on guides, compare, MCC, journal, events | macro |
| Sidebar box | 300 × 250 | 300 × 250 | Right aside, below page facts | macro |
| Sponsored listing | native row | native row | After the third organic result on listing and category pages | macro |
| Mobile anchor | not shown | 320 × 50 | Fixed to the bottom on phones, dismissible for the session | yes |

Responsive slots use CSS container queries, so each slot picks its size from
the width it actually has. A 728 banner inside a 700px article column
automatically serves the 300 × 250 version instead of overflowing.

Margin ads only exist at 1560px and wider because they must sit outside the
content column (1200 + 2 × 180). Below that, margin inventory is simply not
shown. Do not shrink the content column to make room: it would change the
layout for every visitor to serve a minority of screens.

## Page plan

| Page | Banner | Margins | Billboard | In-article | Sidebar | Sponsored row | Anchor |
|---|---|---|---|---|---|---|---|
| Home | ✓ | ✓ | ✓ | | | | ✓ |
| Directory listing | ✓ | ✓ | | | | ✓ | ✓ |
| Service category | ✓ | ✓ | | | ✓ | ✓ | ✓ |
| Provider profile | ✓ | ✓ | | | ✓ | | ✓ |
| Compare index | ✓ | ✓ | | | | | ✓ |
| Compare pair | ✓ | ✓ | | ✓ | | | ✓ |
| Country index | ✓ | ✓ | ✓ | | | | ✓ |
| Country guide | ✓ | ✓ | | ✓ | | | ✓ |
| Industry guide | ✓ | ✓ | | ✓ | | | ✓ |
| Payment method | ✓ | ✓ | | ✓ | ✓ | | ✓ |
| Glossary | ✓ | ✓ | | | ✓ | | ✓ |
| MCC code | ✓ | ✓ | | ✓ | | | ✓ |
| Journal | ✓ | ✓ | | ✓ | | | ✓ |
| Events | ✓ | ✓ | | ✓ | | | ✓ |
| Match, Assist, For providers, Advertise, Hub, 404 | ad-free | | | | | | |

Maximum 6 units per page (the margin pair counts as one). The busiest page,
the service category landing, carries 5.

## Policy

1. Every ad has a visible "Sponsored" label and its own bordered container.
2. Ad links use `rel="sponsored nofollow"`.
3. Ads never change ranking, verdicts, ratings or default sort. "How we rank" says so.
4. No ads inside comparison tables, the match tool, forms or search ordering.
5. Conversion pages are ad-free.
6. Advertisers must hold the licences their product needs; unlicensed or prohibited services are declined.
7. Every slot reserves its height before load. No layout shift.
8. Paid-tier verified providers can remove competitor sidebar ads from their own profile.

## Featured vs sponsored

These are different products and must stay visibly different:

- **Featured** (provider tier): one labelled row at the top of a listing, bought through the provider program. It is a profile, with real ratings.
- **Sponsored listing** (ad): a dashed, grey row after the third organic result, bought through advertising. No rating unless the sponsor has real reviews, links with rel=sponsored.

## SEO and performance impact

- Ads add no structured data and no headings to the page outline.
- Reserved heights keep CLS at zero from ads. Check with Lighthouse on listing and profile.
- In the real build, ad creatives load lazily below the fold and from our own domain or the advertiser's, never via a third-party ad server that blocks rendering.
- Google treats heavy above-the-fold ads as a page experience problem. Above the fold we allow one banner only.

## Analytics

Each ad carries `data-cta="ad-{slot}"` (margins add `-left` or `-right`). Track
impressions with an IntersectionObserver at 50 percent visible for 1 second,
and clicks per slot, per page, per advertiser. Advertisers get a monthly report.

## Open decisions

- Prices per slot (`[PRICE]` everywhere).
- Whether competitors can buy ads on each other's profiles at all, or only category sponsors.
- Minimum traffic before ads launch. Selling empty audience numbers damages the provider relationships the directory depends on.
