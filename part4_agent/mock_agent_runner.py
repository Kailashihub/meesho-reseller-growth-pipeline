from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PART1 = ROOT / "part1_sql" / "output" / "monthly_category_revenue.csv"
PART2 = ROOT / "part2_engine" / "growth_engine.py"
PART2_OUT = ROOT / "part2_engine" / "growth_output.csv"
PART3 = ROOT / "part3_narrative" / "masking.py"
REPORT = ROOT / "part3_narrative" / "narrative_report.md"

def main():
    print("[1/4] Intake: checking Part 1 output")
    if not PART1.exists():
        raise SystemExit(f"STOP: missing input {PART1}")

    print("[2/4] Summary: validating and calculating growth")
    subprocess.run([sys.executable, str(PART2)], check=True)

    if not PART2_OUT.exists():
        raise SystemExit("STOP: Part 2 output was not created")

    print("[3/4] Report Draft: generating deterministic narrative")
    subprocess.run([sys.executable, str(PART3)], check=True)

    print("[4/4] Validate: checking human-review gate")
    text = REPORT.read_text(encoding="utf-8")
    required = ["Human review", "simulated", "20%"]
    missing = [item for item in required if item.lower() not in text.lower()]
    if missing:
        raise SystemExit(f"STOP: narrative validation failed; missing {missing}")

    print("PENDING_HUMAN_APPROVAL")
    print(f"Draft: {REPORT}")
    print("No external publication or API call was performed.")

if __name__ == "__main__":
    main()
