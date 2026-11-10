# TapeOut Gate — a secret-leak guard for onchain agents

**Event:** OKX X Layer TapeOut Accelerate · 100,000 USDT pool (1st 20,000 /
2nd 10,000×5 / 3rd 6,000×5) · **deadline Mon 8 Dec 2026 05:29 IST**
(7 Dec 23:59 UTC, provisional) · solo, online, free, India not excluded
on the event page.

**One-line pitch:** before an agent's drafted call reaches a TapeOut circuit
or an X Layer contract, it crosses this desk — secrets get stopped,
destinations get checked, every decision gets a receipt, and the receipt
is logged onchain.

## Status — Day 1 (9 Nov 2026): RESEARCH + SCAFFOLD

| Piece | State |
|---|---|
| Research (official OKX page + TapeOut/X Layer docs) | Done — see RESEARCH.md |
| Deterministic gate core (scanner / policy / receipts) | Ported, **62/62 tests PASS** (Python 3.12.3, unittest, Linux sandbox) |
| TapeOut/X Layer integration layer (`app/tapeout.py`, `app/gate.py`) | Written, tested, **no chain contact yet** |
| Contracts (`GateAudit.sol`, `PolicyRegistry.sol`) | Written, **NOT compiled, NOT deployed** (no solc/Foundry in sandbox) |
| Front-end skeleton (Film Noir) + local demo server | Written, serves locally, talks to `/api/gate` |
| GitHub repo | Not created (parent creates via live browser) |
| Vercel deploy | Not attempted (browser task) |
| Submission | Not submitted — deadline 8 Dec 05:29 IST |

**Honest summary:** the gate runs for real on your machine today. Nothing
runs against TapeOut or X Layer yet. The onchain half is designed,
written, and waiting for the Week-2 testnet deploy.

## Run it locally

```bash
python3 -m unittest discover -s tests          # 62 tests
python3 app/server.py                           # http://127.0.0.1:8000
python3 app/server.py --allow 0x1111...         # demo with an allowlisted dest
```

## Layout

- `CONCEPT.md` — what it is, who pays, why it wins
- `RESEARCH.md` — verified vs unverified, with sources + dates
- `DESIGN.md` — the precise off-chain / onchain split
- `PLAN.md` — 4-week build plan + deployment runbook
- `SUBMISSION_DRAFT.md` — what the form asks, what's still unknown
- `STATUS.md` — the honest ledger (what's real, what's scaffold)
- `design/` — design constitution + registry (Film Noir)
- `app/` — scanner + policy + receipts (REUSED, labelled) · tapeout + gate
  + server + front-end (NEW)
- `contracts/` — GateAudit + PolicyRegistry (written, uncompiled)
- `tests/` — 62 tests (24 ported, 38 new)

## Reuse, labelled honestly

- `app/scanner.py`, `app/receipts.py` — ported verbatim from
  hermes-secret-gate (42/42 tests in its home repo, verified 9 Nov 2026).
- `app/policy.py` — ported verbatim from CageCheck (10/10 in its home repo).
- Everything TapeOut/X Layer-facing is NEW: payload canonicalisation +
  hashing, verdict encoding, onchain-record builder, destination registry
  checks, gate orchestration, contracts, front-end, submission narrative.
- The event rules allow existing projects with substantial new development
  during the event — the new-development list is in DESIGN.md §7.

## Rules that bind this project

Free-only, no card, no secrets in the repo, no invented addresses or
numbers, no claim of a deploy until an explorer link exists. The
ABHI_22 quality rulebook applies: this scaffold is IN_PROGRESS, not
COMPLETE — it lacks live HTTPS, a live-recorded demo video, and the
remaining gates.
