# MENYELAM

**Strict bug bounty hunting methodology: NO RAW, NO CLAIM.**

MENYELAM (Indonesian for "to dive") is a disciplined framework for web bug bounty hunting. Its core principle: *you are wrong until raw evidence proves otherwise.* Your job is not to find bugs — it is to **fail as hard as possible at disproving your own findings**.

## The Laws

1. **NO RAW, NO CLAIM.** Raw = unedited request/response pairs, transaction data, or tool output. Screenshots alone don't count.
2. **Explicit status required:** `[CONFIRMED]` / `[UNTESTED]` / `[UNCONFIRMED]` / `[BY-DESIGN]` / `[BLOCKED]`. Ambiguous language is forbidden.
3. **No hedge words** (maybe/probably/seems/likely). Replace with raw evidence or `[UNKNOWN]`.
4. `[CONFIRMED]` requires ALL of: 3 reproductions under different conditions + raw evidence for each + passing self-adversarial review. Missing one = automatically `[UNCONFIRMED]`.
5. `[BLOCKED]` is invalid until at least 6 variations have been tried and failed, each with raw evidence.
6. `[BY-DESIGN]` requires: Intent + Boundary + Consequence analysis, raw evidence, and at least one documented attempt to prove it wrong.
7. **Never test out of scope.** When in doubt → STOP, mark `[ASSUMPTION]`, ask the official channel.
8. **Never write conclusions before all STOP conditions are met.**

## Workflow

```
L0: READ THE PROGRAM → scope, rules of engagement, severity, format, channel, embargo, duplicates, SLA
FILTER every signal → Intent? Boundary? Consequence? → BUG or by-design
HUNT: MAP all surfaces → HYPOTHESIZE per surface → TEST one variable at a time → 20+ ANGLES per signal
ROOT CAUSE → E2E to visible impact in raw evidence
MATRIX: every surface gets a final status. No row left without one.
```

## Repository Structure

- `METHODOLOGY.md` — the full methodology
- `recon/` — lightweight recon toolkit (subdomain enum, JS endpoint discovery, header/probe checks)
- `phases/` — phased hunting prompts (00–10) for systematic coverage

## Quick Start

```bash
# 1. Recon
python3 recon/recon.py example.com

# 2. JS endpoint discovery
python3 recon/jsdiscover.py https://example.com

# 3. Follow phases/00-recon.md through phases/10-report.md
# 4. Track everything in your MATRIX with explicit statuses
```

## Philosophy

> Don't look for ways to finish fast. Look for ways your own finding is wrong — and when you fail to find one despite trying hard, only then may it be considered correct.

## License

MIT
