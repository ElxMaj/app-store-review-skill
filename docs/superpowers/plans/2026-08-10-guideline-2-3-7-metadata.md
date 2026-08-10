# Guideline 2.3.7 Metadata Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release v1.2.0 with a deterministic, field-aware Guideline 2.3.7 metadata check, evidence-calibrated rejection recovery, tighter skill instructions, and verified packages for every configured distribution.

**Architecture:** Keep the dependency-free Python scanner as the deterministic evidence layer. Add typed metadata inputs and whitelisted Fastlane discovery, emit high-confidence blockers separately from ambiguous warnings, and expose scan coverage in schema 1.1. Keep policy interpretation in the skill references, then package the canonical files through intentional compatibility wrappers.

**Tech Stack:** Python 3.11 standard library, `unittest`, Markdown skill references, JSON plugin manifests and evals, GitHub Actions, Tessl CLI, ZIP `.skill` archive.

## Global Constraints

- Release version is `1.2.0`; report schema version is `1.1`; policy verification date is `2026-08-10`.
- Stable blocker ID is `ASR-METADATA-PRICE-237`; ambiguous warning ID is `ASR-METADATA-PRICE-237-REVIEW`.
- Deterministic evidence never contains matched metadata text, credentials, email addresses, app names copied from metadata, or prompt-injection strings.
- Only `name`, `subtitle`, `keywords`, and `promotional_text` run the presence-only price rule. `description` and `release_notes` are covered but excluded from that rule.
- English lexical detection is labeled incomplete for other languages. Local files never prove live App Store Connect state.
- Screenshot and preview price text is a contextual visual check, not an invented caption-field scan.
- The initial pass remains read-only. Fixes remain grouped and approval-gated.
- Preserve the uncommitted ClaudePluginHub badge when README changes are integrated.
- Do not publish a higher Tessl score until a live Tessl review reports it.

---

### Task 1: Typed metadata discovery and pricing findings

**Files:**
- Modify: `scripts/tests/test_app_store_review_scan.py`
- Modify: `scripts/app_store_review_scan.py`

**Interfaces:**
- `ScanContext(..., metadata_specs: Sequence[str] = (), metadata_roots: Sequence[Path] = ())`
- `MetadataInput(path: Path, field: str, locale: str, display_path: str)`
- `parse_metadata_spec(value: str, root: Path) -> MetadataInput`
- `collect_metadata_inputs(ctx: ScanContext) -> None`
- `scan_metadata_pricing(ctx: ScanContext) -> None`
- CLI: repeatable `--metadata FIELD[:LOCALE]=PATH` and repeatable `--metadata-root PATH`
- Report: `schema_version: "1.1"` and `metadata_scan` with `files_scanned`, sorted `fields`, sorted `locales`, and sorted `pricing_rule_fields`

- [ ] **Step 1: Add failing Fastlane and finding-calibration tests**

Add test helpers that pass `metadata_specs` and `metadata_roots` into `ScanContext`. Add table-driven tests proving:

```text
BLOCKER: 100% free, always free, completely free, free trial, free-to-play,
         free to use, at no cost, on sale, 20% off, 20％ off, save $5,
         $9.99, 9,99 €, USD 9.99, 9.99 EUR
WARNING: a standalone ambiguous "free"
NO FINDING: ad-free, gluten-free, hands-free, freeform, freestyle,
            point of sale, sales tax, discount calculator
```

Use `fastlane/metadata/en-US/subtitle.txt`, plus name, keywords, and promotional-text cases. Assert exact IDs, severity, guideline `2.3.7`, confidence `official`, and signals such as `Pricing-language rule matched; field=subtitle; locale=en-US; category=free-claim`. Assert the raw matched text is absent from serialized JSON.

- [ ] **Step 2: Run the new tests and confirm RED**

Run:

```bash
python3 -m unittest scripts.tests.test_app_store_review_scan.ScannerTests.test_fastlane_metadata_price_claims -v
```

Expected: failure because metadata inputs and `ASR-METADATA-PRICE-237` do not exist.

- [ ] **Step 3: Add failing input, coverage, privacy, and determinism tests**

Cover all of these cases:

