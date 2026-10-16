#!/usr/bin/env python3
"""Render the wireframe into site/.

Each file in src/pages/ is a page body that starts with a meta block:

    <!--meta
    {"route": "/providers/", "title": "...", "description": "...",
     "crumbs": [["Home", "/"], ["Providers", null]], "jsonld": [...], "faq": "category"}
    -->

The renderer wraps the body in the shared head, header, footer, cookie banner
and auth modal, expands {{macros}} from data/*.json and writes
site/<route>/index.html. FAQ markup and FAQPage JSON-LD come from the same
data/faqs.json entry so they cannot drift.

This is a local dev tool. Its output in site/ is committed and Vercel serves
it as static files, with no build step on Vercel.

    python3 scripts/render.py
"""
import hashlib
import html
import os
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"
OUT = Path(os.environ.get("WF_OUT", ROOT / "site"))
BASE_URL = "https://example.com"  # placeholder origin for canonicals in the wireframe
BRAND = "[DIRECTORY NAME]"

TAX = json.loads((ROOT / "data" / "taxonomy.json").read_text())
PROV = json.loads((ROOT / "data" / "providers.json").read_text())["providers"]
FAQS = json.loads((ROOT / "data" / "faqs.json").read_text())
ADS = json.loads((ROOT / "data" / "ads.json").read_text())
PLACED = []  # slots placed on the page currently being rendered

VERSIONS = json.loads((ROOT / "data" / "versions.json").read_text())
# A branch is v2 if it carries the ad inventory. No per-branch config, so merges stay clean.
VERSION = "v2" if (ROOT / "data" / "ads.json").exists() else "v1"

e = html.escape


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def service_href(name):
    """Only card processing is built. Other services point at that sample with
    the intended slug in the query string, so reviewers see the real URL plan."""
    slug = slugify(name)
    if slug == "card-processing":
        return "/providers/card-processing/"
    return f"/providers/card-processing/?s={slug}"


def category_href(cat):
    return f"/providers/?category={cat['slug']}"


def provider_href(p):
    return "/provider/provider-alpha/" if p["slug"] == "provider-alpha" else f"/provider/provider-alpha/?p={p['slug']}"


# ---------- shared chrome ----------

def version_bar(route):
    links = "".join(
        f'<a class="version-switch__opt{" is-current" if v["id"] == VERSION else ""}" '
        + (f'href="{route}" aria-current="page"' if v["id"] == VERSION else f'href="/hub/#versions" data-version="{v["id"]}"')
        + f'><strong>{e(v["label"])}</strong> <span>{e(v["detail"])}</span></a>'
        for v in VERSIONS["versions"]
    )
    cfg = e(json.dumps({"current": VERSION, **{k: VERSIONS[k] for k in ("versions", "only_in")}}))
    return f"""<nav class="version-bar" aria-label="Wireframe version" data-versions="{cfg}">
  <div class="container version-bar__inner">
    <span class="version-bar__label">Wireframe</span>
    <div class="version-switch">{links}</div>
    <a class="version-bar__hub" href="/hub/">All templates</a>
  </div>
</nav>"""


