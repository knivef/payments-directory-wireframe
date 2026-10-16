#!/usr/bin/env bash
# Repo health check. Run from anywhere: ./scripts/check.sh
# Exits non-zero on any failure. Placeholders are reported, not failed:
# this is a wireframe and [BRACKETS] are expected until copy is approved.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
FAIL=0
pass() { printf "  ok    %s\n" "$1"; }
fail() { printf "  FAIL  %s\n" "$1"; FAIL=1; }
SRC_GLOBS=(--include="*.html" --include="*.css" --include="*.js" --include="*.md" --include="*.json" --include="*.py")

echo "Payments directory wireframe, health check"; echo

echo "1. Em dashes"
HITS=$(grep -rn $'\xe2\x80\x94' "${SRC_GLOBS[@]}" --exclude-dir=.git . 2>/dev/null || true)
[ -n "$HITS" ] && { fail "em dashes found:"; echo "$HITS" | sed 's/^/        /'; } || pass "none"
echo

echo "2. Double hyphen used as punctuation"
HITS=$(grep -rnE '[[:alnum:][:punct:]] -- [[:alnum:]]' --include="*.html" --include="*.md" --include="*.json" --exclude-dir=.git . 2>/dev/null || true)
[ -n "$HITS" ] && { fail "' -- ' found:"; echo "$HITS" | sed 's/^/        /'; } || pass "none"
echo

echo "3. site/ is up to date with src/ and data/"
TMP=$(mktemp -d)
WF_OUT="$TMP" python3 scripts/render.py >/dev/null || fail "render.py failed"
if diff -rq "$TMP" site >/dev/null 2>&1; then pass "in sync"; else fail "site/ is stale. Run: python3 scripts/render.py"; diff -rq "$TMP" site | head -5 | sed 's/^/        /'; fi
rm -rf "$TMP"
echo

echo "4. Tokens"
python3 - <<'PY'
import re, sys
ALLOW = {"font-sans","font-serif","bg","surface","surface-2","fg","muted","line","ink","ink-fg","accent","accent-soft","accent-strong","warn-soft","radius-sm","radius","radius-lg"}
bad = 0
tok = open("assets/tokens.css").read()
for name in set(re.findall(r"(?:^|[;{\s])--([a-z0-9-]+)\s*:", tok)) - ALLOW:
    print(f"  FAIL  tokens.css defines --{name}, not in allowlist"); bad = 1
base = open("assets/base.css").read()
for name in set(re.findall(r"(?:^|[;{\s])--([a-z0-9-]+)\s*:", base)):
    print(f"  FAIL  base.css defines token --{name}; tokens live in tokens.css"); bad = 1
for hexv in set(re.findall(r"#[0-9a-fA-F]{3,8}\b", base)):
    print(f"  FAIL  base.css hardcodes colour {hexv}"); bad = 1
for name in set(re.findall(r"var\(--([a-z0-9-]+)\)", base)) - ALLOW:
    print(f"  FAIL  base.css reads undefined token --{name}"); bad = 1
print("  ok    tokens allowlisted, no raw hex in base.css" if not bad else "", end="\n" if not bad else "")
sys.exit(bad)
PY
[ $? -ne 0 ] && FAIL=1
echo

echo "5. Rendered pages: headings, JSON-LD, links, instruction brackets"
python3 - <<'PY'
import json, re, sys
from pathlib import Path
from html.parser import HTMLParser
site = Path("site"); bad = 0
pages = sorted(site.rglob("*.html"))
routes = {"/" + str(p.relative_to(site)).replace("index.html", "") for p in pages}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h = []; s.ld = []; s.links = []; s._ld = False; s._sr = False
    def handle_starttag(s, t, a):
        a = dict(a)
        if re.fullmatch(r"h[1-6]", t): s.h.append(int(t[1]))
        if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s.ld.append("")
        if t == "a" and a.get("href", "").startswith("/"): s.links.append(a["href"])
    def handle_endtag(s, t):
        if t == "script": s._ld = False
    def handle_data(s, d):
        if s._ld: s.ld[-1] += d
