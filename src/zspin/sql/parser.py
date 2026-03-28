from __future__ import annotations


class SQLParser:
    def parse(self, query: str) -> dict[str, str]:
        tokens = query.strip().split()
        if not tokens:
            raise ValueError("empty query")

        cmd = tokens[0].lower()

        if cmd == "insert" and len(tokens) >= 3:
            return {"type": "insert", "key": tokens[1], "value": " ".join(tokens[2:])}

        if cmd == "select" and len(tokens) == 2:
            return {"type": "select", "key": tokens[1]}

        if cmd == "delete" and len(tokens) == 2:
            return {"type": "delete", "key": tokens[1]}

        raise ValueError("unsupported query")
