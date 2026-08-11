# Release Maintenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the canonical report through GitHub Pages, monitor public registry freshness, remove Dependabot activity, and enforce protected pull-request changes for the repository owner.

**Architecture:** Two focused GitHub Actions workflows handle public report deployment and read-only registry monitoring. Repository settings and bot cleanup remain explicit post-merge GitHub operations, while all durable configuration stays versioned in the repository.

**Tech Stack:** GitHub Actions YAML, Bash, `curl`, `jq`, GitHub CLI, Python unittest, Ruby YAML parser, GitHub Pages.

## Global Constraints

- Do not modify `SKILL.md`, references, scanner behavior, eval content, the v1.2.0 archive, tag, or GitHub release.
- Derive registry versions from repository manifests instead of hard-coding `1.2.0`.
- Registry monitoring is read-only, requires no secrets, and never creates issues or republishes packages.
- Pin every third-party GitHub Action to an exact commit SHA.
- Apply administrator branch-protection enforcement only after the maintenance pull request is merged.

---

### Task 1: Publish the canonical report with GitHub Pages

**Files:**
- Create: `.github/workflows/pages.yml`
- Modify: `README.md`
- Test: local `_site` assembly plus YAML and link assertions

**Interfaces:**
- Consumes: `examples/parceltrack-report.html`, `examples/parceltrack-report.json`
- Produces: `https://elxmaj.github.io/app-store-review-skill/` and `https://elxmaj.github.io/app-store-review-skill/parceltrack-report.json`

- [ ] **Step 1: Record failing release-surface assertions**

Run:

```bash
test -f .github/workflows/pages.yml
rg -F 'https://elxmaj.github.io/app-store-review-skill/' README.md
```

Expected: the workflow file assertion fails and README contains no live Pages URL.

- [ ] **Step 2: Add the Pages workflow**

Create `.github/workflows/pages.yml` with:

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - ".github/workflows/pages.yml"
      - "README.md"
      - "examples/parceltrack-report.html"
      - "examples/parceltrack-report.json"
      - "scripts/render_app_store_report.py"
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
      - uses: actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b # v5
      - name: Assemble report site
        run: |
          mkdir -p _site
          cp examples/parceltrack-report.html _site/index.html
          cp examples/parceltrack-report.json _site/parceltrack-report.json
      - uses: actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b # v4
        with:
          path: _site
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e # v4
```

- [ ] **Step 3: Point README report links to Pages**

Wrap the existing preview image in a link to `https://elxmaj.github.io/app-store-review-skill/`. Change only the linked targets around the preview.

```markdown
[Open the complete sample report](https://elxmaj.github.io/app-store-review-skill/) · [Inspect its source JSON](https://elxmaj.github.io/app-store-review-skill/parceltrack-report.json)
```

- [ ] **Step 4: Verify the Pages artifact locally**

Run:

```bash
pages_stage=$(mktemp -d)
mkdir -p "$pages_stage/_site"
cp examples/parceltrack-report.html "$pages_stage/_site/index.html"
cp examples/parceltrack-report.json "$pages_stage/_site/parceltrack-report.json"
test -s "$pages_stage/_site/index.html"
python3 -m json.tool "$pages_stage/_site/parceltrack-report.json" >/dev/null
ruby -e 'require "yaml"; YAML.parse_file(".github/workflows/pages.yml")'
rg -F 'https://elxmaj.github.io/app-store-review-skill/' README.md
```

Expected: every command exits zero.

- [ ] **Step 5: Commit Task 1**

```bash
git add .github/workflows/pages.yml README.md
git commit -m "feat: publish the sample report with Pages"
```

### Task 2: Add read-only registry freshness monitoring

**Files:**
- Create: `scripts/check_registry_health.sh`
- Create: `scripts/tests/test_registry_health.py`
- Create: `.github/workflows/registry-health.yml`
- Modify: `.github/workflows/validate.yml`
- Test: `scripts/tests/test_registry_health.py`

**Interfaces:**
- Consumes: `.claude-plugin/plugin.json`, `.tessl-plugin/plugin.json`, public ClaudePluginHub HTML, public Tessl JSON API
- Produces: deterministic exit status and concise version/score output for local runs and GitHub Actions

- [ ] **Step 1: Write failing offline behavior tests**

