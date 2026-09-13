from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_exact_worker_runs_one_day_m1_and_writes_validated_outputs(tmp_path):
    cmd = [
        sys.executable, str(ROOT / 'scripts' / 'run_exact_common_worker.py'),
        '--root', str(ROOT),
        '--forecast', str(ROOT / 'inputs' / 'F0_L2_P3_annual_forecast.csv'),
        '--model', 'M1',
        '--start-date', '2025-02-01',
        '--end-date', '2025-02-01',
        '--output-dir', str(tmp_path),
        '--label', 'TEST_M1',
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr + proc.stdout
    summary = json.loads((tmp_path / 'TEST_M1_summary.json').read_text())
    validator = json.loads((tmp_path / 'TEST_M1_validator.json').read_text())
    assert summary['days'] == 1
    assert summary['slots'] == 144
    assert validator['status'] == 'PASS'
    assert summary['fallback_count'] == 0
