# Meesho Reseller Growth & Alert Intelligence Pipeline

IIT Roorkee capstone project implementing an offline, repeatable monthly reseller-growth monitoring workflow.

## What this project does

The pipeline follows:

**Part 1 → Part 2 → Part 3 → Part 4**

- **Part 1:** Generate the supplied seeded dataset and answer the five SQL business questions.
- **Part 2:** Validate Part 1's monthly category revenue feed and calculate month-over-month growth using a numeric 20% absolute-change threshold.
- **Part 3:** Turn only verified Part 2 numbers into a deterministic stakeholder narrative. No LLM or API is required.
- **Part 4:** Run the workflow as Intake → Summary → Report Draft → Validate, then stop at human approval.

## Requirements

- Python 3.10+ recommended.
- No external Python packages.
- No API key.
- No paid service.

## Run in order

From the repository root:

### 1. Generate the exact seeded dataset

```bash
python data/generate_dataset.py
```

Expected files:

- `data/resellers.csv` — 24 resellers
- `data/orders.csv` — 900 orders (300 each for April, May and June 2026)
- `data/meesho_reseller.db` — SQLite database

The seed and generation logic are kept unchanged from the project brief.

### 2. Run Part 1 SQL outputs

```bash
python part1_sql/run_queries.py
```

Creates:

- `part1_sql/output/monthly_category_revenue.csv`
- `part1_sql/output/region_revenue.csv`
- `part1_sql/output/top_resellers.csv`
- `part1_sql/output/zero_order_resellers.csv`
- `part1_sql/output/zero_order_count_diagnostic.csv`
- `part1_sql/output/june_delivered_aov.csv`

The key hand-off file is `monthly_category_revenue.csv`.

### 3. Run Part 2

```bash
python part2_engine/growth_engine.py
```

Output:

`part2_engine/growth_output.csv`

Run its tests:

```bash
python -m unittest part2_engine/test_growth_engine.py
```

### 4. Run Part 3

```bash
python part3_narrative/masking.py
```

Output:

`part3_narrative/narrative_report.md`

Run its tests:

```bash
python -m unittest part3_narrative/test_masking.py
```

### 5. Run Part 4

```bash
python part4_agent/mock_agent_runner.py
```

The runner repeats the hand-off sequence and ends with:

`PENDING_HUMAN_APPROVAL`

It never publishes a report automatically.

## Pipeline mapping

| Part | Workflow role |
|---|---|
| Part 1 | Compute real business numbers with SQL first |
| Part 2 | Validate the hand-off and quantify significant change |
| Part 3 | Convert verified numbers into a safe narrative |
| Part 4 | Orchestrate Intake → Summary → Report Draft → Validate → Human approval |

## Reproducibility

The dataset generator uses the supplied `random.Random(42)` seed, fixed reseller counts, category weights, price ranges and order counts. Regenerating the dataset therefore produces the same data.

## Zero-key operation

The complete pipeline is designed to work with **zero API keys**, paid services, hosted accounts, or external Python packages. The narrative step is a deterministic template-fill function.

## Academic-integrity note

The implementation uses Python standard-library modules such as `random`, `sqlite3`, `csv`, `pathlib`, `subprocess`, `unittest`, and `re`. Official Python documentation may be consulted for these standard-library modules as permitted by the brief.

## Repository submission

The IIT Roorkee brief asks for one public GitHub repository link as the submission. The repository should remain public so the evaluator can access it.