```text
default/subtitle.txt reports locale default
description.txt and release_notes.txt appear in coverage but never trigger the price rule
review_information/demo_password.txt and unknown text files are ignored
explicit description:en-US=/path/file.txt is recognized without filename inference
duplicate auto-discovered and explicit files produce one evidence item
reversed metadata arguments and reverse-created locale directories yield identical
findings and metadata_scan after generated_at is removed
more than 20 matching locales reports stable evidence_total and evidence_omitted
malformed spec, unsupported field, missing file, and directory-as-file are errors
```

- [ ] **Step 4: Implement metadata data structures and strict discovery**

Add frozen `MetadataInput`. Parse `FIELD[:LOCALE]=PATH` with a strict field enum and default explicit locale `unspecified`. Resolve and validate paths without reading directories. Auto-discover only direct whitelisted filenames below locale directories in `<project>/fastlane/metadata`; accept extra roots via `--metadata-root`. Sort roots, locale directories, filenames, and explicit inputs. Deduplicate by resolved physical path plus field and locale. Use stable project-relative paths or `external-metadata/<locale>/<field>/<filename>` aliases for outside-root evidence.

- [ ] **Step 5: Implement normalized high-precision rules**

Normalize with `unicodedata.normalize("NFKC", text).casefold()` and normalize Unicode dash and spacing variants before regex matching. Keep explicit category names:

```python
PRICE_CATEGORIES = (
    "free-claim",
    "no-cost-claim",
    "discount-claim",
    "percent-off",
    "save-amount",
    "currency-amount",
)
```

Emit one blocker finding for high-precision categories and one warning for ambiguous standalone `free`. Exclude specified compounds and non-price phrases. Store no excerpts. Sort evidence by `(path, line, signal)`, cap rendered evidence at 20, and expose total and omitted counts.

- [ ] **Step 6: Wire schema, manual checks, and CLI errors**

Call metadata collection and scanning from `run_scan`. Add `metadata_scan` even when zero files are found. Add a manual check that descriptions, release notes, screenshots, and previews still need contextual accuracy review. In `main`, convert metadata parsing `ValueError` into `parser.error(...)`. Add help text for both repeatable arguments.

- [ ] **Step 7: Run scanner and renderer tests**

Run:

```bash
python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v
python3 scripts/app_store_review_scan.py . --format json | python3 -m json.tool >/dev/null
```

Expected: all tests pass and the JSON smoke test exits 0.

- [ ] **Step 8: Commit Task 1**

```bash
git add scripts/app_store_review_scan.py scripts/tests/test_app_store_review_scan.py
git commit -m "feat: detect App Store metadata price claims"
```

---

### Task 2: Policy guidance, recovery fixture, and Tessl-focused skill cleanup

**Files:**
- Modify: `SKILL.md`
- Modify: `references/guidelines-checklist.md`
- Modify: `references/rejection-playbook.md`
- Modify: `references/report-contract.md`
- Modify: `references/evidence-policy.md` only if a date statement requires it
- Modify: `README.md`
- Modify: `evals/evals.json`
- Create: `evals/rejection-recovery-metadata/task.md`
- Create: `evals/rejection-recovery-metadata/scenario.json`
- Create: `evals/rejection-recovery-metadata/criteria.json`
- Create: `evals/rejection-recovery-metadata/inputs/rejection-details.md`

**Interfaces:**
- Mode B still begins with the exact Apple message and exactly one `Response classification:` line.
- The anonymized fixture cites Guideline 2.3.7, names `subtitle`, and supplies subtitle copy `Always free job alerts`.
- The report contract documents schema `1.1`, scanner `1.2.0`, and `metadata_scan`.

- [ ] **Step 1: Add the failing eval contract**

Create an anonymized rejection fixture with no developer name, email, submission ID, real app name, or screenshot. Require the response to:

```text
preserve Apple's complete supplied message
classify the proven case as FIX
map it to 2.3.7
remove equivalent claims only where they occur after inspecting every live subtitle localization
check localization fallback assets
allow accurate, relevant price-change copy in the description without declaring all description pricing safe
say a new build is normally unnecessary only when no binary or bundled configuration changed and App Store Connect permits the edit
draft a factual reply naming only verified locales and changes
avoid appeal, invented binary work, and a blanket description ban for this fixture
```