def header():
    cats = TAX["categories"]
    cols = "".join(
        f'<div><p class="mega__h">{e(c["name"])}</p><ul>'
        + "".join(f'<li><a href="{service_href(s)}">{e(s)}</a></li>' for s in c["services"][:6])
        + f'<li><a class="link" href="{category_href(c)}">All {e(c["name"].lower())}</a></li></ul></div>'
        for c in cats[:3]
    )
    feature = (
        '<div class="mega__feature"><p class="mega__h">More categories</p><ul>'
        + "".join(f'<li><a href="{category_href(c)}">{e(c["name"])}</a></li>' for c in cats[3:])
        + '</ul><p class="small muted" style="margin-top:16px">Not sure which service you need?</p>'
        '<a class="btn btn--primary btn--sm" href="/match/" data-cta="mega-match">Use the match tool</a>'
        '<p style="margin:12px 0 0"><a class="link small" href="/providers/">Browse all providers</a></p></div>'
    )
    guides = "".join(
        f'<a class="mega__link" href="{g["href"]}">{e(g["name"])}<span>{e(g["blurb"])}</span></a>'
        for g in TAX["guides"]
    )
    community = (
        '<a class="mega__link" href="/journal/sample-guide/">Journal<span>Guides, analysis and news</span></a>'
        '<a class="mega__link" href="/events/">Events<span>Payments conferences worldwide</span></a>'
        '<a class="mega__link" href="/events/?wf=discussions">Discussions<span>Phase 2, noindex until active</span></a>'
        '<a class="mega__link" href="/events/?wf=jobs">Jobs<span>Phase 2</span></a>'
    )
    drawer_groups = "".join(
        f'<details><summary>{e(c["name"])}</summary>'
        + "".join(f'<a href="{service_href(s)}">{e(s)}</a>' for s in c["services"])
        + "</details>"
        for c in cats
    )
    return f"""
<header class="site-header">
  <div class="container site-header__bar">
    <a class="brand" href="/"><span class="brand__mark" aria-hidden="true"></span><span class="brand__name">{BRAND}</span></a>
    <nav class="nav" aria-label="Primary">
      <div class="nav__item"><button class="nav__link" aria-haspopup="true" aria-expanded="false" data-mega="mega-providers">Providers</button>
        <div class="mega" id="mega-providers">{cols}{feature}</div></div>
      <div class="nav__item"><a class="nav__link" href="/compare/">Compare</a></div>
      <div class="nav__item"><button class="nav__link" aria-haspopup="true" aria-expanded="false" data-mega="mega-guides">Guides</button>
        <div class="mega mega--guides" id="mega-guides">{guides}</div></div>
      <div class="nav__item"><button class="nav__link" aria-haspopup="true" aria-expanded="false" data-mega="mega-community">Community</button>
        <div class="mega mega--community" id="mega-community">{community}</div></div>
      <div class="nav__item"><a class="nav__link" href="/for-providers/">For providers</a></div>
    </nav>
    <div class="header-actions">
      <button class="btn btn--ghost btn--sm" data-modal-open="auth" data-cta="nav-signin">Sign in</button>
      <a class="btn btn--primary btn--sm" href="/match/" data-cta="nav-find">Find a provider</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false" data-toggle="drawer"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="drawer container" id="drawer">
    {drawer_groups}
    <details><summary>Guides</summary>{"".join(f'<a href="{g["href"]}">{e(g["name"])}</a>' for g in TAX["guides"])}</details>
    <details><summary>Community</summary><a href="/journal/sample-guide/">Journal</a><a href="/events/">Events</a></details>
    <a href="/compare/" style="padding-left:0;font-weight:600">Compare</a>
    <a href="/for-providers/" style="padding-left:0;font-weight:600">For providers</a>
    <button class="btn btn--ghost btn--block" data-modal-open="auth">Sign in</button>
  </div>
</header>"""