Create `scripts/tests/test_registry_health.py`. Use temporary manifests and `file://` fixture responses to cover:

- matching ClaudePluginHub and Tessl versions succeed,
- a stale ClaudePluginHub version fails with a targeted mismatch,
- missing Tessl security or multiplier data fails.

Run:

```bash
python3 -m unittest scripts.tests.test_registry_health -v
```

Expected: failure because `scripts/check_registry_health.sh` does not exist.

- [ ] **Step 2: Implement the registry checker**

Create an executable `scripts/check_registry_health.sh` that:

1. enables `set -euo pipefail`,
2. derives both expected versions with `jq -r '.version'`,
3. downloads the ClaudePluginHub listing with retry and extracts the first structured `softwareVersion`,
4. downloads Tessl tile and exact-version API responses with retry,
5. verifies latest version, moderation, aggregate, impact, `securityLevel == "NONE"`, and a non-null multiplier,
6. prints observed values without printing response bodies,
7. exits nonzero with a targeted error for any mismatch.

Use these default endpoints exactly:

```text
https://www.claudepluginhub.com/plugins/elxmaj-app-store-review
https://api.tessl.io/v1/tiles/maj-labs/app-store-review
https://api.tessl.io/v1/tiles/maj-labs/app-store-review/versions/$expected_tessl_version
```

Support test-only environment overrides for both manifest paths and all three URLs. This keeps network access out of the unit suite while exercising the real script.

- [ ] **Step 3: Add the scheduled workflow**

Create `.github/workflows/registry-health.yml` with daily `08:17 UTC`, manual dispatch, `contents: read`, a five-minute timeout, pinned `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`, and one step running `scripts/check_registry_health.sh`.

- [ ] **Step 4: Make the offline behavior tests pass**

Run:

```bash
bash -n scripts/check_registry_health.sh
python3 -m unittest scripts.tests.test_registry_health -v
```

Expected: syntax passes and every offline success and failure case behaves as asserted.

- [ ] **Step 5: Add offline structural validation to Validate**

Add steps to `.github/workflows/validate.yml` that run:

```bash
bash -n scripts/check_registry_health.sh
ruby -e 'require "yaml"; Dir[".github/workflows/*.yml"].each { |path| YAML.parse_file(path) }'
```

The normal validation workflow must not call external registries.

- [ ] **Step 6: Record the current live registry state**

Run:

```bash
scripts/check_registry_health.sh
```

Expected on 2026-08-11: a targeted ClaudePluginHub version mismatch if its crawler still serves v1.1.4. Record that external state. Do not weaken the check or block the maintenance pull request on a third-party crawler delay.

- [ ] **Step 7: Commit Task 2**

```bash
git add scripts/check_registry_health.sh scripts/tests/test_registry_health.py .github/workflows/registry-health.yml .github/workflows/validate.yml
git commit -m "ci: monitor registry freshness"
```

### Task 3: Remove Dependabot and publish the maintenance pull request

**Files:**
- Delete: `.github/dependabot.yml`
- Test: repository status and GitHub pull-request state

**Interfaces:**
- Consumes: current Dependabot configuration and PRs #6 and #7
- Produces: no Dependabot configuration, no open Dependabot PRs, no remote Dependabot branches

- [ ] **Step 1: Remove Dependabot configuration**

Delete only `.github/dependabot.yml`, then verify:

```bash
test ! -e .github/dependabot.yml
```

- [ ] **Step 2: Run the full local release gate**

Run:

```bash
python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v
find evals -type f -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .tessl-plugin/plugin.json >/dev/null
unzip -t app-store-review-skill.skill
ruby -e 'require "yaml"; Dir[".github/workflows/*.yml"].each { |path| YAML.parse_file(path) }'
bash -n scripts/check_registry_health.sh
git diff --check origin/main...HEAD
```

Expected: all tests and every offline check pass. The live registry result is reported separately because crawler freshness is external state.

- [ ] **Step 3: Commit Dependabot removal**

```bash
git add .github/dependabot.yml
git commit -m "chore: disable Dependabot"
```

- [ ] **Step 4: Push and open a ready pull request**

