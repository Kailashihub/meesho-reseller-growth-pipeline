"""Optional convenience runner for the whole offline pipeline."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
commands = [
    [sys.executable, str(ROOT / "data" / "generate_dataset.py")],
    [sys.executable, str(ROOT / "part1_sql" / "run_queries.py")],
    [sys.executable, str(ROOT / "part2_engine" / "growth_engine.py")],
    [sys.executable, str(ROOT / "part3_narrative" / "masking.py")],
    [sys.executable, str(ROOT / "part4_agent" / "mock_agent_runner.py")],
]
for command in commands:
    subprocess.run(command, check=True)
print("FULL PIPELINE PASSED")
