"""A scripted stand-in for a hosted model, to rehearse the tutor's hosted path without a key.

    uv run labs/_tools/stand_in_model.py            # listens on http://127.0.0.1:8791/v1
    uv run labs/_tools/stand_in_model.py --once 2   # answers two requests, then stops

In another terminal, inside a lab folder of the workspace:

    TUTOR_BASE_URL=http://127.0.0.1:8791/v1 TUTOR_API_KEY=rehearsal uv run ../tutor.py "why?"

It is not a model. It answers every chat-completions request with the same two fixed answers
in turn: a hint in words, then an answer that breaks the tutor rule by including code, so the
rehearsal shows that the tutor withholds it. It proves the wiring (request, answer, log), and
nothing about how a real model follows the tutor instruction. Standard library only.
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ANSWERS = [
    "What did you expect each district to show, and what did you see? Build the smallest case "
    "by hand and print what comes back. Are the two lists equal, or are they the same object?",
    "Here is the fix:\n```python\ngroups = {d: [] for d in districts}\n```\nDoes that help?",
]


class Handler(BaseHTTPRequestHandler):
    served = 0

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        try:
            asked = json.loads(self.rfile.read(length).decode("utf-8"))
            ok = self.path.endswith("/chat/completions") and asked["messages"][0]["role"] == "system"
        except (ValueError, KeyError, IndexError, TypeError):
            ok = False
        if not ok or not self.headers.get("Authorization", "").startswith("Bearer "):
            self.send_response(400)
            self.end_headers()
            return
        answer = ANSWERS[Handler.served % len(ANSWERS)]
        Handler.served += 1
        body = json.dumps({"choices": [{"message": {"role": "assistant", "content": answer}}]}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="A scripted stand-in for a hosted model.")
    parser.add_argument("--port", type=int, default=8791)
    parser.add_argument("--once", type=int, default=0, help="stop after this many requests")
    args = parser.parse_args()
    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"stand-in model on http://127.0.0.1:{args.port}/v1 (not a model: two fixed answers)", flush=True)
    try:
        if args.once:
            for _ in range(args.once):
                server.handle_request()
        else:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