```bash
git push -u origin agent/release-maintenance
gh pr create --base main --head agent/release-maintenance --title "Publish the live report and tighten repository maintenance" --body-file /private/tmp/app-store-review-maintenance-pr.md
maintenance_pr=$(gh pr view agent/release-maintenance --json number --jq .number)
gh pr ready "$maintenance_pr"
```

The PR body must describe Pages, registry monitoring, Dependabot removal, unchanged skill contents, and local checks.

- [ ] **Step 5: Enable GitHub Pages for workflow deployment**

Before merging the maintenance pull request, run:

```bash
gh api --method POST repos/ElxMaj/app-store-review-skill/pages -f build_type=workflow
```

Treat an existing Pages site as success only after verifying its `build_type` is `workflow`.

- [ ] **Step 6: Wait for required checks and merge**

```bash
maintenance_pr=$(gh pr view agent/release-maintenance --json number --jq .number)
gh pr checks "$maintenance_pr" --watch
gh pr merge "$maintenance_pr" --squash --delete-branch
```

Expected: `validate` passes before merge. Pages does not deploy until the merge reaches `main`.

- [ ] **Step 7: Close Dependabot pull requests**

Run for PRs #6 and #7:

```bash
gh pr close 6 --comment "Dependabot is being disabled for this repository, so this automated update will not be merged."
gh pr close 7 --comment "Dependabot is being disabled for this repository, so this automated update will not be merged."
```

Then delete only the two known remote branches after verifying their exact names from `gh pr view`.

- [ ] **Step 8: Disable automated security-update pull requests**

Check the repository's automated security-fix state. If enabled, disable automated security fixes through the GitHub API. Keep vulnerability alerts enabled so security findings remain visible without Dependabot opening pull requests.

### Reviewer follow-up: Preserve Action update visibility

Before publication, add `.github/scripts/check_action_pins.py`, its offline tests, and `.github/workflows/action-pin-health.yml`. The monthly workflow verifies each full Action SHA against its moving major-version tag without opening pull requests. Update existing pins to the current major tags, document quarterly major-version and advisory review plus GitHub's 60-day scheduled-workflow limitation in `CONTRIBUTING.md`, and keep vulnerability alerts enabled.

### Task 4: Complete deployment and enforce administrator protection

**Files:**
- No repository file changes
- Test: GitHub Pages, Actions, registry state, branch protection, remote refs

**Interfaces:**
- Consumes: merged maintenance commit and existing `main` protection
- Produces: live Pages report and `enforce_admins.enabled == true`

- [ ] **Step 1: Verify post-merge Actions**

Find the merged `main` SHA and verify the `Validate`, `Deploy GitHub Pages`, and any path-triggered publication workflows that ran for it. Every triggered workflow must complete successfully.

- [ ] **Step 2: Verify Pages over HTTPS**

Run:

```bash
curl -fsSL https://elxmaj.github.io/app-store-review-skill/ | rg -F 'Policy / 2026-08-10'
curl -fsSL https://elxmaj.github.io/app-store-review-skill/parceltrack-report.json | python3 -m json.tool >/dev/null
```

Expected: the report contains the current policy date and the JSON parses.

- [ ] **Step 3: Run registry monitoring manually**

Trigger `.github/workflows/registry-health.yml`, wait for completion, and inspect its result. ClaudePluginHub may still fail until its crawler records v1.2.0; if it does, leave the daily monitor active and report the observed stale version rather than weakening the check.

- [ ] **Step 4: Enforce branch rules for administrators**

Update the existing protection through:

```bash
gh api --method POST repos/ElxMaj/app-store-review-skill/branches/main/protection/enforce_admins
```

Verify `enforce_admins.enabled` is true and the required `validate` check, pull-request requirement, and linear-history rule remain enabled.

- [ ] **Step 5: Verify Dependabot and repository state**

Confirm:

- PRs #6 and #7 are closed,
- neither Dependabot remote branch exists,
- `.github/dependabot.yml` is absent on `main`,
- the contributors API lists only `ElxMaj`,
- local `main`, `origin/main`, and the merged PR commit agree,
- the working tree is clean.

- [ ] **Step 6: Final handoff**

Report the Pages URL, PR URL, Action results, protection state, Dependabot cleanup, registry-monitor result, and any external crawler delay. Do not claim ClaudePluginHub is current unless its observed version equals the repository manifest.
