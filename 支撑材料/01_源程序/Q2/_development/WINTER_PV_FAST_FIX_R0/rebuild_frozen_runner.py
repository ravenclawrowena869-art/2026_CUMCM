from __future__ import annotations

import base64
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PART_DIR = ROOT / "frozen_runner_chunks"
OUT_DIR = ROOT / "frozen_runner"
OUT_FILE = OUT_DIR / "run_q80_year.py"
EXPECTED_SHA256 = "5a2ab76328a70a939ab9ada31bb7603ce5acb45d6a0c2d2a18783524f8bb8e47"
PART_SHA256 = {
    "run_q80_year.part01.b64": "286550fab585a79bb11d2386d1555051b302dccb22a44114359e492b85d764aa",
    "run_q80_year.part02.b64": "5ba792cdf23990d828bf80cb4b4ac5b9b6eaf3ae22d30f278f712e07fdebb474",
    "run_q80_year.part03.b64": "0b1cd83aa07b47b4209db83d3c756cdd6b3eecacd222e2513762948f126d2920",
    "run_q80_year.part04.b64": "2d5ba4408c37f269b1d5d910e3c354ae329127147a720c6c333a34dcb57c12ee",
    "run_q80_year.part05.b64": "8fbe64d7f71a260f131c729b04809309a30374863625c92d40b3aeb12a69fc06",
    "run_q80_year.part06.b64": "91bd48f74fe0f71563140573416eaef682f010be0b931f123472c288dbc59b6f",
    "run_q80_year.part07.b64": "cb09394ea97852ffbb3c9b4082cabad85f5e88260665f28ea41fb7bed0f4bad0",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    payload = bytearray()
    for name, expected in PART_SHA256.items():
        encoded = (PART_DIR / name).read_text(encoding="ascii").strip()
        raw = base64.b64decode(encoded, validate=True)
        observed = sha256(raw)
        if observed != expected:
            raise RuntimeError(f"chunk hash mismatch: {name}: {observed}")
        payload.extend(raw)
    observed = sha256(bytes(payload))
    if observed != EXPECTED_SHA256:
        raise RuntimeError(f"runner hash mismatch: {observed}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_bytes(payload)
    print(f"PASS {OUT_FILE} SHA256={observed}")


if __name__ == "__main__":
    main()
