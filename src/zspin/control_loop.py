from __future__ import annotations

import time
from collections.abc import Callable


class ControlLoop:
    def __init__(
        self,
        observe: Callable[[], dict[str, object]],
        decide: Callable[[dict[str, object]], dict[str, object]],
        act: Callable[[dict[str, object]], None],
        interval: int = 5,
    ) -> None:
        self.observe = observe
        self.decide = decide
        self.act = act
        self.interval = interval

    def run(self) -> None:
        while True:
            state = self.observe()
            decision = self.decide(state)
            self.act(decision)
            time.sleep(self.interval)
