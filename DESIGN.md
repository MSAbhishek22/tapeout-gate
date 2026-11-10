# DESIGN — TapeOut Gate integration

Status: Day-1 design (9 Nov 2026). Off-chain half is built and tested;
onchain half is written but uncompiled and undeployed. Nothing in this
file claims a live chain interaction.

## 1. The dispatch path (what the user sees)

```
agent drafts a call                user / agent framework
  { to, value, data, function?, code?, memo? }
        │
        ▼
┌─────────────────────────────┐
│  TAPEOUT GATE (off-chain)   │  deterministic, stdlib Python
│  1. canonicalise + hash     │  one JSON form, SHA-256
│  2. secret scan             │  hermes-secret-gate core
│  3. policy scan (code only) │  CageCheck AST core
│  4. destination check       │  allow/block lists
│  5. receipt (masked)        │  replayable
└─────────────┬───────────────┘
              │ decision: ALLOW / HOLD / BLOCK
              ▼
   ALLOW ──► dispatch to TapeOut circuit / X Layer call
             + log receipt to GateAudit
   HOLD  ──► human reviews; dispatch only after a human clears it
             (no auto-approve path for a HOLD)
   BLOCK ──► dispatch refused; receipt logged as BLOCK evidence
```

The gate is a **pre-dispatch checkpoint**, not a proxy: in v1 the agent
framework calls the gate and honours the verdict. A framework that
skips the gate is not stopped — see §6 honest limits.

## 2. Off-chain vs onchain — the precise split

| Piece | Where | Why there |
|---|---|---|
| Secret scanner (9 named rules + entropy heuristic) | Off-chain (`app/scanner.py`) | Regex/entropy over arbitrary text is not something a contract should do; it must also run before any bytes are formed, and it must never see a chain |
| Policy engine (AST: secret paths, subprocess, network egress, destructive calls, secret env reads) | Off-chain (`app/policy.py`), only when the payload carries agent-drafted `code` | Same reason; and running it over hex calldata would be theatre — calldata has no imports |
| Canonicalisation + SHA-256 payload hash | Off-chain (`app/tapeout.py`) | Deterministic bytes must be fixed before anything is hashed or logged |
| Verdict (ALLOW/HOLD/BLOCK) + decision precedence | Off-chain (`app/gate.py`) | Fail-closed logic with human-review semantics lives where the human is |
| Receipts (masked findings, replay string, bounded ring) | Off-chain (`app/receipts.py`) | Receipts contain the evidence; only their id + hashes leave the machine |
| **Audit log** (`GateAudit.recordDecision`) | **Onchain, X Layer** | Append-only, tamper-evident evidence: payload hash, verdict uint8, rules hash, receipt id, sender, timestamp |
| **Destination registry** (`PolicyRegistry.status`) | **Onchain, X Layer** | Allow/block lists are shared team state; the contract is the one copy every agent instance reads |
| Front-end | **X Layer DeWEB** (TapeKit container) + Vercel mirror | A security tool's UI should not be one takedown away from disappearing; Vercel mirror keeps the demo reachable for judges |
| Verdict-as-circuit (stretch) | **TapeOut circuit** via `eval(circuitId, bytes)` | 2-bit verdict mirrored as onchain-computable logic — Tier B, §5 |

**What NEVER goes onchain:** payload content, calldata, memos, code,
secrets, or anything the scanner flagged. Only `bytes32` hashes, a
`uint8` verdict, and a receipt-id string. A receipt id is meaningless
without the off-chain receipt store, which is the point: the chain
proves *a decision happened*, the receipt proves *what the decision was*.

## 3. Payload model

```json
{
  "to": "0x… (40 hex, required)",
  "value": "0 (decimal string, wei, required)",
  "data": "0x… (even hex, required)",
  "function": "transfer(address,uint256) (optional, human-readable)",
  "code": "agent-drafted script (optional; policy-scanned if present)",
  "memo": "free text (optional; secret-scanned like everything else)"
}
```

Canonical form: keys sorted, compact separators, `to`/`data`
lowercased, `value` stripped of leading zeroes. Unknown keys are
rejected — a payload the gate cannot describe exactly is a payload it
cannot approve. `canonical_payload()` raises `PayloadError`; the gate
turns that into a BLOCK receipt, never an exception the caller can
forget.

## 4. Decision precedence (fail-closed, first match wins)

