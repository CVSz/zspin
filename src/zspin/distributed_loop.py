from __future__ import annotations

import time


class DistributedLoop:
    def __init__(self, leader, controller, interval: int = 3) -> None:
        self.leader = leader
        self.controller = controller
        self.interval = interval

    def run(self) -> None:
        while True:
            if self.leader.try_acquire():
                self.controller.run()
                self.leader.renew()

            time.sleep(self.interval)
