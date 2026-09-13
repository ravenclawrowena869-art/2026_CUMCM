from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from q3_contract import Q3Contract


STAGE_SCHEDULES = {
    "S0_00_ONLY": (0,),
    "S3_00_06_12_18": (0, 360, 720, 1080),
}


class Q3Controller(Protocol):
    def run_year(self, contract: Q3Contract, stage_minutes: tuple[int, ...]) -> dict:
        ...


@dataclass
class FormalQ3Runner:
    contract: Q3Contract
    controller: Q3Controller

    def run(self, strategy_id: str) -> dict:
        self.contract.require_formal_lock()
        if strategy_id not in STAGE_SCHEDULES:
            raise ValueError(f"unknown Q3 strategy: {strategy_id}")
        return self.controller.run_year(self.contract, STAGE_SCHEDULES[strategy_id])
