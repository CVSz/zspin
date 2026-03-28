from __future__ import annotations


class QueryPlanner:
    def plan(self, parsed: dict[str, str]) -> dict[str, str]:
        if parsed["type"] == "select":
            return {"op": "scan", "key": parsed["key"]}

        if parsed["type"] == "insert":
            return {"op": "insert", "key": parsed["key"], "value": parsed["value"]}

        if parsed["type"] == "delete":
            return {"op": "delete", "key": parsed["key"]}

        return {"op": "unknown"}
