# Community Launch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Introduce the open-source App Store review skill through high-fit, rule-compliant developer channels.

**Architecture:** Use the GitHub repository and live report as the two public proof surfaces. Write unique copy for each channel, disclose the maker relationship, and log each submission without manufacturing engagement.

**Tech Stack:** GitHub, Show HN, iOS Dev Weekly, Reddit community rules, ClaudePluginHub.

## Global Constraints

- Do not ask for votes or coordinate engagement.
- Disclose that Elie Majorel is the maker.
- Do not post to a community outside its allowed self-promotion window.
- Do not claim pass rates, Apple affiliation, or guaranteed approval.

---

### Task 1: Rule and asset gate

**Files:**
- Create: `docs/launch/2026-08-11-launch-log.md`

**Interfaces:**
- Consumes: current official channel rules, repository URL, and live report URL.
- Produces: a channel table with allowed format, account requirement, copy, and status.

- [ ] Verify the current official rules for every selected channel.
- [ ] Record maker disclosure, source URLs, final destination URLs, and any timing restrictions.
- [ ] Drop channels that do not permit the intended submission.

### Task 2: Submit high-fit surfaces

**Files:**
- Modify: `docs/launch/2026-08-11-launch-log.md`

**Interfaces:**
- Consumes: approved channel rows from Task 1.
- Produces: truthful submission records and public URLs where available.

- [ ] Submit a concise editorial suggestion to iOS Dev Weekly.
- [ ] Submit Show HN only after the release is live and directly usable.
- [ ] Prepare Reddit-specific copy for the next permitted window, and post only if the signed-in account meets community requirements.
- [ ] Record accepted, pending, blocked, or scheduled status for each action.
