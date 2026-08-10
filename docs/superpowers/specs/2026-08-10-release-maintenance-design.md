# Release Maintenance Design

## Goal

Turn the v1.2.0 repository into a safer, easier-to-evaluate public release by publishing the canonical sample report as a live site, monitoring registry freshness, removing unwanted Dependabot automation, and requiring the owner to use the same protected pull-request path as contributors.

## Scope

This change covers four repository-maintenance surfaces:

1. GitHub Pages for the existing sample report.
2. Daily read-only checks for Tessl and ClaudePluginHub freshness.
3. Dependabot removal and closure of its two open pull requests.
4. Enforcement of the existing `main` branch rules for administrators.

It does not change `SKILL.md`, the scanner, references, eval content, the v1.2.0 archive, or the published v1.2.0 tag and release.

## GitHub Pages

Add `.github/workflows/pages.yml`. The workflow runs on pushes to `main` that change the canonical report, its renderer, the Pages workflow, or the README. It also supports manual dispatch.

The build job creates a temporary `_site` directory and copies:

- `examples/parceltrack-report.html` to `_site/index.html`
- `examples/parceltrack-report.json` to `_site/parceltrack-report.json`

It then configures Pages, uploads `_site`, and deploys it through the `github-pages` environment. The workflow uses least-privilege permissions: `contents: read`, `pages: write`, and `id-token: write`. Every third-party action is pinned to the current stable major's exact commit SHA.

The public URL is `https://elxmaj.github.io/app-store-review-skill/`. The README preview image, the “Open the complete sample report” link, and the report JSON link use that live site. The report remains generated from the checked-in canonical JSON, so Pages adds no second report source.

## Registry freshness monitor

Add `.github/workflows/registry-health.yml`. It runs daily at 08:00 UTC and on manual dispatch. It has only `contents: read` permission.

The check derives expected versions from repository files rather than hard-coding a release:

- ClaudePluginHub expected version: `.claude-plugin/plugin.json`
- Tessl expected version: `.tessl-plugin/plugin.json`

It downloads the public ClaudePluginHub listing and extracts its structured `softwareVersion`. It queries the public Tessl tile endpoint and verifies that:

- the latest version equals the repository version,
- moderation status is `pass`,
- aggregate and impact scores are present,
- security has no findings,
- the evaluation multiplier is present.

A stale or malformed registry response fails the workflow. GitHub's normal workflow-failure notifications provide the alert. The workflow does not create issues, republish packages, mutate registry data, or require secrets.

The monitor intentionally does not require Tessl's quality subscore because the public v1.2.0 API currently reports that field as null even after moderation and evaluations complete. Requiring it would create a permanent false alarm.

## Dependabot removal

Remove `.github/dependabot.yml`. Close pull requests #6 and #7 with a short explanation that automated dependency updates are disabled for this repository. Delete their remote Dependabot branches after the pull requests are closed.

Dependabot is already absent from the repository's contributor list. This cleanup removes the remaining open bot activity without rewriting history.

## Branch protection

The current `main` protection already requires:

- pull requests,
- the `validate` status check,
- up-to-date branches,
- linear history,
- no force pushes or deletion.

After the maintenance pull request is merged and both validation and Pages deployment succeed, enable administrator enforcement through the GitHub branch-protection API. This is deliberately the final mutation so it cannot prevent the maintenance release from landing.

Future owner changes must then use a pull request and pass `validate`. Tessl publication and Pages deployment continue to run after merge to `main`.

## Verification

Before opening the pull request:

- run the 36 Python tests,
- parse every repository JSON file used by packaging and evals,
- run `unzip -t app-store-review-skill.skill`,
- validate both workflow YAML files with Ruby's YAML parser,
- execute the registry-check shell logic locally,
- assemble the Pages artifact locally and confirm the HTML and JSON exist at their public paths,
- run `git diff --check`.

After merge:

- confirm `Validate`, `Publish to Tessl`, `Deploy GitHub Pages`, and the registry health workflow are green where triggered,
- confirm the Pages URL serves the current report and JSON,
- confirm Dependabot PRs and branches are gone,
- confirm `enforce_admins.enabled` is true,
- confirm the local and remote `main` commit match.

## Failure handling

- A Pages deployment failure leaves the existing GitHub release and registries untouched.
- A registry-health failure is diagnostic only and cannot republish or alter a listing.
- If branch protection cannot be updated, report the exact current rule state and leave all other completed work intact.
- If a Dependabot branch is already absent, treat branch deletion as complete after confirming its pull request is closed.
