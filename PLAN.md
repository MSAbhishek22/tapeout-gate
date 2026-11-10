# PLAN — 4 weeks to the 8 Dec 2026 submission

Deadline: **Mon 8 Dec 2026 05:29 IST** (7 Dec 23:59 UTC, provisional —
re-check the official page weekly; it may move).
Safe target: **submit by Fri 5 Dec 2026 20:00 IST**, leaving a buffer
for a form quirk or a re-record.

## Week 1 — 9–15 Nov (Day 1 done 9 Nov)

- [x] Research (official OKX page, TapeOut, X Layer) — RESEARCH.md
- [x] Scaffold: ported cores + new integration layer + contracts (written)
  + Film Noir front-end + local server — 62/62 tests PASS
- [ ] Parent: live-browser visit to the OKX page — capture the
  **submission form URL + field list** and the **Telegram channel link**
- [ ] Parent: create the GitHub repo (live browser) + push this scaffold
- [ ] Check the X Layer ToS restricted-persons list (India eligibility)
- [ ] Join the event Telegram channel; ask in public if needed:
  form link, Demo Day location, whether a developer tool needs a
  circuit ID or whether contract addresses suffice

## Week 2 — 16–22 Nov: go onchain (testnet)

- [ ] Wallet: fresh self-custodial wallet for this project only
  (user-owned; keys never in the repo, never in chat)
- [ ] Claim test OKB from the X Layer testnet faucet
  (`web3.okx.com/xlayer/faucet` — verify the URL live first);
  record only that the claim succeeded, never amounts as assets
- [ ] Compile `GateAudit.sol` + `PolicyRegistry.sol` in Remix (browser,
  free, no install) against testnet (chain ID 1952); fix any compile
  errors; record the compiler version
- [ ] Deploy both to X Layer testnet; verify on the explorer;
  record addresses + explorer links in STATUS.md + SUBMISSION_DRAFT.md
- [ ] Wire the front-end to read `PolicyRegistry.status` (read-only)
  and to *prepare* (not send) `recordDecision` calls
- [ ] **Tier-B spike:** TapeOut Canvas — build the smallest verdict
  circuit, tape it out on testnet, read it back via `eval(circuitId,
  bytes)`. Go/no-go by 22 Nov. If it fails or needs real funds, drop
  Tier B, keep Tier A
- [ ] Vercel deploy of the front-end (browser task) + confirm the live
  link serves and `/api/gate` answers (or a clearly-labelled demo mode)

## Week 3 — 23–29 Nov: product + DeWEB + video

- [ ] DeWEB deploy (TapeKit container) — verify the DeWEB link serves
  the same front-end; record the link
- [ ] Live end-to-end demo: draft a payload with a planted synthetic
  secret → BLOCK + receipt; clean payload to an allowlisted address →
  ALLOW + onchain log visible on the explorer
- [ ] Interaction inventory (no dead buttons) + responsive + low-motion
  checks on the live link
- [ ] Record the demo video (≤3 min) **from the live link**, with at
  least one real gate run and one explorer view; problem, features,
  users + business model, TapeOut usage — per the judging criteria
- [ ] Fill SUBMISSION_DRAFT.md with real addresses, links, and the
  new-development list

## Week 4 — 30 Nov–5 Dec: harden + submit

- [ ] Buffer for re-records, form quirks, and a second testnet deploy
  if a contract needs a fix
- [ ] Final QA pass against the rulebook gates (live HTTPS, deploy/
  commit match, video from live product, release evidence)
- [ ] **Submit by Fri 5 Dec 20:00 IST** via the form; save the
  confirmation (screenshot + text) in `runs/`
- [ ] Demo Day prep (if shortlisted): 3-minute live run + receipts on
  the explorer, offline Demo Day logistics TBD by organisers

## Deployment runbook

### Front-end (Vercel) — browser task, free tier, no card

1. Repo pushed to GitHub (parent, live browser).
2. Vercel → import repo → framework: static (the front-end is one
   HTML file; the demo server is local-only and NOT deployed — the
   deployed page calls a clearly-labelled demo gate or a small
   serverless `/api/gate` added in Week 2 if a backend is wanted;
   default is a static page with the gate logic compiled to JS in
   Week 3, or a "request a live demo" path — decide in Week 2, do not
   fake a live gate).
3. Confirm the live link serves, no console errors, low-motion toggle
   works, mobile layout holds.
4. Record the URL in STATUS.md; the demo video is recorded from this URL.

### Contracts (Remix) — browser task, free, testnet only

1. Open Remix, create `GateAudit.sol` + `PolicyRegistry.sol` from
   `contracts/` (copy verbatim).
2. Compile with Solidity ^0.8.20; note the exact compiler version.
3. Connect the project wallet to **X Layer testnet (chain ID 1952)**;
   confirm the network in the wallet before sending anything.
4. Deploy GateAudit, then PolicyRegistry; fund only with faucet test
   OKB (never mainnet funds, never a card).
5. Verify each contract on the explorer (Sourcify path if offered);
   copy the explorer URLs into STATUS.md.
6. Allowlist one demo destination via `setBlocked`/`setAllowed` from
   the owner wallet; record the transaction hash.
7. **Stop conditions:** any card/payment prompt, any mainnet network
   in the wallet, any request for a seed phrase outside the wallet
   app — stop and report to the parent.

### DeWEB (TapeKit) — Week 3, steps TBD after the Week-2 spike

DeWEB deploy steps were not verifiable from official docs on Day 1.
Do not invent them here; write them into this runbook after the
hands-on check, with the exact commands/links used.

## If the deadline moves

The event page says the deadline is provisional. Re-check the page
every Monday. If it moves earlier, cut Tier B first, then the DeWEB
deploy (Vercel mirror suffices for the access link), never the
contracts or the video.
