# Prompt 02: Design system

Builds the tokens, the component CSS and the behaviour script. Neutral by
design: the wireframe tests structure, not brand.

---

```
Build the wireframe design system for DIRECTORY_NAME. Read
docs/deconstruction.md section 4 for the benchmark's visual language.

Take the patterns, not the brand. Do not reuse their colours or fonts.

## assets/tokens.css

The only file allowed to set colour, type families and radii. Define exactly
these custom properties on :root, nothing else (scripts/check.sh enforces the
allowlist):

--font-sans, --font-serif, --bg, --surface, --surface-2, --fg, --muted, --line,
--ink, --ink-fg, --accent, --accent-soft, --accent-strong, --warn-soft,
--radius-sm, --radius, --radius-lg

Redefine the colour tokens for dark mode under
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } }.
Check WCAG AA for --fg on --bg, --muted on --bg, --ink-fg on --ink and
--accent-strong on --accent-soft, in both modes.

Type: one geometric sans for everything, one serif used only for H2s and one
italic accent word per hero H1 (the benchmark's signature move).
Load both from Google Fonts.

## assets/base.css

All layout and components. Reads tokens with var(); never a raw hex value and
never defines a token. Mobile first, breakpoints at 640, 720, 900, 960, 1024.
Container max 1200px with a 16px gutter on mobile, 24px from 768px.

Components, each a reusable class:
- Buttons: .btn plus --primary (ink fill), --ghost (border), --soft, --sm,
  --lg, --block. One primary per viewport.
- Pill eyebrow (.pill), badge (verified, featured), tag chip, star rating,
  logo tile (48px and 88px), striped image placeholder (.ph)
- Sticky header, mega menu panels (anchored to the header bar so they never
  overflow the viewport), mobile drawer, burger
- Breadcrumbs, section head (eyebrow plus H2 on the left, "See all" ghost
  button on the right)
- Card grids 2, 3, 4 up; mini logo card; horizontal snap carousel
- Hero (two column and centred), search bar, stats strip
- Tabs (ARIA tabs) and sticky anchor tabs for long pages
- Numbered steps (3 and 6 up), two column benefit split, checklist
- FAQ accordion on <details>, inline CTA box, full-width dark CTA band,
  platform map link grid
- Listing: filter rail (sticky on desktop, toggled drawer on mobile) with
  searchable checkbox facets and counts; result row card with logo, name,
  badges, rating, meta, blurb, service tags and two actions
- Profile head, two column with sticky aside, key-value list, data table
- Compare: logos with VS badge, verdict banner, side-by-side table
- Forms: field, input, select, textarea, fieldset with legend, chip
  checkboxes, progress bar for a stepper
- Pricing card, guide scorecard, byline bar, table of contents, event row
- Newsletter band, footer, cookie banner, modal
- Wireframe note (.wf-note): yellow annotation, hidden when body has .hide-notes

## assets/site.js

No framework, no dependencies. Every behaviour binds to a data attribute and
silently does nothing if the attribute is absent:
- data-mega: open one mega menu, close on outside click and Escape
- data-toggle: toggle .is-open on a target id (drawer, filters)
- data-tabs with role="tab" and aria-controls
- data-modal-open / data-modal / data-modal-close, Escape closes
- data-cookie banner with data-cookie-choice buttons, choice remembered
- data-notes-toggle: show and hide wireframe notes, remembered
- data-stepper with data-step, data-next, data-prev and a .progress bar
- facet search filtering its own checkbox labels
- form[data-wf-form]: never submits; either navigates to the given path or
  reveals [data-form-msg]

Wrap every localStorage call in try/catch.

## Component gallery

Before stage 3, render one throwaway page that shows every component once and
screenshot it at 1280px and 375px. Delete the page after approval.

Run ./scripts/check.sh. Then stop.
```
