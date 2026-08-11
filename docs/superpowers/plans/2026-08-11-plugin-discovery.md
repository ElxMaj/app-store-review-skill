# Plugin Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a detected install guide and a real Claude Code command that delegates to the existing App Store review skill.

**Architecture:** Keep user documentation at the repository root and add one flat plugin command at `commands/review.md`. The command is an adapter only. Existing skill files remain the source of review behavior.

**Tech Stack:** Markdown, Claude Code plugin manifests, Python `unittest`, GitHub Actions.

## Global Constraints

- README must remain below 130 lines.
- No hooks, MCP servers, or agents may be added for score alone.
- The command must delegate to `app-store-review:app-store-review` and preserve `$ARGUMENTS`.
- All release manifests and packaged version markers must use `1.2.1`.

---

### Task 1: Install and command contract

**Files:**
- Create: `INSTALL.md`
- Create: `commands/review.md`
- Modify: `README.md`
- Modify: `scripts/tests/test_package_consistency.py`

**Interfaces:**
- Consumes: Claude Code's plugin skill namespace and `$ARGUMENTS` substitution.
- Produces: `/app-store-review:review <request>` and copyable installation paths.

- [ ] Add failing tests that require the command to name `app-store-review:app-store-review`, include `$ARGUMENTS`, keep workflow details out of the adapter, and require all four install routes in `INSTALL.md`.
- [ ] Run the focused test and confirm it fails because the two files do not exist.
- [ ] Add the minimal command, install guide, and README copy.
- [ ] Run the focused test and confirm it passes.

### Task 2: Patch release synchronization

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`
- Modify: `.tessl-plugin/plugin.json`
- Modify: `copilot-plugin/.github/plugin/plugin.json`
- Modify: `scripts/app_store_review_scan.py`
- Modify: `copilot-plugin/skills/app-store-review/scripts/app_store_review_scan.py`
- Modify: `references/report-contract.md`
- Modify: `examples/parceltrack-report.json`
- Modify: `examples/parceltrack-report.html`
- Modify: `app-store-review-skill.skill`
- Modify: `scripts/tests/test_package_consistency.py`

**Interfaces:**
- Consumes: the existing deterministic packaging contract.
- Produces: consistent version `1.2.1` across registry and report surfaces.

- [ ] Change the test expectation to `1.2.1` and confirm the focused version test fails against `1.2.0`.
- [ ] Update version markers, regenerate the report HTML, synchronize the Copilot copy, and rebuild the `.skill` archive deterministically.
- [ ] Run package consistency and confirm it passes.

### Task 3: End-to-end verification

**Files:**
- Verify: all modified files.

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: a release candidate ready for a protected-branch pull request.

- [ ] Run `claude plugin validate .`.
- [ ] Load the plugin locally and inspect its component inventory.
- [ ] Run all Python unit tests.
- [ ] Check README line count, JSON parsing, archive contents, git diff, and secret scan.
- [ ] Commit the release candidate, push the branch, open a pull request, wait for checks, and merge only when protection permits.
