from __future__ import annotations

from dataclasses import asdict, dataclass

from q3_contract import Q3Contract
from q3_settlement import settle_day
from q3_state import CommitmentChange
from q3_storage import replay_storage
from q3_time import slot_right_endpoint_minute


@dataclass(frozen=True)
class ValidationReport:
    pass_all: bool
    executed_slot_mutation_count: int
    commitment_delta_max_residual_kwh: float
    cost_identity_residual_yuan: float
    balance_max_residual_kwh: float
    balance_argmax_slot: int | None
    soc_bound_max_violation_kwh: float
    storage_power_max_violation_kwh: float
    soc_recursion_max_residual_kwh: float
    simultaneous_charge_discharge_count: int

    def to_dict(self) -> dict:
        return asdict(self)


def validate_day(
    contract: Q3Contract,
    prices: list[float],
    q0_kwh: list[float],
    ledger: list[CommitmentChange],
    final_commitment_kwh: list[float],
    normal_received_kwh: list[float],
    emergency_kwh: list[float],
    actual_load_kwh: list[float],
    actual_pv_kwh: list[float],
    charge_kwh: list[float],
    discharge_kwh: list[float],
    initial_soc_kwh: float,
    reported_soc_end_kwh: list[float],
    claimed_total_cost_yuan: float,
) -> ValidationReport:
    n = 144
    vectors = [prices, q0_kwh, final_commitment_kwh, normal_received_kwh, emergency_kwh,
               actual_load_kwh, actual_pv_kwh, charge_kwh, discharge_kwh, reported_soc_end_kwh]
    if any(len(v) != n for v in vectors):
        raise ValueError("Q3 daily vectors must have 144 slots")

    mutation_count = 0
    delta_residual = 0.0
    replayed = list(map(float, q0_kwh))
    for row in ledger:
        if slot_right_endpoint_minute(row.target_slot) <= row.decision_minute:
            mutation_count += 1
        expected_plus = max(row.new_commitment_kwh - row.old_active_commitment_kwh, 0.0)
        expected_minus = max(row.old_active_commitment_kwh - row.new_commitment_kwh, 0.0)
        delta_residual = max(
            delta_residual,
            abs(expected_plus - row.delta_plus_kwh),
            abs(expected_minus - row.delta_minus_kwh),
            abs(replayed[row.target_slot - 1] - row.old_active_commitment_kwh),
        )
        replayed[row.target_slot - 1] = row.new_commitment_kwh
    delta_residual = max(
        delta_residual,
        max(abs(a - b) for a, b in zip(replayed, final_commitment_kwh)),
    )

    settlement = settle_day(contract, prices, q0_kwh, ledger, emergency_kwh)
    cost_residual = abs(settlement.total_cost_yuan - float(claimed_total_cost_yuan))

    max_balance = 0.0
    argmax = None
    for i in range(n):
        lhs = normal_received_kwh[i] + emergency_kwh[i] + actual_pv_kwh[i] + discharge_kwh[i]
        rhs = actual_load_kwh[i] + charge_kwh[i]
        residual = abs(lhs - rhs)
        if residual > max_balance:
            max_balance = residual
            argmax = i + 1

    storage = replay_storage(
        contract,
        initial_soc_kwh,
        charge_kwh,
        discharge_kwh,
        reported_soc_end_kwh,
    )

    tol = 1e-7
    pass_all = all([
        mutation_count == 0,
        delta_residual <= tol,
        cost_residual <= 1e-6,
        max_balance <= tol,
        storage.max_bound_violation_kwh <= tol,
        storage.max_power_violation_kwh <= tol,
        storage.max_recursion_residual_kwh <= tol,
        storage.simultaneous_charge_discharge_count == 0,
    ])

    return ValidationReport(
        pass_all=pass_all,
        executed_slot_mutation_count=mutation_count,
        commitment_delta_max_residual_kwh=delta_residual,
        cost_identity_residual_yuan=cost_residual,
        balance_max_residual_kwh=max_balance,
        balance_argmax_slot=argmax,
        soc_bound_max_violation_kwh=storage.max_bound_violation_kwh,
        storage_power_max_violation_kwh=storage.max_power_violation_kwh,
        soc_recursion_max_residual_kwh=storage.max_recursion_residual_kwh,
        simultaneous_charge_discharge_count=storage.simultaneous_charge_discharge_count,
    )