1. Malformed payload → **BLOCK**
2. Secret scan LEAKED → **BLOCK**
3. Policy BLOCKED → **BLOCK**
4. Destination blocklisted → **BLOCK**
5. Secret scan REVIEW → **HOLD**
6. Policy HELD → **HOLD**
7. Destination UNKNOWN (on neither list) → **HOLD**
8. Otherwise → **ALLOW** (requires: clean scan, no code or clean code,
   allowlisted destination)

There is no approve path for a BLOCK. A HOLD is cleared only by a human
removing the cause (the secret, the risky code, the unknown destination)
and re-running the gate — the same rule hermes-secret-gate and
CageCheck already enforce.

## 5. TapeOut circuit integration — two tiers

### Tier A — committed (what the submission will show)

- `GateAudit` + `PolicyRegistry` deployed on **X Layer testnet**
  (chain ID 1952), verified on the explorer, addresses in the
  submission.
- Front-end on **DeWEB** (TapeKit container) + Vercel mirror.
- The submission's "which TapeOut ecosystem features" answer names:
  X Layer contracts (GateAudit, PolicyRegistry) + DeWEB hosting.
- This satisfies the event requirement on its own: "use TapeOut
  circuits, contracts, or onchain data on X Layer, or run on X Layer
  DeWEB" — contracts + DeWEB.

### Tier B — stretch (verify in Week 2, claim only if it works)

A TapeOut circuit that mirrors the 2-bit verdict as onchain logic:
the gate's verdict (ALLOW=00, HOLD=01, BLOCK=10, plus a spare code)
is computable by a small combinational circuit built in the TapeOut
Canvas from NAND/LATCH, taped out as a Circuit NFT, and read back via
`eval(circuitId, bytes)`. The demo would show the same verdict coming
back from the circuit as from the off-chain gate.

**Status: UNVERIFIED.** The `eval(circuitId, bytes)` interface is
secondary-sourced (PANews guide) and the Canvas flow has not been
tried. Week-2 spike: build the smallest possible circuit, tape it out
on testnet, read it back. If any step fails or costs real funds, Tier B
is dropped from the submission with no damage to Tier A — the design
does not depend on it.

## 6. Honest limits (say these to a judge before they find them)

1. **The audit log is evidence, not proof.** A record proves a decision
   was logged by a sender at a time. It does not prove the scan ran —
   anyone can log a fake ALLOW. The receipt's replay string (re-run
   the scan on the same canonical text, same verdict) is the proof,
   and it runs offchain. Do not claim otherwise.
2. **The scanner is not a guarantee.** Regex + entropy catches known
   credential shapes and suspicious tokens. It cannot prove a payload
   is secret-free, and a novel secret format will pass. The UI says so.
3. **v1 does not enforce.** The gate advises; the framework must honour
   it. True enforcement — a dispatcher contract that only forwards
   calls with a fresh ALLOW receipt — is a v2 design (named here, not
   built).
4. **PolicyRegistry v1 has a single owner** (the deployer). Pragmatic
   for a hackathon; not a decentralisation claim. Multisig ownership
   is the stated v2 step.
5. **Contracts are uncompiled and undeployed** as of Day 1. No address
   in this repo is real. Addresses appear only after the Week-2
   testnet deploy, with explorer links.
6. **No TapeOut circuit exists yet.** Tier B is a spike, not a claim.

## 7. "Substantial new development" — the event-work list

New in the event window (this repo, 9 Nov – 8 Dec 2026):

- Payload model, canonicalisation, hashing, verdict encoding,
  onchain-record builder (`app/tapeout.py`)
- Gate orchestration + decision precedence (`app/gate.py`)
- Local demo server + Film Noir front-end (`app/server.py`,
  `app/index.html`)
- Both contracts (`contracts/GateAudit.sol`, `PolicyRegistry.sol`)
- Testnet deploy, DeWEB deploy, TapeOut circuit spike (Weeks 2–3)
- Demo video from the live link + submission narrative (Week 3–4)

Reused, labelled in-code and in README (hermes-secret-gate scanner +
receipts; CageCheck policy engine). The reused cores are the
*instruments*; the TapeOut/X Layer integration, the payload model, and
the product are new — and only the event-window work is what the
submission asks judges to judge.

## 8. Data that must never exist in this repo

Private keys, wallet seeds, API tokens, faucet-claimed test OKB
amounts as "assets", contract addresses before deployment, demo video
URLs before recording, submission confirmation numbers before
submitting. The `.gitignore` equivalent for this scaffold: nothing
secret-shaped is committed, and the scanner itself would flag it —
the test suite includes a case proving a synthetic token never appears
in a receipt or onchain record.
