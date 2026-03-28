from __future__ import annotations


class StateMachine:
    def __init__(self) -> None:
        self.kv: dict[str, object] = {}

    def apply(self, command: dict[str, object]) -> None:
        op = str(command.get("op", "")).lower()
        key = str(command.get("key", ""))

        if op == "set":
            self.kv[key] = command.get("value")
            return

        if op == "delete":
            self.kv.pop(key, None)
            return

        raise ValueError(f"unsupported operation: {op}")
