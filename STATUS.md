# STATUS — the honest ledger

Updated 9 Nov 2026 (Day 1). This file is the only place that may claim
a state; README/CONCEPT/DESIGN defer to it.

## What is REAL (verified in this sandbox today)

- Research: official OKX event page read in full (prizes, deadline,
  requirements, judging, terms). See RESEARCH.md.
- Gate core: scanner + policy + receipts ported from hermes-secret-gate
  (42/42 in its home repo) and CageCheck (10/10 in its home repo) —
  both re-run and passing here.
- New integration layer (`app/tapeout.py`, `app/gate.py`) + local demo
  server + Film Noir front-end skeleton — written and tested.
- **Tests: 62/62 PASS** — `python3 -m unittest discover -s tests`,
  Python 3.12.3, Linux sandbox, 0.563s.
  Breakdown: scanner 18 (ported) + policy 6 (ported) + tapeout 23
  (new) + gate 11 (new) + server 4 (new).

## What is SCAFFOLD (written, not live)

- Contracts `GateAudit.sol` + `PolicyRegistry.sol`: written, **not
  compiled** (no solc/Foundry in sandbox), **not deployed**, no
  addresses exist.
- Front-end: skeleton wired to the local server only. No live URL.
- Demo video: not recorded. No video URL exists.
- Submission: not submitted. No confirmation exists.
- GitHub repo: not created. No repo URL exists.
- TapeOut circuit: does not exist. Tier B is a Week-2 spike.

## What is UNKNOWN (do not claim)

- Submission form URL + fields; Telegram channel link; Demo Day
  location/date; X Layer ToS restricted-persons list; `eval(circuitId,
  bytes)` interface; DeWEB deploy steps; FabX/TapeCode function;
  X Layer testnet faucet liveness; TapeOut factory/processor
  addresses on X Layer.

## Rulebook gate state

Per the ABHI_22 rulebook this project is **IN_PROGRESS**: research,
distinct design, working product (local), and QA (tests) are done;
live HTTPS deployment, GitHub/deploy commit match, demo video from
the live product, and final release evidence are all still open.
Do not call it COMPLETE until those pass.
