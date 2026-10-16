# Prompt 05: QA and deploy

Final checks, then GitHub and Vercel. The push and the deploy are outward
facing: Claude asks before each one.

---

```
QA and deploy the DIRECTORY_NAME wireframe.

## 1. Automated
python3 scripts/render.py
./scripts/check.sh
It must pass: no em dashes, no " -- ", site/ in sync with src/, token
allowlist, one H1 per page, no heading skips, JSON-LD parses, every internal
link resolves, no unfilled instruction brackets like [H1: ...], and the ad
policy checks in section 6.

Then list every copy placeholder with:
grep -rnoE "\[[A-Z][^]<]*\]" src/pages data | sort | uniq -c | sort -rn
Group them in the report as: needs a number, needs copy, needs a legal or
business decision.

## 2. Browser
Serve site/ locally (python3 -m http.server 4321 --directory site).
On every route:
- Desktop 1280px: open each mega menu, click every nav and footer link once.
- Mobile 375px: document.documentElement.scrollWidth must equal 375. Open the
  drawer and the filters toggle.
- Test: tabs, accordions, stepper next and back, auth modal open and Escape,
  cookie banner choice persists, notes toggle persists.
- Ads (v2): at 1680px both margin skyscrapers show outside the content
  column; at 1024px and 375px every ad fits its column; the mobile anchor
  closes and stays closed for the session; "Hide ads" hides every slot;
  ad-free pages (match, assist, for providers, advertise, hub, 404) have none.
- Dark mode: emulate prefers-color-scheme dark and screenshot home and profile.
- Console: zero errors.
Fix anything that fails and rerun section 1.

## 3. Report
A short table: route, desktop ok, 375 ok, console clean, notes. Then the
placeholder groups from section 1.

## 4. Commit and push (ask first)
Show me the file list and the commit message, then wait for approval.
git init -b main (if needed), git add -A, commit with an imperative one-line
message, then: gh repo create knivef/REPO_SLUG --private --source=. --push

## 5. Deploy (ask first)
vercel.json already sets outputDirectory to site, no build command, and
X-Robots-Tag noindex on everything. Confirm with me, then:
vercel link, then vercel --prod.
Open the deployed URL and screenshot home, listing, profile and compare.
Give me the URL.
```