Add the scenario to `evals/evals.json` and validate all JSON files with `python3 -m json.tool`.

- [ ] **Step 2: Add the 2.3.7 field-and-context matrix**

In `references/guidelines-checklist.md`, distinguish direct price advertising in name, subtitle, keywords, and promotional text from contextual screenshot/preview UI, descriptions, release notes, and expected commerce fields. State the English-only detector limit and require inspection of every live localization and fallback asset.

- [ ] **Step 3: Add evidence-calibrated rejection recovery**

In `references/rejection-playbook.md`, add the dedicated price-reference mapping and this conditional same-build rule:

```text
If only editable App Store metadata or product-page assets changed, and no binary
or bundled configuration changed, a new build is normally unnecessary. Confirm
that the current App Store Connect status permits the edit, retain the selected
build, and resubmit the rejected item or app version.
```

Keep `CLARIFY`, `REQUEST INTERPRETATION`, and `APPEAL` available when the cited field is wrong, missing, or contextually legitimate. The reply template names only verified fields, locales, version, build, and attachments.

- [ ] **Step 4: Update the report contract and policy dates**

Document `metadata_scan`, `evidence_total`, and `evidence_omitted`; update the sample scanner version to `1.2.0` and schema to `1.1`. Change bundled policy verification dates to `2026-08-10` only where current Apple sources were checked.

- [ ] **Step 5: Tighten the canonical skill for Tessl quality**

Reduce `SKILL.md` from 261 lines to no more than 220 lines without removing behavior. Keep one output-gates section, the read-only and approval gates, mode selection, evidence labels, copy-paste scanner and renderer commands, and current-policy checks. Replace repeated Mode A, Mode B, Mode C, report-field, and reviewer-path details with direct instructions to read the corresponding reference completely. Do not replace exact output contracts that the agent must print.

- [ ] **Step 6: Update README while retaining the existing badge**

Keep the ClaudePluginHub badge already present in the worktree. Update the guidelines badge and stated policy date to `2026-08-10`, add the typed metadata command syntax where scanner usage is documented, and keep the README under 130 lines with no em dash.

- [ ] **Step 7: Validate docs and evals**

Run:

```bash
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool evals/rejection-recovery-metadata/scenario.json >/dev/null
python3 -m json.tool evals/rejection-recovery-metadata/criteria.json >/dev/null
test "$(wc -l < SKILL.md | tr -d ' ')" -le 220
! rg -n '—' README.md
rg -n '2026-08-10|ASR-METADATA-PRICE-237|Guideline 2.3.7' SKILL.md references README.md evals
```

Expected: JSON validation passes, `SKILL.md` is at most 220 lines, README contains no em dash, and policy/finding references are present.

- [ ] **Step 8: Commit Task 2**

```bash
git add SKILL.md references README.md evals
git commit -m "docs: add Guideline 2.3.7 recovery workflow"
```

---

