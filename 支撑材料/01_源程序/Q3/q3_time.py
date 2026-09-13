from __future__ import annotations

STAGE_MINUTES = (0, 360, 720, 1080)
SLOTS_PER_DAY = 144
SLOT_MINUTES = 10


def slot_right_endpoint_minute(slot: int) -> int:
    if not 1 <= slot <= SLOTS_PER_DAY:
        raise ValueError(f"slot out of range: {slot}")
    return slot * SLOT_MINUTES


def future_slots(stage_minute: int) -> list[int]:
    if stage_minute not in STAGE_MINUTES:
        raise ValueError(f"unsupported stage minute: {stage_minute}")
    return [
        slot
        for slot in range(1, SLOTS_PER_DAY + 1)
        if slot_right_endpoint_minute(slot) > stage_minute
    ]


def executed_slots(stage_minute: int) -> list[int]:
    future = set(future_slots(stage_minute))
    return [slot for slot in range(1, SLOTS_PER_DAY + 1) if slot not in future]