for p in pages:
    src = p.read_text(); x = P(); x.feed(src); name = str(p.relative_to(site))
    if x.h.count(1) != 1: print(f"  FAIL  {name}: {x.h.count(1)} H1s"); bad = 1
    for a, b in zip(x.h, x.h[1:]):
        if b > a + 1: print(f"  FAIL  {name}: heading skip h{a} to h{b}"); bad = 1; break
    for blob in x.ld:
        try: json.loads(blob)
        except Exception as e: print(f"  FAIL  {name}: invalid JSON-LD {e}"); bad = 1
    for href in set(x.links):
        path = href.split("#")[0].split("?")[0]
        if path and path not in routes and path != "/404.html": print(f"  FAIL  {name}: broken link {href}"); bad = 1
    m = re.findall(r"\[(?:H[1-6]|CTA|SECTION|TODO)[^\]]*\]", src)
    if m: print(f"  FAIL  {name}: unfilled instruction brackets {m[:3]}"); bad = 1
if not bad: print(f"  ok    {len(pages)} pages: one H1 each, no skips, JSON-LD parses, links resolve")
total = sum(len(re.findall(r"\[[A-Z][^\]<]*\]", re.sub(r"<script.*?</script>", "", p.read_text(), flags=re.S))) for p in pages)
print(f"  info  {total} copy placeholders across rendered pages (expected in a wireframe)")
sys.exit(bad)
PY
[ $? -ne 0 ] && FAIL=1
echo

echo "6. Ad policy (v2)"
python3 - <<'PY'
import json, re, sys
from pathlib import Path
ads = json.loads(Path("data/ads.json").read_text())
site = Path("site"); bad = 0; total = 0
free = {r for r in ads["ad_free_routes"]}
for p in sorted(site.rglob("*.html")):
    route = "/404/" if p.name == "404.html" else "/" + str(p.relative_to(site)).replace("index.html", "")
    src = p.read_text()
    blocks = re.findall(r'<aside class="ad[ "][^>]*data-ad-slot="([a-z]+)"[^>]*>(.*?)</aside>', src, re.S)
    total += len(blocks)
    if route in free and blocks: print(f"  FAIL  {route}: ad-free page has {len(blocks)} ad(s)"); bad = 1
    for slot, inner in blocks:
        if ads["label"] not in inner: print(f"  FAIL  {route}: {slot} ad has no '{ads['label']}' label"); bad = 1
        for a in re.findall(r'<a [^>]*class="(?:ad__creative|btn[^"]*)"[^>]*>', inner):
            if 'rel="sponsored nofollow"' not in a: print(f"  FAIL  {route}: {slot} ad link missing rel=sponsored"); bad = 1
    for tag in ("table", "form"):
        for chunk in re.findall(rf"<{tag}\b.*?</{tag}>", src, re.S):
            if "data-ad-slot" in chunk: print(f"  FAIL  {route}: ad inside <{tag}>"); bad = 1
    slots = {s for s, _ in blocks}
    planned = set(ads["page_plan"].get(route, []))
    if slots != planned: print(f"  FAIL  {route}: rendered {sorted(slots)} vs plan {sorted(planned)}"); bad = 1
    counted = len(blocks) - (1 if "margin" in slots else 0)
    if counted > ads["max_per_page"]: print(f"  FAIL  {route}: {counted} ads, max {ads['max_per_page']}"); bad = 1
if not bad: print(f"  ok    {total} ad units: labelled, rel=sponsored, none in tables or forms, match page plan, ad-free routes clean")
sys.exit(bad)
PY
[ $? -ne 0 ] && FAIL=1
echo

[ $FAIL -eq 0 ] && echo "All checks passed." || echo "Checks failed. Fix the items above before pushing."
exit $FAIL
