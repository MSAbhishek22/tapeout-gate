# SUBMISSION DRAFT — OKX X Layer TapeOut Accelerate

Status: DRAFT, 9 Nov 2026. The form itself has not been seen yet —
its URL and field list are UNKNOWN (see RESEARCH.md §5.1). This draft
holds everything the official page says the submission must contain,
so filling the form is mechanical once the link is captured. Nothing
below is submitted anywhere.

## What the official page requires

- Project description: product/service, target users + how to reach
  them, revenue model, why users pay and keep using it. (Tool projects
  may explain use cases + commercial applications instead.)
- Relevant addresses or links.
- Circuit projects: processor contract address + circuit ID.
- Websites/apps/tools: an access link + which TapeOut ecosystem
  projects/features are used.
- Existing projects: describe the substantial new development completed
  during the event.

## Draft answers (fill the TBDs in Weeks 2–3)

**Project name:** TapeOut Gate
**One-liner:** A secret-leak guard for onchain agents — every
agent-drafted call is scanned, policy-checked, and destination-checked
before dispatch, and every decision is receipted on X Layer.
**Category:** Developer tool.
**Access link:** TBD — Vercel URL (Week 2) + DeWEB link (Week 3).
**Demo video (≤3 min):** TBD — record Week 3 from the live link.
**Contracts (X Layer testnet, chain ID 1952):**
- GateAudit: TBD — not deployed
- PolicyRegistry: TBD — not deployed
**TapeOut circuit:** TBD — Tier-B spike, Week 2 (processor contract
address + circuit ID only if the spike succeeds).
**TapeOut ecosystem features used:** X Layer contracts (GateAudit,
PolicyRegistry); X Layer DeWEB hosting (front-end); TapeOut circuit
(Tier B, if verified). No BEM, no PoD mining, no token.
**Target users:** teams shipping onchain agents on X Layer / TapeOut;
reached via the event Telegram, TapeOut ecosystem channels, and
agent-framework docs.
**Revenue model:** free solo/dev tier; paid team tier (hosted verifier
+ private audit log + registry management + alerts). No token.
**Why users pay and keep using:** one leaked deploy key costs more
than a year of the tool; the onchain receipt is audit evidence; and
the gate sits in the dispatch path, so use is habitual, not optional.
**Existing project?** Yes — built on hermes-secret-gate and CageCheck.
**New development during the event:** payload model +
canonicalisation + hashing; gate orchestration + decision precedence;
both contracts; DeWEB front-end; TapeOut circuit spike; demo video;
submission narrative. (Full list: DESIGN.md §7.)
**Team:** solo — M S Abhishek (India). **Wallet for prizes:** TBD —
self-custodial address to be confirmed by the user at submission
time; never invented here.

## Form-ready: team background + elevator pitch (written 9 Nov 2026)

**Team + background (form field):** Solo — M S Abhishek, BTech
Computer Science & Engineering, 7th semester, Shobhit University,
Meerut, India. I build deterministic secret-leak guards:
hermes-secret-gate, a secret-scan plugin for the Hermes agent whose
catalog PR was merged into NousResearch/hermes-agent, and CageCheck,
a fail-closed secret-leak guard for agent-written code. TapeOut Gate
is built on those two cores, with all TapeOut/X Layer integration —
payload model, gate orchestration, both contracts, front-end —
written new for this event.

**Elevator pitch (form field):** Onchain agents draft contract
calls, and the draft is where secrets leak — one deploy key pasted
into a memo or calldata is public forever. TapeOut Gate is a
pre-dispatch checkpoint for agent builders on X Layer: every
agent-drafted call is secret-scanned, policy-checked, and
destination-checked before dispatch, with a clear ALLOW / HOLD /
BLOCK verdict and a masked, replayable receipt for every decision.
The receipt's hash and verdict are written to the GateAudit contract
on X Layer, so a team can prove after the fact that a blocked call
was blocked. Only hashes leave the machine — no payload, secret, or
code ever touches the chain.

*(Pitch note: the contracts are written but not yet deployed — testnet
deploy is Week 2 per PLAN.md. The pitch above is the submission text;
do not paste it into the form until the deploy is real and the
addresses are in this draft.)*

## Still unknown (parent / Week 2)

**RESOLVED 9 Nov 21:01 IST (browser flow check on the official page https://web3.okx.com/xlayer/build-x-series):**
1. Form URL + exact fields — **KNOWN: single Google Form = registration + submission (no separate register step). Short URL https://forms.gle/EoDNbxQ65dev1wFd9 ; full URL https://docs.google.com/forms/d/e/1FAIpQLScyVnDmyzxRyBxszLUWbwV5kVbpmZJ3JS6oyOxqjALRvhR1kg/viewform. Deadline: before 7 Dec 23:59 UTC (= 8 Dec 05:29 IST). Entries can be updated later, but project fields are required even for an early entry. Fields (all required except website): Full Name, Nationality, Project name, Project logo (upload, 256x256 px, max 10 MB), Telegram handle, Project X Account, Team contact email, team size (max 4), team + background, elevator pitch, GitHub repo link, Demo Video link (max 3 min — longer may be disqualified), project website (optional).**
2. Telegram support channel link — **KNOWN: https://t.me/+-7ouB60aYig2MmM1 (join for updates). Also follow https://x.com/XLayerOfficial and https://x.com/TapeOutWorld. No X post required.**
3. Demo Day location + date — **STILL TBA: "Online/Offline Demo Day"; finale offline, location chosen by nationality.**
4. Whether a developer tool must supply a circuit ID or whether contract addresses + DeWEB link suffice — **still open.**
5. X Layer ToS restricted-persons list (India eligibility wording) — **STILL UNVERIFIED: no country list on the page; India neither expressly included nor excluded. Terms: 18+, local law, sanctions, Restricted Persons ineligible; winners face identity checks. Prize confirmed on page: 100,000 USDT (1st 20,000 x1, 2nd 10,000 x5, 3rd 6,000 x5), staged milestone payout. Solo OK ("Individuals and teams are welcome").**
6. **Still missing to submit:** GitHub repo URL (no repo yet), demo video (no video yet), project logo (no file yet), project X account (none yet), nationality (user to confirm), prize wallet (user to confirm at submission time, never invented).
