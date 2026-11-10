# DESIGN CONSTITUTION — TapeOut Gate

Status: describes the **Day-1 skeleton UI** in `app/index.html`
(9 Nov 2026). Where the built UI differs from this file later, the
built UI wins and the difference must be stated here.

## 0. Style pick (permanent user rule, 9 Nov)

**Cinematic / Film Noir — chosen. Neo-Brutalism — rejected, and why:**

A secret-leak guard is a night-desk job: one lamp, one verdict, one
receipt. Film Noir gives that directly — near-black scenes, a single
warm spotlight, signal lamps (amber/red/green) as the only colour that
matters, oversized verdict typography as the dramatic beat. It fits the
product's emotional promise: quiet, procedural, trustworthy.

Neo-Brutalism was the other candidate. Its loud flat colour blocks and
heavy borders would fight the product in two ways: they make dense
receipts and hashes harder to read (the judge's core evidence), and
they shout where a fail-closed gate should stay calm — a gate that
looks excitable is a gate you don't trust with keys. Noir wins on both
readability and tone.

## 1. Product personality and emotional tone

A night-shift security desk, not a hacker terminal and not a SaaS
dashboard. Calm, procedural, a little severe. The verdict is the only
drama in the room. Nothing glows, nothing pulses, nothing pretends to
be intelligent. The intelligence is in the procedure, and the procedure
is visible: paste → check → verdict → receipt → onchain log.

## 2. Target user and context of use

A developer about to let an agent send a contract call, and a judge
watching a screen share. Primary viewing context is a laptop screen
share: the whole decision must be readable in one scroll, with no tab
hunting. The user pastes an untrusted draft; the tool must never send
that draft anywhere except — as hashes — to the audit log. A BLOCK
means "refused", never "sent anyway".

## 3. Visual metaphor — desk lamp + signal lamps + receipt

- **Desk lamp:** a single warm radial spotlight from the top of the
  page (amber, 14% opacity). Everything else stays in the dark.
- **Signal lamps:** ALLOW / HOLD / BLOCK as pill lamps; only one is
  ever lit, in green / amber / red. The lamps are the status system —
  no other status colour exists on the page.
- **Receipt:** monospace, panelled, the only place hashes and JSON
  appear. A receipt looks like paper under the lamp.
- **Verdict as cinema:** the verdict word is the largest type on the
  page (44–84px), letters staggering in one by one — the one kinetic
  moment, and it means something every time.

## 4. Colour palette (semantic roles)

| Role | Value | Use |
|---|---|---|
| Night | `#0b0a08` | Page background |
| Desk | `#14120e` | Panels, inputs, receipt |
| Paper | `#e8e2d4` | Primary text |
| Dim | `#9a937f` | Secondary text, labels |
| Line | `#3a332a` | Borders, dividers |
| Lamp amber | `#e8a33d` | Spotlight, HOLD, primary button, accents |
| Alarm red | `#e5484d` | BLOCK |
| Clear green | `#4cc38a` | ALLOW |

No other hues. The amber is the only warm accent; red and green appear
only as verdicts.

## 5. Typography

- **Display / verdict:** Georgia serif, light weight, tight leading —
  the cinematic voice. Verdict letters stagger in (kinetic typography).
- **Body:** Georgia serif, 19px lede, 1.6 line-height — readable,
  editorial, unhurried.
- **Data / labels / buttons:** ui-monospace, letterspaced uppercase
  labels (12px, 0.18–0.28em). Receipts, hashes, and JSON are always
  monospace; prose is never monospace.

## 6. Layout, grid, composition

Single column, max 880px, generous vertical rhythm (48px sections,
56px kicker). Three numbered beats: 1 paste the draft, 2 the verdict,
3 the receipt — then a short "what happens onchain" coda. One scroll,
no tabs, no sidebar. Borders are 1px lines; panels are flat. The demo
banner (local-only warning) sits above everything until a deploy
exists, then it is replaced by the live status line.

## 7. Components and behaviour

- **Payload textarea:** monospace, pre-filled with a harmless example
  (`to` zero address, `ping()`). Invalid JSON → BLOCK with the parse
  error, never a crash.
- **Run the gate button:** amber, uppercase mono. One action, one
  outcome.
- **Verdict:** kinetic stagger (45ms per letter), colour by decision.
- **Receipt `<pre>`:** full JSON of decision + masked receipt +
  prepared onchain record. Never contains secret material (tested).
- **Low-motion toggle:** button + `prefers-reduced-motion` both
  disable all motion; the verdict renders instantly.

## 8. Motion language (at least two techniques, per the style rule)

1. **Scroll reveal + stagger** — sections fade/slide in via
   IntersectionObserver (opacity + translateY only).
2. **Kinetic typography** — verdict letters stagger in with per-letter
   delay (opacity + translateY only).
3. No other motion. No particles, no continuous animation, no 3D
   canvas in v1 — a security desk does not spin.

## 9. 3D concept

Deliberately minimal in v1: depth comes from the spotlight gradient
and the lamp glow, not from a 3D scene. If a 3D element is added later
(Week 3), it must be one object only — a glass signal lamp or a paper
receipt in shallow depth — and it must serve the verdict moment, not
decorate the page. No multiple real-time 3D canvases, ever.

## 10. Performance rules (non-negotiable)

- Animate transform + opacity only. Never width/height/top/left.
- No hundreds of continuous particles; no continuous animation at all.
- Compressed assets only (no images in v1 at all — pure CSS).
- Off-screen animations paused (IntersectionObserver unobserves after
  reveal).
- `prefers-reduced-motion` respected + a visible low-motion toggle.
- Must stay usable on a low-end phone: single column, system fonts,
  no framework.

## 11. Responsive behaviour

Desktop: 880px column, 72px headline. Mobile: same column, 40px
headline, lamps wrap, textarea full-width, receipt scrolls
horizontally within its panel. No layout shift on verdict change
(the verdict block reserves its line).

## 12. Design research — HONEST STATUS

Rulebook §1.1 asks for five inspected references. **Not done yet:**
no design-reference sites were visually inspected on Day 1, and none
are claimed here. Week 2 will inspect two developer-security tools,
one cinematic/motion reference, one strong-typography reference, and
one data-dense receipt/log UI, and record them in
`design/DESIGN_REGISTRY.md` with URLs, dates, and what was learned.
Until then, this constitution rests on the stated metaphor and the
CageCheck lineage (border-inspector desk), not on inspected references.
