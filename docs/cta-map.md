# CTA map

One primary CTA per viewport. Primary is the dark filled button
(`.btn--primary`), secondary is ghost (`.btn--ghost`), tertiary is a text link.
Every CTA carries a unique `data-cta` value so clicks are attributable in
analytics. Event name convention: `cta_click` with `cta` = the data-cta value.

## Global

| Location | Primary | Secondary | data-cta |
|---|---|---|---|
| Header | Find a provider → `/match/` | Sign in → auth modal | `nav-find`, `nav-signin` |
| Pre-footer band | Get matched → `/match/` | Talk to our team → `/assist/` | `band-match`, `band-assist` |
| Provider band | List your company → `/for-providers/` | | `band-list` |
| Newsletter | Subscribe | | `newsletter` |
| Cookie banner | Accept all | Customise, Reject non-essential | `cookie-accept`, `cookie-custom`, `cookie-reject` |

## Per template

| Template | Primary | Secondary | Supply side / other |
|---|---|---|---|
| Home hero | Find a provider match → `/match/` | Browse the directory → `/providers/` | |
| Home categories | | View category | Submit your company |
| Listing rows | Request intro (auth modal) | View profile | List your company (promo card) |
| Service category | Get matched for {service} → `/match/` | Compare top providers | List your company |
| Provider profile | Request intro (auth modal) | Compare with... | Claim this profile, Suggest a correction, Write a review |
| Compare pair | Request intro to {A} / {B} | See alternatives | |
| Compare index | Compare (form submit) | Popular comparisons | |
| Match | Find providers (form submit) | Prefer a human? Assist | |
| Assist | Book a call | See how it works | |
| For providers | Create free profile | Talk to sales | |
| Country, industry, method, MCC, glossary | Find providers for {X} → `/match/` | Browse {X} providers | Suggest an edit |
| Journal | Find a provider | Read related guides | Share |
| Events | View event | Submit an event | |

## Auth gating

Gated: Request intro, contacts on profiles, writing reviews. Ungated: all
browsing, guides, comparisons, match tool results summary. Gating more than this
hurts SEO and trust.
