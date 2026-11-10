# DESIGN REGISTRY — TapeOut Gate

The registry of every visual decision, so the identity never repeats
and never drifts silently. Updated when the built UI changes.

## Identity

- **Style:** Cinematic / Film Noir (chosen 9 Nov 2026; Neo-Brutalism
  explicitly rejected — see DESIGN_CONSTITUTION.md §0).
- **Metaphor:** night desk — desk lamp + signal lamps + paper receipt.
- **Palette:** night `#0b0a08`, desk `#14120e`, paper `#e8e2d4`,
  dim `#9a937f`, line `#3a332a`, lamp amber `#e8a33d`, alarm red
  `#e5484d`, clear green `#4cc38a`.
- **Type:** Georgia serif (display/body) + ui-monospace (data/labels).
- **Motion:** scroll reveal + stagger; kinetic verdict typography.
  Transform + opacity only. Low-motion mode included.

## Elements in use (Day-1 skeleton)

| Element | Where | Notes |
|---|---|---|
| Spotlight gradient | `body::before` | Amber radial, top-centre, 14% |
| Demo banner | Header | Amber border; says "local gate only" until a deploy exists |
| Kicker | Header | Mono, letterspaced, "OKX X Layer · TapeOut Accelerate · Developer tool" |
| Headline | Header | "The night desk for onchain agents." — amber on "onchain agents." |
| Signal lamps | Header | ALLOW / HOLD / BLOCK pills; one lit at a time |
| Low-motion toggle | Header | Button; also auto-on under `prefers-reduced-motion` |
| Payload textarea | §1 | Prefilled harmless example; mono |
| Run the gate | §1 | Amber button; POSTs to `/api/gate` |
| Verdict | §2 | 44–84px, kinetic stagger, colour by decision |
| Receipt | §3 | Mono `<pre>`; decision + masked receipt + onchain record |
| Onchain coda | §4 | What leaves the desk; "not deployed yet" until Week 2 |

## Interaction inventory (Day 1)

| Control | Works? | Notes |
|---|---|---|
| Low-motion toggle | Yes (local) | Toggles `body.low-motion` |
| Run the gate | Yes (local server) | Needs `python3 app/server.py`; invalid JSON → BLOCK with error |
| Lamps | Yes | Lit from the gate response |
| Payload textarea | Yes | Editable; example is harmless |
| Allowlist input | Removed 9 Nov | Was a display-only field (dead control). Server allowlist is set by `--allow` flags; the UI now explains that in text instead. |

## Design references

**None inspected yet (Day 1).** Week 2: two developer-security
tools, one cinematic/motion reference, one typography reference, one
data-dense receipt/log UI — each with URL, date inspected, what was
learned, what NOT to copy. No reference is recorded until it is
actually inspected.
