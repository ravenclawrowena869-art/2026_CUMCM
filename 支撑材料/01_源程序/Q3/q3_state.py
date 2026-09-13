from __future__ import annotations

from dataclasses import dataclass, asdict

from q3_time import future_slots, slot_right_endpoint_minute


@dataclass(frozen=True)
class CommitmentChange:
    date: str
    stage_id: int
    decision_minute: int
    target_slot: int
    old_active_commitment_kwh: float
    new_commitment_kwh: float
    delta_plus_kwh: float
    delta_minus_kwh: float
    forecast_vintage_id: str
    known_at_max: str

    def to_dict(self) -> dict:
        return asdict(self)


class ActiveCommitmentBook:
    def __init__(self, date: str) -> None:
        self.date = date
        self.active = [0.0] * 144
        self.stage_ledger: list[CommitmentChange] = []
        self.plan_initialized = False

    def set_day_ahead(self, commitments_kwh: list[float]) -> None:
        if self.plan_initialized:
            raise RuntimeError("day-ahead plan already initialized")
        if len(commitments_kwh) != 144:
            raise ValueError("day-ahead plan must contain 144 slots")
        if any(x < 0 for x in commitments_kwh):
            raise ValueError("negative purchase commitment")
        self.active = list(map(float, commitments_kwh))
        self.plan_initialized = True

    def adjust(
        self,
        stage_id: int,
        decision_minute: int,
        updates: dict[int, float],
        forecast_vintage_id: str,
        known_at_max: str,
    ) -> None:
        if not self.plan_initialized:
            raise RuntimeError("day-ahead plan is missing")
        allowed = set(future_slots(decision_minute))
        for slot, new_value in updates.items():
            if slot not in allowed:
                endpoint = slot_right_endpoint_minute(slot)
                raise RuntimeError(
                    f"slot {slot} ending at {endpoint} min is already executed"
                )
            if new_value < 0:
                raise ValueError("negative purchase commitment")
            old_value = self.active[slot - 1]
            new_value = float(new_value)
            self.active[slot - 1] = new_value
            self.stage_ledger.append(
                CommitmentChange(
                    date=self.date,
                    stage_id=stage_id,
                    decision_minute=decision_minute,
                    target_slot=slot,
                    old_active_commitment_kwh=old_value,
                    new_commitment_kwh=new_value,
                    delta_plus_kwh=max(new_value - old_value, 0.0),
                    delta_minus_kwh=max(old_value - new_value, 0.0),
                    forecast_vintage_id=forecast_vintage_id,
                    known_at_max=known_at_max,
                )
            )
