from __future__ import annotations

from dataclasses import dataclass

from q3_contract import Q3Contract
from q3_state import CommitmentChange


@dataclass(frozen=True)
class SettlementSummary:
    plan_cost_yuan: float
    adjustment_cost_yuan: float
    emergency_cost_yuan: float

    @property
    def total_cost_yuan(self) -> float:
        return self.plan_cost_yuan + self.adjustment_cost_yuan + self.emergency_cost_yuan


def plan_cost(prices: list[float], q0_kwh: list[float]) -> float:
    if len(prices) != len(q0_kwh):
        raise ValueError("price/plan length mismatch")
    return sum(float(p) * float(q) for p, q in zip(prices, q0_kwh))


def adjustment_cost(
    contract: Q3Contract,
    delivery_prices: list[float],
    ledger: list[CommitmentChange],
    issue_prices: dict[int, float] | None = None,
) -> float:
    cost = 0.0
    for row in ledger:
        if contract.settlement_price_time == "DELIVERY_SLOT_PRICE":
            p = float(delivery_prices[row.target_slot - 1])
        elif contract.settlement_price_time == "ISSUE_TIME_PRICE":
            if issue_prices is None or row.stage_id not in issue_prices:
                raise ValueError("issue-time price missing for adjustment stage")
            p = float(issue_prices[row.stage_id])
        else:
            raise ValueError(f"unsupported settlement price time: {contract.settlement_price_time}")
        cost += contract.increase_factor * p * row.delta_plus_kwh
        cost -= contract.decrease_refund_factor * p * row.delta_minus_kwh
    return cost


def final_vs_original_adjustment_cost(
    contract: Q3Contract,
    delivery_prices: list[float],
    q0_kwh: list[float],
    final_commitment_kwh: list[float],
) -> float:
    if len(q0_kwh) != len(final_commitment_kwh):
        raise ValueError("commitment length mismatch")
    cost = 0.0
    for p, q0, qf in zip(delivery_prices, q0_kwh, final_commitment_kwh):
        up = max(float(qf) - float(q0), 0.0)
        down = max(float(q0) - float(qf), 0.0)
        cost += contract.increase_factor * float(p) * up
        cost -= contract.decrease_refund_factor * float(p) * down
    return cost


def emergency_cost(
    contract: Q3Contract,
    prices: list[float],
    emergency_kwh: list[float],
) -> float:
    if len(prices) != len(emergency_kwh):
        raise ValueError("price/emergency length mismatch")
    return sum(
        contract.emergency_factor * float(p) * float(r)
        for p, r in zip(prices, emergency_kwh)
    )


def settle_day(
    contract: Q3Contract,
    prices: list[float],
    q0_kwh: list[float],
    ledger: list[CommitmentChange],
    emergency_kwh: list[float],
    issue_prices: dict[int, float] | None = None,
) -> SettlementSummary:
    return SettlementSummary(
        plan_cost_yuan=plan_cost(prices, q0_kwh),
        adjustment_cost_yuan=adjustment_cost(contract, prices, ledger, issue_prices),
        emergency_cost_yuan=emergency_cost(contract, prices, emergency_kwh),
    )