### Task 3: Versioned packages, archive, and release validation

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`
- Modify: `.tessl-plugin/plugin.json`
- Modify: `copilot-plugin/.github/plugin/plugin.json`
- Modify: `copilot-plugin/skills/app-store-review/SKILL.md`
- Modify: `copilot-plugin/skills/app-store-review/references/*.md`
- Modify: `copilot-plugin/skills/app-store-review/scripts/*.py`
- Modify: `.github/workflows/validate.yml`
- Create: `scripts/tests/test_package_consistency.py`
- Rebuild: `app-store-review-skill.skill`

**Interfaces:**
- All four manifest versions and both scanner copies report `1.2.0`.
- Root references equal Copilot references and archive references byte-for-byte.
- Root scanner and renderer equal Copilot and archive scripts byte-for-byte.
- Archive `SKILL.md` equals root `SKILL.md` byte-for-byte.
- Compatibility loader remains a functional pointer to `../../SKILL.md`.
- Copilot skill equals the canonical body plus its existing `Packaged resources` appendix.

- [ ] **Step 1: Write failing package-consistency tests**

Add tests that parse every manifest, inspect ZIP members, compare the intentional matrix above, assert scanner and report-contract sample versions, verify the compatibility loader, and verify the Copilot appendix links every packaged reference and script. Assert the archive contains no test fixtures or private rejection evidence.

- [ ] **Step 2: Run package tests and confirm RED**

Run:

```bash
python3 -m unittest scripts.tests.test_package_consistency -v
```

Expected: failure because manifests and scanner are not `1.2.0`, mirrors are stale, and the archive has not been rebuilt.

- [ ] **Step 3: Synchronize intentional package copies**

Copy root references and scripts into the Copilot package. Rebuild the Copilot `SKILL.md` as the complete canonical body followed by the existing `## Packaged resources` appendix. Leave `skills/app-store-review/SKILL.md` as the compatibility loader. Update all four manifests to `1.2.0`.

- [ ] **Step 4: Rebuild the portable archive**

Create a temporary `app-store-review/` directory containing root `SKILL.md`, `references/`, `scripts/`, and `agents/openai.yaml`. Build `app-store-review-skill.skill` as a ZIP without filesystem-owner metadata, then inspect it with:

```bash
unzip -t app-store-review-skill.skill
unzip -l app-store-review-skill.skill
```

- [ ] **Step 5: Strengthen CI validation**

Keep existing unit, JSON smoke, and ZIP integrity steps. Add explicit JSON validation for the manifests and eval files; package-consistency tests are included through unittest discovery. Do not describe this as a security scan.

- [ ] **Step 6: Run complete local validation**

Run:

```bash
python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v
python3 scripts/app_store_review_scan.py . --format json | python3 -m json.tool >/dev/null
python3 -m json.tool tessl.json >/dev/null
python3 -m json.tool .tessl-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool copilot-plugin/.github/plugin/plugin.json >/dev/null
unzip -t app-store-review-skill.skill
tessl plugin lint .
```

Expected: every command exits 0.

- [ ] **Step 7: Commit Task 3**

```bash
git add .claude-plugin .codex-plugin .tessl-plugin copilot-plugin .github/workflows/validate.yml scripts/tests/test_package_consistency.py app-store-review-skill.skill
git commit -m "release: package app-store-review v1.2.0"
```

---

### Task 4: Final review, merge, and publication

**Files:**
- Review all changes from `origin/main` through the release commit.
- Create tag: `v1.2.0`
- Attach: `app-store-review-skill.skill`

**Interfaces:**
- GitHub default branch contains all v1.2.0 files.
- Tessl package is `maj-labs/app-store-review@1.2.0`.
- GitHub Release title is `v1.2.0` and includes the portable `.skill` artifact.

- [ ] **Step 1: Run an independent whole-branch review**

Review policy accuracy, scanner false positives, secret handling, deterministic output, eval discrimination, package consistency, README claims, and the diff against `origin/main`. Resolve every blocking or important finding and rerun affected tests.

- [ ] **Step 2: Verify the exact release candidate**

Run all Task 3 validation commands again from a clean worktree. Confirm `git status --short` contains no untracked or unstaged release files and `git diff --check origin/main...HEAD` is clean.

- [ ] **Step 3: Merge and push main**

Fetch current `origin/main`, integrate without dropping the v1.1.6 human-craft changes or ClaudePluginHub badge, fast-forward or merge into local `main`, and push `main`. Never force-push main.

- [ ] **Step 4: Tag and publish GitHub Release**

Create annotated tag `v1.2.0`, push it, and create a GitHub Release whose notes state the new 2.3.7 metadata audit, evidence-calibrated recovery, and Tessl-quality cleanup without claiming a higher live score. Attach `app-store-review-skill.skill`.

- [ ] **Step 5: Publish and evaluate on Tessl**

Publish `maj-labs/app-store-review@1.2.0` with scenario quality checks or confirm the GitHub workflow succeeded. Request a fresh Tessl quality and impact review, then record the live score and factor only after Tessl reports them.

- [ ] **Step 6: Confirm remaining distribution surfaces**

Verify GitHub installation instructions for Claude Code, Codex, GitHub Copilot, and `npx skills add`. Check ClaudePluginHub after the GitHub release; request a refresh only if it does not ingest the new version automatically. Pause for confirmation immediately before submitting any public browser form.
