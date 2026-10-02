# Prompt / Narrative Safety Pack

## Purpose
Convert only verified Part 2 metrics into a concise stakeholder update.

## Evidence contract
1. Read only `part2_engine/growth_output.csv`.
2. Never invent, estimate, round beyond the supplied display rule, or add a number not present in the verified feed.
3. State the 20% absolute MoM threshold explicitly.
4. Preserve caveats: simulated data and human review.
5. If a field is missing or validation fails, stop instead of drafting.

## Offline implementation
`masking.py` is a deterministic template-fill implementation. It does not call an LLM, use an API key, or require a paid service.

## Narrative structure
- Executive summary
- Significant June movements
- Caveats / human-review note
