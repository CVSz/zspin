from __future__ import annotations

import time


class TrueTime:
    def __init__(self, epsilon: float = 0.01) -> None:
        self.epsilon = epsilon

    def now(self) -> tuple[float, float]:
        current = time.time()
        return (current - self.epsilon, current + self.epsilon)

    def after(self, ts: tuple[float, float]) -> None:
        while time.time() < ts[1]:
            time.sleep(0.001)
