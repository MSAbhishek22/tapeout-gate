"""Smoke tests for the local demo server (server.py) — NEW, 9 Nov 2026.

Starts the real server on an ephemeral localhost port and talks to it
over HTTP. No chain, no network beyond loopback.
"""

import json
import os
import sys
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import server as server_mod  # noqa: E402

TO = "0x1111111111111111111111111111111111111111"


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server_mod.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever,
                                      daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def test_health(self):
        with urllib.request.urlopen(self.url("/api/health")) as resp:
            body = json.loads(resp.read())
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["onchain"], "not_deployed")

    def test_index_serves(self):
        with urllib.request.urlopen(self.url("/")) as resp:
            html = resp.read().decode("utf-8")
        self.assertIn("TapeOut Gate", html)
        self.assertIn("local gate only", html)

    def test_gate_hold_unknown_destination(self):
        req = urllib.request.Request(
            self.url("/api/gate"),
            data=json.dumps({"to": TO, "value": "0", "data": "0x"}).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
        # No allowlist configured on the server -> UNKNOWN -> HOLD.
        self.assertEqual(body["decision"], "HOLD")

    def test_gate_bad_json_400(self):
        req = urllib.request.Request(
            self.url("/api/gate"), data=b"{not json",
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            urllib.request.urlopen(req)
            self.fail("expected HTTPError")
        except urllib.error.HTTPError as exc:
            self.assertEqual(exc.code, 400)


if __name__ == "__main__":
    unittest.main()
