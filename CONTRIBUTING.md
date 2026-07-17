# Contributing

Contributions should improve evidence quality or reduce false positives.

## New rejection cases

Add the case to `references/evidence-policy.md`. Include the guideline number, Apple's exact wording when available, source date and URL, every material change before resubmission, and the final outcome. Update `references/rejection-playbook.md` only when the case changes a recovery recommendation. A rejection report without an outcome should not be presented as a successful remediation.

## Check improvements and false positives

Policy or manual-check changes belong in `references/guidelines-checklist.md`. Framework-specific interpretation belongs in `references/frameworks.md`. Deterministic checks and false-positive fixes belong in `scripts/app_store_review_scan.py` with a regression test in `scripts/tests/test_app_store_review_scan.py`.

Run before opening a pull request:

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/app_store_review_scan.py . --format json | python3 -m json.tool >/dev/null
```

Do not add approval-rate claims, unattributed rejection text, or guesses about Apple's internal detection system.