def footer():
    cats = "".join(f'<li><a href="{category_href(c)}">{e(c["name"])}</a></li>' for c in TAX["categories"])
    guides = "".join(f'<li><a href="{g["href"]}">{e(g["name"])}</a></li>' for g in TAX["guides"])
    return f"""
<div class="container">
  <section class="newsletter" aria-labelledby="nl-h">
    <div><h2 id="nl-h" style="font-size:28px">One email a week on payments</h2><p class="muted" style="margin:0">New providers, guide updates and industry changes. No spam.</p></div>
    <form data-wf-form="stay"><label class="sr-only" for="nl-email">Work email</label><input class="input" id="nl-email" type="email" placeholder="Work email" required><button class="btn btn--primary" data-cta="newsletter">Subscribe</button>
    <p class="small" data-form-msg hidden>Wireframe: form does not submit.</p></form>
  </section>
</div>
<footer class="site-footer">
  <div class="container">
    <div class="footer-cols">
      <div class="footer-brand"><a class="brand" href="/"><span class="brand__mark" aria-hidden="true"></span>{BRAND}</a>
        <p class="muted small" style="margin-top:12px;max-width:260px">An independent directory of payment providers. [OWNERSHIP LINE, one sentence, to be confirmed].</p></div>
      <div><h3>Providers</h3><ul>{cats}</ul></div>
      <div><h3>Guides</h3><ul>{guides}</ul></div>
      <div><h3>Tools</h3><ul><li><a href="/match/">Match tool</a></li><li><a href="/compare/">Compare</a></li><li><a href="/assist/">Assist</a></li><li><a href="/for-providers/#badges">Trust badges</a></li><li><a href="/advertise/">Advertise</a></li></ul></div>
      <div><h3>Company</h3><ul><li><a href="/hub/">About</a></li><li><a href="/hub/#how-we-rank">How we rank</a></li><li><a href="/hub/#ownership">Ownership</a></li><li><a href="/hub/">Roadmap</a></li><li><a href="/hub/">Contact</a></li></ul></div>
      <div><h3>Legal</h3><ul><li><a href="/hub/">Terms</a></li><li><a href="/hub/">Privacy</a></li><li><a href="/hub/">Cookies</a></li><li><a href="/hub/">Disclaimer</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>&copy; 2026 {BRAND}. Wireframe for internal review.</span><span>LinkedIn · X · YouTube</span></div>
  </div>
</footer>
<div class="cookie" data-cookie hidden role="dialog" aria-label="Cookie preferences">
  <strong>Cookies</strong>
  <p style="margin:6px 0 0">We use essential cookies to run the site and, with your consent, analytics to improve it. <a href="/hub/">Cookie policy</a>.</p>
  <div class="cookie__actions"><button class="btn btn--primary btn--sm" data-cookie-choice="all" data-cta="cookie-accept">Accept all</button><button class="btn btn--ghost btn--sm" data-cookie-choice="essential" data-cta="cookie-reject">Essential only</button><button class="btn btn--sm" data-cookie-choice="custom" data-cta="cookie-custom">Customise</button></div>
</div>
<div class="modal" data-modal="auth" hidden>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="auth-h">
    <button class="modal__close" data-modal-close aria-label="Close">&times;</button>
    <h2 id="auth-h" style="font-size:28px">Sign in to request intros</h2>
    <p class="muted small">Browsing is free and open. An account lets you request introductions, see contacts and write reviews.</p>
    <form data-wf-form="stay"><div class="field"><label for="auth-email">Work email</label><input class="input" id="auth-email" type="email" required></div>
    <button class="btn btn--primary btn--block" data-cta="auth-continue">Continue with email</button>
    <p class="small" data-form-msg hidden>Wireframe: no account is created.</p></form>
    <p class="small muted" style="margin-top:12px">Continue with Google · Continue with LinkedIn</p>
  </div>
</div>
<div class="wf-toggle"><button class="btn btn--soft btn--sm" data-ads-toggle>Hide ads</button><button class="btn btn--soft btn--sm" data-notes-toggle>Hide notes</button></div>"""


# ---------- macros ----------

def stars(p):
    return f'<span class="stars">&#9733; {p["rating"]}</span> <span class="muted">({p["reviews"]} reviews)</span>'


def provider_rows(arg=None):
    """{{provider_rows}}, {{provider_rows:5}} (first 5) or {{provider_rows:3-8}} (slice)."""
    start, end = 0, len(PROV)
    if arg and "-" in arg:
        start, end = (int(x) for x in arg.split("-"))
    elif arg:
        end = int(arg)
    out = []
    for i, p in enumerate(PROV[start:end], start):
        featured = i == 0
        badge = '<span class="badge">Verified</span>' if p["verified"] else '<span class="badge badge--muted">Unverified</span>'
        label = '<span class="badge badge--muted">Featured</span> ' if featured else ""
        tags = "".join(f'<span class="tag">{e(s)}</span>' for s in p["services"])
        out.append(f"""<article class="row-card{' row-card--featured' if featured else ''}">
  <div class="logo-tile" aria-hidden="true">{p["initials"]}</div>
  <div><h3><a href="{provider_href(p)}">{e(p["name"])}</a></h3>
    <div class="row-card__meta">{label}{badge}{stars(p)}<span>{e(p["domain"])}</span><span>HQ {e(p["hq"])}</span></div>
    <p>{e(p["blurb"])}</p><div>{tags}</div></div>
  <div class="row-card__actions"><button class="btn btn--primary btn--sm" data-modal-open="auth" data-cta="row-intro-{p["slug"]}">Request intro</button><a class="btn btn--ghost btn--sm" href="{provider_href(p)}" data-cta="row-profile-{p["slug"]}">View profile</a></div>
</article>""")
    return "\n".join(out)


