# Prompt 03b: Ad inventory (v2)

Adds banner, margin, in-content and sponsored listing ads to the built
templates. Run after prompt 03 is approved and before the SEO pass.

---

```
Add direct-sold advertising to DIRECTORY_NAME's wireframe. Read CLAUDE.md,
docs/ads-spec.md (create it from this prompt if missing), scripts/render.py and
assets/base.css first.

## Model
Direct-sold sponsors only. Payment companies buy slots by service category,
country, industry or run of site. No ad network, no third-party scripts.

## 1. data/ads.json (single source of truth)
Define:
- label: "Sponsored"
- max_per_page: 6 (the margin pair counts as one)
- ad_free_routes: match, assist, for-providers, advertise, hub, 404
- slots, each with name, desktop size, mobile size, placement, targeting, price
  ("[PRICE] per month"), and auto: true for slots the renderer places itself:
  leaderboard 728x90 / 320x50 (auto, band under header)
  margin 160x600 pair, desktop only (auto, fixed in page margins)
  billboard 970x250 / 300x250
  inarticle 728x90 / 300x250
  rail 300x250
  native (sponsored listing row)
  anchor 320x50, mobile only (auto, dismissible)
- policy: the 8 rules in docs/ads-spec.md
- page_plan: route to list of slots, for every ad-eligible route

## 2. Renderer
In scripts/render.py:
- {{ad:<slot>}} macro renders a slot. Every ad is an
  <aside class="ad ad--<slot>" data-ad-slot="<slot>" aria-label="Advertisement">
  with a visible label, a placeholder creative showing the size(s) and
  "[ADVERTISER CREATIVE]", links with rel="sponsored nofollow", and an
  "Advertise here" link to /advertise/#slot-<slot> (not on margin or anchor).
- The sponsored listing uses the organic row-card layout but no heading
  element, a dashed border, the label as a pill, and no rating.
- Auto-place leaderboard (top of <main>), margin pair and anchor (after the
  footer) from page_plan. Add class has-anchor to <body> when the page has an
  anchor.
- Track placed slots per page. Fail the build if placed slots do not equal
  the page_plan, if an ad-free route has any ad, or if the count exceeds
  max_per_page.
- {{provider_rows:a-b}} renders a slice so a sponsored row can sit after row 3.
- Macros {{ad_inventory}}, {{ad_policy}}, {{ad_page_plan}} render tables from
  ads.json for the advertise page and hub.
- Footer Tools column gets "Advertise". Wireframe toggles get "Hide ads".

## 3. CSS (assets/base.css)
- .ad uses container-type: inline-size. Default to the mobile size; switch to
  728x90 at @container (min-width: 728px) and 970x250 at 970px. A slot must
  never overflow its column.
- Creatives have fixed height so nothing shifts on load.
- Margins: position fixed, top below the header, left and right at
  calc(50% - 600px - 180px), display only at min-width 1560px.
- Anchor: fixed bottom, phones only, close button as a tab above the bar so the
  creative keeps its full 320px. Push cookie banner and wireframe toggles up
  when the anchor is present.
- body.hide-ads hides every ad (for side by side review).

## 4. JS (assets/site.js)
- data-ads-toggle: show or hide all ads, remembered in localStorage.
- data-ad-close: hides the anchor for the session (sessionStorage), removes
  has-anchor from <body>. Wrap storage calls in try/catch.

## 5. Placement per page
Insert macros where docs/ads-spec.md's page plan says. Rules:
- Billboard only on home (after the first two browse sections) and country index.
- In-article after the second H2 of a guide, never inside a table, form,
  comparison block or stepper.
- Sidebar box at the bottom of the aside, below page facts and correction links.
- Sponsored row after the third organic row, never first.
- Add a .wf-note wherever a placement decision is not obvious (profile ads,
  compare ads, featured vs sponsored).

## 6. New page: /advertise/ (ad-free)
Hero (H1, primary "Request the media kit", ghost "See placements", page diagram
placeholder), audience stats as [N] with a note never to estimate them,
inventory table {{ad_inventory}}, targeting cards (service, country,
industry), page plan {{ad_page_plan}}, public ad policy {{ad_policy}}, media
kit request form. JSON-LD: Service.

## 7. Checks
Add check.sh section 6 that parses rendered HTML: every ad labelled, every ad
link rel="sponsored nofollow", no ad inside <table> or <form>, rendered slots
equal page_plan, ad-free routes clean, max per page respected.

Verify in the browser at 375, 1024 and 1680px: no horizontal scroll, slot
sizes as expected, margins visible only at 1680, anchor close and Hide ads work.
Then python3 scripts/render.py and ./scripts/check.sh.
```
