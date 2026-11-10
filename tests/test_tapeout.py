"""Tests for the NEW TapeOut/X Layer integration layer (tapeout.py)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from tapeout import (
    PayloadError,
    build_onchain_record,
    canonical_payload,
    check_destination,
    encode_verdict,
    payload_hash,
    rules_hash,
    verdict_name,
)

TO = "0x1111111111111111111111111111111111111111"
TO2 = "0x2222222222222222222222222222222222222222"


class TestCanonicalPayload(unittest.TestCase):
    def test_canonical_is_deterministic(self):
        a = {"to": TO, "value": "0", "data": "0x"}
        b = {"data": "0x", "value": "0", "to": TO}
        self.assertEqual(canonical_payload(a), canonical_payload(b))

    def test_value_normalises_leading_zeroes(self):
        self.assertIn('"value":"0"', canonical_payload(
            {"to": TO, "value": "000", "data": "0x"}))

    def test_address_lowercased(self):
        out = canonical_payload(
            {"to": "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
             "value": "0", "data": "0x"})
        self.assertIn("0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", out)

    def test_missing_field_rejected(self):
        with self.assertRaises(PayloadError):
            canonical_payload({"to": TO, "value": "0"})

    def test_bad_address_rejected(self):
        with self.assertRaises(PayloadError):
            canonical_payload({"to": "not-an-address", "value": "0", "data": "0x"})

    def test_odd_hex_data_rejected(self):
        with self.assertRaises(PayloadError):
            canonical_payload({"to": TO, "value": "0", "data": "0x123"})

    def test_unknown_key_rejected(self):
        with self.assertRaises(PayloadError):
            canonical_payload({"to": TO, "value": "0", "data": "0x",
                               "surprise": True})

    def test_non_dict_rejected(self):
        with self.assertRaises(PayloadError):
            canonical_payload("nope")


class TestHashes(unittest.TestCase):
    def test_payload_hash_is_64_hex(self):
        h = payload_hash(canonical_payload({"to": TO, "value": "0", "data": "0x"}))
        self.assertEqual(len(h), 64)
        int(h, 16)  # must parse as hex

    def test_same_payload_same_hash(self):
        c = canonical_payload({"to": TO, "value": "0", "data": "0x"})
        self.assertEqual(payload_hash(c), payload_hash(c))

    def test_different_payload_different_hash(self):
        c1 = canonical_payload({"to": TO, "value": "0", "data": "0x"})
        c2 = canonical_payload({"to": TO, "value": "1", "data": "0x"})
        self.assertNotEqual(payload_hash(c1), payload_hash(c2))

    def test_rules_hash_order_independent(self):
        self.assertEqual(rules_hash(["b", "a"]), rules_hash(["a", "b"]))

    def test_rules_hash_empty_is_stable(self):
        self.assertEqual(rules_hash([]), rules_hash([]))


class TestVerdictEncoding(unittest.TestCase):
    def test_roundtrip(self):
        for word, code in (("ALLOW", 0), ("HOLD", 1), ("BLOCK", 2)):
            self.assertEqual(encode_verdict(word), code)
            self.assertEqual(verdict_name(code), word)

    def test_unknown_word_rejected(self):
        with self.assertRaises(PayloadError):
            encode_verdict("MAYBE")

    def test_unknown_code_rejected(self):
        with self.assertRaises(PayloadError):
            verdict_name(9)


class TestOnchainRecord(unittest.TestCase):
    def test_record_shape_matches_contract(self):
        rec = build_onchain_record("ab" * 32, "BLOCK",
                                   ["github_token"], "HSG-20261109-0001")
        self.assertEqual(rec["contract"], "GateAudit")
        self.assertEqual(rec["function"], "recordDecision")
        args = rec["args"]
        self.assertEqual(args["payloadHash"], "0x" + "ab" * 32)
        self.assertEqual(args["verdict"], 2)
        self.assertEqual(args["verdictName"], "BLOCK")
        self.assertTrue(args["rulesHash"].startswith("0x"))
        self.assertEqual(args["receiptId"], "HSG-20261109-0001")

    def test_bad_hash_rejected(self):
        with self.assertRaises(PayloadError):
            build_onchain_record("xyz", "ALLOW", [], "HSG-1")

    def test_empty_receipt_rejected(self):
        with self.assertRaises(PayloadError):
            build_onchain_record("ab" * 32, "ALLOW", [], "")


class TestDestination(unittest.TestCase):
    def test_allowlisted(self):
        self.assertEqual(check_destination(TO, [TO], [])[0], "ALLOW")

    def test_blocklisted(self):
        self.assertEqual(check_destination(TO, [], [TO])[0], "BLOCK")

    def test_block_wins_over_allow(self):
        self.assertEqual(check_destination(TO, [TO], [TO])[0], "BLOCK")

    def test_unknown_is_unknown(self):
        status, reason = check_destination(TO2, [TO], [])
        self.assertEqual(status, "UNKNOWN")
        self.assertIn("neither list", reason)


if __name__ == "__main__":
    unittest.main()