def category_cards():
    return '<div class="grid grid--3">' + "".join(
        f'<a class="card" href="{category_href(c)}"><div class="card__icon" aria-hidden="true"></div><h3>{e(c["name"])}</h3><p>{e(c["blurb"])}</p><span class="card__meta">[N] providers</span></a>'
        for c in TAX["categories"]
    ) + "</div>"


def recent_cards():
    return '<div class="grid grid--4">' + "".join(
        f'<a class="card mini" href="{provider_href(p)}"><span class="logo-tile" aria-hidden="true">{p["initials"]}</span><span><span class="mini__name">{e(p["name"])}</span><br><span class="mini__sub">{e(p["domain"])} · {e(p["hq"])}</span></span></a>'
        for p in PROV
    ) + "</div>"


def alt_cards():
    return '<div class="grid grid--4">' + "".join(
        f'<a class="card" href="{provider_href(p)}"><div class="mini"><span class="logo-tile" aria-hidden="true">{p["initials"]}</span><span class="mini__name">{e(p["name"])}</span></div><p style="margin:12px 0 0">{e(p["blurb"])}</p></a>'
        for p in PROV[1:5]
    ) + "</div>"


def platform_map():
    return '<div class="platform-map">' + "".join(
        f'<div><h3>{e(c["name"])} <span class="muted small">[N]</span></h3><ul>'
        + "".join(f'<li><a href="{service_href(s)}">{e(s)}</a></li>' for s in c["services"])
        + "</ul></div>"
        for c in TAX["categories"]
    ) + "</div>"


def region_cards():
    return '<div class="carousel">' + "".join(
        f'<a class="ph region-card" href="/countries/">{e(r)}</a>' for r in TAX["regions"]
    ) + "</div>"


def industry_cards():
    return '<div class="carousel">' + "".join(
        f'<a class="card" href="/industries/igaming/"><div class="card__icon" aria-hidden="true"></div><h3>{e(i)}</h3><p>Methods, risk profile and providers.</p></a>'
        for i in TAX["industries"]
    ) + "</div>"


def facets():
    def facet(title, items, search=False):
        s = f'<input type="search" placeholder="Search {title.lower()}" aria-label="Search {title.lower()}">' if search else ""
        return f'<div class="facet"><h3>{e(title)}</h3>{s}' + "".join(
            f'<label><input type="checkbox"> {e(x)}<span>[N]</span></label>' for x in items
        ) + "</div>"
    allserv = [s for c in TAX["categories"] for s in c["services"]][:10]
    return (
        '<h2 class="sr-only">Filters</h2>'
        + facet("Service", allserv, True)
        + facet("Region", TAX["regions"])
        + facet("Industry", TAX["industries"][:8], True)
        + facet("Payment method", TAX["payment_methods"][:8], True)
        + '<div class="facet"><h3>Data quality</h3><label><input type="checkbox"> Verified only</label><label><input type="checkbox"> Has reviews</label></div>'
    )


def faq_block(key):
    return '<div class="faq">' + "".join(
        f'<details><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>' for f in FAQS[key]
    ) + "</div>"


def cta_band():
    return """<div class="container section--tight"><div class="cta-band">
  <div><h2>Tell us what you need. We will shortlist providers that fit.</h2><p>Four questions about your business, country and methods. Free, takes two minutes.</p></div>
  <div class="cta-band__ctas"><a class="btn btn--primary btn--lg" href="/match/" data-cta="band-match">Get matched</a><a class="btn btn--ghost btn--lg" href="/assist/" data-cta="band-assist">Talk to our team</a></div>
</div></div>"""


def crumbs_html(crumbs):
    if not crumbs:
        return ""
    items = "".join(
        f'<li><a href="{h}">{e(n)}</a></li>' if h else f'<li aria-current="page">{e(n)}</li>' for n, h in crumbs
    )
    return f'<nav aria-label="Breadcrumb" class="container"><ol class="crumbs">{items}</ol></nav>'


