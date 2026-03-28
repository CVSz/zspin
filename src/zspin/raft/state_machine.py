from __future__ import annotations

from typing import Callable


class StateMachine:
    def __init__(self) -> None:
        self.kv: dict[str, object] = {}
        self.handlers: dict[str, Callable[[dict[str, object]], None]] = {}

    def register_handler(self, op: str, handler: Callable[[dict[str, object]], None]) -> None:
        self.handlers[op.lower()] = handler

    def apply(self, command: dict[str, object]) -> None:
        op = str(command.get("op", "")).lower()
        key = str(command.get("key", ""))

        handler = self.handlers.get(op)
        if handler is not None:
            handler(command)
            return

        if op == "set":
            self.kv[key] = command.get("value")
            return

        if op == "delete":
            self.kv.pop(key, None)
            return

        raise ValueError(f"unsupported operation: {op}")
