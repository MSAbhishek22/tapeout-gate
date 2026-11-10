# CONCEPT — TapeOut Gate

## The problem (real, specific)

Onchain agents draft contract calls — `to`, `value`, `data` — and send
them. The draft is where secrets leak: an agent that has seen a deploy
key, a wallet seed phrase in a config dump, or an API token in a log
will happily paste it into a memo field, a calldata argument, or a
"helper script" it writes to finish the job. One leaked key in one
transaction is public forever. Existing secret scanners live in editors
and CI; nothing stands between an *agent's draft* and the *chain*.

## The product

**TapeOut Gate** is a developer tool for agent builders on X Layer:
paste (or pipe) an agent-drafted contract-call payload, and the gate
decides ALLOW / HOLD / BLOCK **before dispatch**:

1. **Secret scan** (deterministic, regex + entropy, fail-closed) over the
   canonical payload text. A known credential format = BLOCK. A
   suspicious token = HOLD for a human.
2. **Policy check** on any agent-drafted code attached to the payload
   (CageCheck AST engine): secret paths, subprocess, network egress,
   destructive calls = BLOCK; network import with no connect = HOLD.
3. **Destination check** against an onchain allow/block registry:
   blocklisted = BLOCK, unknown = HOLD, allowlisted = ALLOW.
4. **Receipt** for every decision — masked findings only, replayable
   (re-run the scan, same verdict) — and the receipt's hash + verdict +
   id are written to the **GateAudit contract on X Layer**, so a team
   can prove after the fact that a blocked call was blocked, and when.

## Who pays, and why they keep using it

- **Target users:** teams shipping onchain agents on X Layer / TapeOut
  (agent frameworks, DeFi bots, Telegram trading agents), and their
  users, who currently have no proof a rogue draft was stopped.
- **How to reach them:** the TapeOut + X Layer builder channels
  (event Telegram, TapeOut ecosystem), then agent-framework docs and
  the DeWEB-hosted demo.
- **Revenue model (no token):** free solo/dev tier (local gate + public
  testnet log); paid team tier = hosted verifier + private audit log +
  policy-registry management + Slack/Discord alerts. Teams pay because
  one leaked deploy key costs more than a year of the tool, and because
  the onchain receipt is audit evidence they can show a partner or an
  auditor.
- **Why they keep using it:** it sits in the dispatch path, not in a
  dashboard they forget — every call crosses the desk, so the habit
  forms on day one.

## Why TapeOut / X Layer (not just "a scanner with a chain sticker")

- The **audit log belongs onchain**: a local log can be edited after an
  incident; an append-only contract log cannot. That is the whole
  trust argument, and it only works on a cheap, EVM-equivalent L2 —
  X Layer (chain ID 196, OKB gas, ~1s blocks).
- The **destination registry belongs onchain**: allow/block lists are
  shared team state; a contract is the one copy every agent instance
  can read without a central server.
- The **front-end belongs on DeWEB**: a security tool's own UI should
  not be a takedown away from disappearing; TapeOut's DeWEB (site files
  in a circuit's container) is the honest host for it.
- The **verdict belongs in a circuit (stretch)**: the 2-bit verdict
  (ALLOW/HOLD/BLOCK) is small enough to mirror as onchain-computable
  logic in a TapeOut circuit, callable via `eval(circuitId, bytes)`.
  That is a Week-2 verification spike, not a Day-1 claim — see
  DESIGN.md §5.

## What "substantial new development" means here

Everything a judge touches is new in the event window: the payload
model + canonicalisation + hashing, the gate orchestration and decision
precedence, both contracts, the DeWEB front-end, the TapeOut circuit
spike, the demo video, and the submission narrative. Reused (and
labelled as reused): the deterministic scanner, receipts, and policy
engine cores from hermes-secret-gate and CageCheck. See DESIGN.md §7.

## Out of scope (deliberately)

- No token, no PoD mining participation, no BEM economics.
- No secret *detection* guarantees: regex + entropy catches known
  shapes and suspicious tokens; it cannot prove a payload is
  secret-free. The tool says so in the UI.
- No onchain *enforcement* in v1: the gate runs offchain and the log is
  evidence; a malicious agent that skips the gate is not stopped by
  the contract. Onchain enforcement (a dispatcher contract that only
  forwards allowlisted, receipted calls) is a v2 design, named in
  DESIGN.md §6.
