from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class RPCHandler(BaseHTTPRequestHandler):
    node = None

    def do_POST(self) -> None:  # noqa: N802
        if RPCHandler.node is None:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b'{"error":"node not ready"}')
            return

        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)
        command = json.loads(body)
        if command.get("type") == "append" and hasattr(RPCHandler.node, "append_entries"):
            result = RPCHandler.node.append_entries(command)
        elif self.path == "/vote" and hasattr(RPCHandler.node, "request_vote"):
            vote = RPCHandler.node.request_vote(
                int(command["term"]),
                str(command["candidate"]),
                int(command.get("last_log_index", -1)),
                int(command.get("last_log_term", 0)),
            )
            term = getattr(RPCHandler.node, "term", command["term"])
            result = {"vote": vote, "term": term}
        else:
            result = RPCHandler.node.apply(command)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def log_message(self, format: str, *args: object) -> None:
        del format, args
        return


def start_rpc(node: object, port: int) -> None:
    RPCHandler.node = node
    server = HTTPServer(("0.0.0.0", port), RPCHandler)
    print(f"[RPC] running on {port}")
    server.serve_forever()
