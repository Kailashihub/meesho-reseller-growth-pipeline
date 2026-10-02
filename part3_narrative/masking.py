"""Part 3: deterministic, evidence-bound narrative generation.

No LLM/API is used. The narrative is generated only from verified Part 2
rows. The masking helpers remove accidental raw numeric-looking tokens from
free text; the report itself is built from structured values rather than
free-form model output.
"""

from __future__ import annotations
import csv
import re
from pathlib import Path

def mask_unverified_numbers(text: str, allowed_numbers: set[str] | None = None) -> str:
    allowed_numbers = allowed_numbers or set()
    pattern = re.compile(r"(?<![\w])(?:₹\s*)?\d+(?:,\d{3})*(?:\.\d+)?%?")
    def repl(match):
        token = match.group(0)
        normalized = token.replace("₹", "").replace(",", "").strip()
        if normalized in allowed_numbers:
            return token
        return "[MASKED]"
    return pattern.sub(repl, text)

def load_growth(path: str | Path) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _fmt_pct(value: str) -> str:
    if value in ("", None):
        return "n/a"
    if value == "inf":
        return "from zero"
    return f"{float(value) * 100:.1f}%"

def build_report(growth_csv: str | Path) -> str:
    rows = load_growth(growth_csv)
    june = [r for r in rows if r["month"] == "June"]
    alerts = [r for r in june if r["significant_change"].lower() == "true"]

    lines = [
        "# Meesho Reseller Growth & Alert Intelligence — Monthly Update",
        "",
        "## Executive summary",
        f"- The June feed contains {len(june)} category observations.",
        f"- The growth rule flags {len(alerts)} June category movements at or above the 20% absolute month-over-month threshold.",
        "- Figures below are copied from the validated Part 2 output; no external or invented values are introduced.",
        "",
        "## Significant June movements",
    ]
    if not alerts:
        lines.append("- No June movements met the configured threshold.")
    else:
        for r in alerts:
            direction = "increased" if float(r["mom_growth"]) > 0 else "decreased"
            lines.append(
                f"- **{r['category']}**: revenue {direction} by {_fmt_pct(r['mom_growth'])} "
                f"to {float(r['revenue']):,.2f}, based on {r['n_orders']} orders."
            )

    lines += [
        "",
        "## Caveats",
        "- The threshold is an explicit rule, not a claim that every flagged movement is operationally important.",
        "- This dataset contains April–June 2026 simulated records generated from the supplied seeded script.",
        "- Human review is required before external distribution.",
    ]
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    source = root / "part2_engine" / "growth_output.csv"
    report = build_report(source)
    (root / "part3_narrative" / "narrative_report.md").write_text(report, encoding="utf-8")
    print("Narrative report written.")
