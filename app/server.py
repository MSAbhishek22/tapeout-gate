"""Local demo server — NEW code, written 9 Nov 2026.

Stdlib only (http.server). Serves the Film Noir front-end and one
endpoint, POST /api/gate, which runs the deterministic gate on a JSON
payload and returns the decision + masked receipt + prepared onchain
record.

This server is LOCAL ONLY. It sends nothing to any chain, signs
nothing, and holds no keys. It exists so the gate can be demoed and
smoke-tested before any deploy. Run:

    python3 app/server.py            # http://127.0.0.1:8000

Allow/block lists are empty by default, so every destination is
UNKNOWN and every well-formed clean payload HOLDs — that is the
fail-closed default, not a bug. Pass --allow 0x... to allowlist a
destination for a demo run.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gate import gate_payload  # noqa: E402
from receipts import ReceiptStore  # noqa: E402

STORE = ReceiptStore()
ALLOWLIST: set = set()
BLOCKLIST: set = set()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep test output quiet
        pass

    def _send_json(self, status: int, obj: dict) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path in ("/", "/index.html"):
            here = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(here, "index.html"), "rb") as fh:
                body = fh.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok", "gate": "tapeout-gate",
                                  "onchain": "not_deployed"})
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        if self.path != "/api/gate":
            self._send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._send_json(400, {"error": "bad Content-Length"})
            return
        if length > 64 * 1024:
            self._send_json(413, {"error": "payload too large (64 KiB max)"})
            return
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "body is not valid JSON"})
            return
        if not isinstance(payload, dict):
            self._send_json(400, {"error": "body must be a JSON object"})
            return
        result = gate_payload(payload, ALLOWLIST, BLOCKLIST, STORE)
        self._send_json(200, result)


def main() -> None:
    parser = argparse.ArgumentParser(description="TapeOut Gate local demo")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--allow", action="append", default=[],
                        help="allowlisted destination address (repeatable)")
    parser.add_argument("--block", action="append", default=[],
                        help="blocklisted destination address (repeatable)")
    args = parser.parse_args()
    ALLOWLIST.update(a.lower() for a in args.allow)
    BLOCKLIST.update(b.lower() for b in args.block)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"TapeOut Gate demo at http://127.0.0.1:{args.port} "
          f"(local only, nothing onchain)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
