# Part 4 — Agent Specification

## Goal
Run the monthly reseller-monitoring workflow as a guarded, repeatable process.

## Workflow
1. **Intake** — locate the Part 1 monthly category revenue CSV.
2. **Summary** — invoke the Part 2 validation/growth engine with the configured 20% threshold.
3. **Report Draft** — generate the Part 3 deterministic narrative from the verified output.
4. **Validate** — confirm required files exist, row counts are sensible, and the narrative contains the human-review gate.
5. **Human approval** — the mock runner prints `PENDING_HUMAN_APPROVAL`; it does not publish or send the report automatically.

## Guardrails
- No API key is required.
- No external service is called.
- Invalid or corrupted input stops the workflow before narrative generation.
- Part 3 may only consume validated Part 2 output.
- The runner never auto-publishes a report.

## Inputs / outputs
- Input: `part1_sql/output/monthly_category_revenue.csv`
- Intermediate: `part2_engine/growth_output.csv`
- Draft: `part3_narrative/narrative_report.md`
- Status: console output from `mock_agent_runner.py`

## Human review
The final state is intentionally `PENDING_HUMAN_APPROVAL`. A real production implementation could place an approval task in an approved workflow system, but this capstone uses an offline mock.
