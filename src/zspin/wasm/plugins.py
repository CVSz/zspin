from __future__ import annotations


class WasmPlugin:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, context: dict[str, object]) -> dict[str, str]:
        _ = context
        # placeholder for WASM execution
        return {"plugin": self.name, "status": "executed"}


class PluginManager:
    def __init__(self) -> None:
        self.plugins: list[WasmPlugin] = []

    def register(self, plugin: WasmPlugin) -> None:
        self.plugins.append(plugin)

    def run_all(self, context: dict[str, object]) -> list[dict[str, str]]:
        return [plugin.execute(context) for plugin in self.plugins]
