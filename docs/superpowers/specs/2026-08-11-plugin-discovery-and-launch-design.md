# Plugin Discovery and Launch Design

## Goal

Raise the plugin's documentation and capability signals with useful, verifiable additions, then introduce the live project to communities that serve Apple-platform developers.

## Repository design

- Add `INSTALL.md` at the repository root. It will cover Skills CLI, ClaudePluginHub, Claude Code marketplace, Tessl, direct invocation, update, uninstall, and verification.
- Add `commands/review.md` as one thin Claude Code entry point. It will pass the user's arguments to the existing `app-store-review:app-store-review` skill and will not duplicate its policy or workflow.
- Add the ClaudePluginHub command and direct slash invocation to the README while keeping it below 130 lines.
- Release the plugin as version `1.2.1` so registries can distinguish the new component inventory.

## Safety and quality boundaries

- Do not add hooks, agents, MCP servers, or network calls for score alone.
- Keep the first review pass read-only and preserve the existing approval gate for fixes.
- Do not change the canonical skill instructions or references except for release-version synchronization required by package tests.
- Test command delegation, installation copy, package consistency, manifest validity, and the complete Python suite before publishing.

## Launch design

Use a factual maker disclosure: Elie Majorel built and maintains the project under Maj Labs. Link to the public repository and live report. Lead with the concrete artifact and the evidence model, not score claims.

Submit only where current rules allow self-promotion. Use Show HN for the runnable open-source tool, iOS Dev Weekly's suggestion form for editorial consideration, and relevant directories. Prepare Reddit posts for an allowed community window instead of posting out of turn. Do not ask for votes, cross-post identical copy, or imply Apple endorsement.

## Success checks

- Claude Code validates the marketplace and discovers both the skill and the review command.
- `INSTALL.md` contains copyable commands and a concrete verification step.
- README stays below 130 lines and includes the ClaudePluginHub installer exactly once.
- All local tests and GitHub checks pass.
- Every external submission records its destination, final copy, and status.