MACROS = {
    "provider_rows": lambda arg: provider_rows(arg),
    "ad": lambda arg: ad_slot(arg),
    "ad_inventory": lambda arg: ad_inventory(),
    "ad_policy": lambda arg: ad_policy(),
    "ad_page_plan": lambda arg: ad_page_plan(),
    "category_cards": lambda arg: category_cards(),
    "recent_cards": lambda arg: recent_cards(),
    "alt_cards": lambda arg: alt_cards(),
    "platform_map": lambda arg: platform_map(),
    "region_cards": lambda arg: region_cards(),
    "industry_cards": lambda arg: industry_cards(),
    "facets": lambda arg: facets(),
    "faq": lambda arg: faq_block(arg),
    "cta_band": lambda arg: cta_band(),
}


def expand(body, meta):
    body = body.replace("{{crumbs}}", crumbs_html(meta.get("crumbs")))

    def sub(m):
        name, _, arg = m.group(1).partition(":")
        if name not in MACROS:
            raise SystemExit(f"Unknown macro {{{{{name}}}}} in {meta['route']}")
        return MACROS[name](arg or None)

    return re.sub(r"\{\{([a-z_]+(?::[a-z0-9_-]+)?)\}\}", sub, body)


# ---------- ads (v2) ----------

def size_label(sz):
    return sz.replace("x", " × ") if sz and sz != "native" else ""


def ad_slot(slot_id, side=None):
    if slot_id not in ADS["slots"]:
        raise SystemExit(f"Unknown ad slot {slot_id}")
    PLACED.append(slot_id)
    slot = ADS["slots"][slot_id]
    label = e(ADS["label"])
    href = f"/advertise/#slot-{slot_id}"
    if slot_id == "native":
        return f"""<aside class="ad ad--native row-card" data-ad-slot="native" aria-label="Advertisement">
  <div class="logo-tile" aria-hidden="true">AD</div>
  <div><p class="row-card__title"><a href="{href}" rel="sponsored nofollow">[SPONSOR NAME]</a></p>
    <div class="row-card__meta"><span class="ad__label">{label}</span><span>[sponsor-domain.example]</span></div>
    <p>[Sponsor line, max 140 characters. Same fields as an organic row, no rating unless the sponsor has real reviews.]</p></div>
  <div class="row-card__actions"><a class="btn btn--ghost btn--sm" href="{href}" rel="sponsored nofollow" data-cta="ad-native">Visit site</a></div>
</aside>"""
    d, m = size_label(slot["desktop"]), size_label(slot["mobile"])
    sizes = (f'<span class="ad__size ad__size--d">{d}</span>' if d else "") + (f'<span class="ad__size ad__size--m">{m}</span>' if m else "")
    extra = f" ad--{side}" if side else ""
    close = '<button class="ad__close" data-ad-close aria-label="Close ad">&times;</button>' if slot_id == "anchor" else ""
    more = "" if slot_id in ("anchor", "margin") else f'<a class="ad__more" href="/advertise/#slot-{slot_id}">Advertise here</a>'
    return f"""<aside class="ad ad--{slot_id}{extra}" data-ad-slot="{slot_id}" aria-label="Advertisement">
  <span class="ad__label">{label}</span>{close}
  <a class="ad__creative" href="{href}" rel="sponsored nofollow" data-cta="ad-{slot_id}{'-' + side if side else ''}">{sizes}<span class="ad__adv">[ADVERTISER CREATIVE]</span><span class="ad__name">{e(slot["name"])}</span></a>
  {more}
</aside>"""


def ad_inventory():
    rows = "".join(
        f'<tr id="slot-{k}"><td><strong>{e(v["name"])}</strong></td><td>{size_label(v["desktop"]) or "Not shown"}</td><td>{size_label(v["mobile"]) or ("Native" if v["mobile"] == "native" else "Not shown")}</td><td>{e(v["placement"])}</td><td>{e(v["targeting"])}</td><td>{e(v["price"])}</td></tr>'
        for k, v in ADS["slots"].items()
    )
    return f'<div class="table-wrap"><table><thead><tr><th scope="col">Slot</th><th scope="col">Desktop</th><th scope="col">Mobile</th><th scope="col">Where</th><th scope="col">Targeting</th><th scope="col">Price</th></tr></thead><tbody>{rows}</tbody></table></div>'


