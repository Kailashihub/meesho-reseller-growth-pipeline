"""Part 2: validated growth engine.

The engine consumes Part 1's monthly_category_revenue.csv and applies a
numeric rule for "significant change":
    absolute MoM revenue growth >= 20%.

Rules:
- First month for a category has no prior month, so growth is None.
- Zero previous revenue with positive current revenue is treated as +inf.
- Zero previous and zero current revenue is treated as 0.0.
- Input schema, numeric fields, duplicate month/category rows and month order
  are validated before calculations.
"""

from __future__ import annotations
import csv
from pathlib import Path

REQUIRED_COLUMNS = ["month", "category", "revenue", "n_orders"]
MONTH_ORDER = {"April": 0, "May": 1, "June": 2}
DEFAULT_THRESHOLD = 0.20

class ValidationError(ValueError):
    pass

def load_feed(path: str | Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        raise ValidationError(f"Input file does not exist: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValidationError(
                f"Expected columns {REQUIRED_COLUMNS}, got {reader.fieldnames}"
            )
        rows = list(reader)

    if not rows:
        raise ValidationError("Input feed is empty.")

    seen = set()
    for i, row in enumerate(rows, start=2):
        key = (row["month"], row["category"])
        if key in seen:
            raise ValidationError(f"Duplicate month/category at CSV row {i}: {key}")
        seen.add(key)

        if row["month"] not in MONTH_ORDER:
            raise ValidationError(f"Unsupported month at CSV row {i}: {row['month']}")

        try:
            revenue = float(row["revenue"])
            n_orders = int(row["n_orders"])
        except (TypeError, ValueError):
            raise ValidationError(f"Non-numeric revenue/order count at CSV row {i}")

        if revenue < 0 or n_orders < 0:
            raise ValidationError(f"Negative revenue/order count at CSV row {i}")

        row["revenue"] = revenue
        row["n_orders"] = n_orders

    return rows

def calculate_growth(rows: list[dict], threshold: float = DEFAULT_THRESHOLD) -> list[dict]:
    if not (0 <= threshold <= 1):
        raise ValueError("threshold must be between 0 and 1")

    by_category = {}
    for row in rows:
        by_category.setdefault(row["category"], []).append(row)

    results = []
    for category, items in by_category.items():
        items.sort(key=lambda r: MONTH_ORDER[r["month"]])
        previous = None
        for row in items:
            current = row["revenue"]
            if previous is None:
                growth = None
            elif previous == 0:
                growth = float("inf") if current > 0 else 0.0
            else:
                growth = (current - previous) / previous

            significant = growth is not None and abs(growth) >= threshold
            results.append({
                "month": row["month"],
                "category": category,
                "revenue": round(current, 2),
                "n_orders": row["n_orders"],
                "mom_growth": growth,
                "significant_change": significant,
            })
            previous = current

    return sorted(results, key=lambda r: (MONTH_ORDER[r["month"]], r["category"]))

def run(input_path: str | Path, output_path: str | Path, threshold: float = DEFAULT_THRESHOLD) -> list[dict]:
    rows = load_feed(input_path)
    results = calculate_growth(rows, threshold)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        fields = ["month","category","revenue","n_orders","mom_growth","significant_change"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            growth = r["mom_growth"]
            if growth == float("inf"):
                growth_value = "inf"
            elif growth is None:
                growth_value = ""
            else:
                growth_value = f"{growth:.6f}"
            w.writerow({
                "month": r["month"],
                "category": r["category"],
                "revenue": f"{r['revenue']:.2f}",
                "n_orders": r["n_orders"],
                "mom_growth": growth_value,
                "significant_change": str(r["significant_change"]).lower(),
            })
    return results

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    inp = root / "part1_sql" / "output" / "monthly_category_revenue.csv"
    out = root / "part2_engine" / "growth_output.csv"
    result = run(inp, out)
    alerts = [r for r in result if r["significant_change"]]
    print(f"Validated {len(result)} rows; significant changes: {len(alerts)}")
