"""Gate orchestration — NEW code, written 9 Nov 2026.

Takes one agent-drafted contract-call payload and runs every check in
order, fail-closed, before anything is dispatched toward a TapeOut
circuit or an X Layer contract call:

  1. Canonicalise + hash the payload (tapeout.py).
  2. Secret-scan the canonical text (hermes-secret-gate scanner).
     A LEAKED verdict blocks; REVIEW holds.
  3. If the payload carries agent-drafted ``code``, run the CageCheck
     policy engine on it. BLOCKED blocks; HELD holds. Pure calldata
     payloads report policy ``not_applicable`` — the policy engine
     scans Python, and running it over hex calldata would be theatre.
  4. Check the destination against the allow/block lists. BLOCKED
     blocks; UNKNOWN holds; only an allowlisted destination allows.
  5. Record a masked receipt (never contains secret material) and
     build the onchain record for GateAudit.

Decision precedence (first match wins): malformed payload -> BLOCK;
secret LEAKED -> BLOCK; policy BLOCKED -> BLOCK; destination BLOCK ->
BLOCK; secret REVIEW -> HOLD; policy HELD -> HOLD; destination UNKNOWN
-> HOLD; otherwise ALLOW.

Nothing here sends a transaction, calls an RPC, or contacts TapeOut.
The ``onchain_record`` in the result is a *prepared* call, not a sent
one — see STATUS.md.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from receipts import ReceiptStore  # noqa: E402
from scanner import scan_text  # noqa: E402
from policy import scan as policy_scan  # noqa: E402
from tapeout import (  # noqa: E402
    PayloadError,
    build_onchain_record,
    canonical_payload,
    check_destination,
    payload_hash,
)

DECISION_ALLOW = "ALLOW"
DECISION_HOLD = "HOLD"
DECISION_BLOCK = "BLOCK"


def gate_payload(payload: dict, allowlist=(), blocklist=(),
                 store: ReceiptStore | None = None) -> dict:
    """Run the full gate on one payload dict. Never raises for a bad
    payload — a malformed payload is a BLOCK with a receipt, not an
    exception the caller can forget to handle."""
    store = store or ReceiptStore()
    try:
        canonical = canonical_payload(payload)
    except PayloadError as exc:
        receipt = store.record(
            kind="gate_malformed", verdict="BLOCK",
            gate="tapeout-gate", findings=[{
                "rule": "malformed_payload", "line": 0,
                "masked": str(exc), "severity": "BLOCK",
            }],
        )
        return {
            "decision": DECISION_BLOCK,
            "reason": f"malformed payload: {exc}",
            "scan": None, "policy": None, "destination": None,
            "payload_hash": None, "receipt": receipt,
            "onchain_record": None,
        }

    phash = payload_hash(canonical)
    scan = scan_text(canonical)
    code = payload.get("code")
    if code:
        policy_verdict, policy_rule, policy_detail = policy_scan(code)
        policy = {"verdict": policy_verdict, "rule": policy_rule,
                  "detail": policy_detail}
    else:
        policy = {"verdict": "not_applicable", "rule": "no_code_field",
                  "detail": "Payload carries no agent-drafted code; "
                            "policy engine does not apply to calldata."}

    dest_status, dest_reason = check_destination(
        payload["to"], allowlist, blocklist)
    destination = {"status": dest_status, "reason": dest_reason}

    # --- decision, fail-closed, first match wins -------------------------
    if scan["verdict"] == "LEAKED":
        decision, reason = DECISION_BLOCK, "secret scan: LEAKED"
        rules = [f["rule"] for f in scan["findings"]]
    elif policy["verdict"] == "BLOCKED":
        decision, reason = DECISION_BLOCK, f"policy: {policy['rule']}"
        rules = [policy["rule"]]
    elif dest_status == "BLOCK":
        decision, reason = DECISION_BLOCK, dest_reason
        rules = ["destination_blocklisted"]
    elif scan["verdict"] == "REVIEW":
        decision, reason = DECISION_HOLD, "secret scan: REVIEW"
        rules = [f["rule"] for f in scan["findings"]]
    elif policy["verdict"] == "HELD":
        decision, reason = DECISION_HOLD, f"policy: {policy['rule']}"
        rules = [policy["rule"]]
    elif dest_status == "UNKNOWN":
        decision, reason = DECISION_HOLD, dest_reason
        rules = ["destination_unknown"]
    else:
        decision, reason = DECISION_ALLOW, "all checks passed"
        rules = []

    receipt = store.record(
        kind="gate_decision", verdict=decision,
        gate="tapeout-gate", findings=scan["findings"],
    )
    onchain = build_onchain_record(phash, decision, rules,
                                   receipt["receipt_id"])
    return {
        "decision": decision,
        "reason": reason,
        "scan": scan,
        "policy": policy,
        "destination": destination,
        "payload_hash": phash,
        "receipt": receipt,
        "onchain_record": onchain,
    }