def ad_policy():
    return '<ul class="checklist">' + "".join(f"<li>{e(x)}</li>" for x in ADS["policy"]) + "</ul>"


def ad_page_plan():
    slots = list(ADS["slots"])
    head = "".join(f'<th scope="col">{e(ADS["slots"][k]["name"])}</th>' for k in slots)
    rows = "".join(
        f'<tr><td><a class="link" href="{r}">{r}</a></td>' + "".join(f'<td>{"&#10003;" if k in plan else ""}</td>' for k in slots) + "</tr>"
        for r, plan in ADS["page_plan"].items()
    )
    free = "".join(f'<tr><td>{r}</td><td colspan="{len(slots)}" class="muted">Ad-free</td></tr>' for r in ADS["ad_free_routes"])
    return f'<div class="table-wrap"><table><thead><tr><th scope="col">Page</th>{head}</tr></thead><tbody>{rows}{free}</tbody></table></div>'


def auto_ads(route, where):
    plan = ADS["page_plan"].get(route, [])
    if where == "top" and "leaderboard" in plan:
        return f'<div class="ad-band"><div class="container">{ad_slot("leaderboard")}</div></div>'
    if where == "bottom":
        out = ""
        if "margin" in plan:
            out += ad_slot("margin", "left")
            PLACED.pop()  # the pair counts as one slot
            out += ad_slot("margin", "right")
        if "anchor" in plan:
            out += ad_slot("anchor")
        return out
    return ""


def check_ads(route):
    plan = ADS["page_plan"].get(route, [])
    placed = list(PLACED)
    if route in ADS["ad_free_routes"] and placed:
        raise SystemExit(f"{route} is ad-free but has ads: {placed}")
    if sorted(set(placed)) != sorted(plan) or len(placed) != len(set(placed)):
        raise SystemExit(f"{route}: ads placed {placed} do not match page_plan {plan}")
    if len(placed) > ADS["max_per_page"]:
        raise SystemExit(f"{route}: {len(placed)} ads exceeds max_per_page {ADS['max_per_page']}")


# ---------- head ----------

def jsonld(meta):
    blocks = list(meta.get("jsonld", []))
    url = BASE_URL + meta["route"]
    if meta.get("crumbs"):
        blocks.append({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE_URL + (h or meta["route"])}
                for i, (n, h) in enumerate(meta["crumbs"])
            ],
        })
    if meta.get("faq"):
        blocks.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in FAQS[meta["faq"]]
            ],
        })
    for b in blocks:
        b.setdefault("@context", "https://schema.org")
        if b.get("url") == "{url}":
            b["url"] = url
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks
    )


def ver(name):
    return hashlib.sha1((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]


def page(meta, body):
    url = BASE_URL + meta["route"]
    top, bottom = auto_ads(meta["route"], "top"), auto_ads(meta["route"], "bottom")
    has_anchor = "anchor" in ADS["page_plan"].get(meta["route"], [])
    title, desc = e(meta["title"]), e(meta["description"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}/og/{slugify(meta['route']) or 'home'}.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="/assets/tokens.css?v={ver('tokens.css')}">
<link rel="stylesheet" href="/assets/base.css?v={ver('base.css')}">
{jsonld(meta)}
</head>
<body{' class="has-anchor"' if has_anchor else ""}>
<a class="sr-only" href="#main">Skip to content</a>
<div class="top-stack">
{version_bar(meta["route"] if meta["route"] != "/404/" else "/404.html")}
{header()}
</div>
<main id="main">
{top}
{body}
</main>
{footer()}
{bottom}
<script src="/assets/site.js?v={ver('site.js')}" defer></script>
</body>
</html>
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    count = 0
    for src in sorted(SRC.glob("*.html")):
        raw = src.read_text()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
        if not m:
            raise SystemExit(f"{src.name}: missing meta block")
        meta = json.loads(m.group(1))
        PLACED.clear()
        body = expand(raw[m.end():], meta)
        if meta.get("band", True):
            body += "\n" + cta_band()
        route = meta["route"]
        dest = OUT / "404.html" if route == "/404/" else OUT / route.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        html_out = page(meta, body)
        check_ads(route)
        dest.write_text(html_out)
        count += 1
    print(f"Rendered {count} pages into site/")


if __name__ == "__main__":
    main()
