# Pre-Launch Review: ShareFlow iOS App

## Problem/Feature Description

Your team has been building ShareFlow, an iOS productivity app built with Expo that lets users share photos and videos from any app via a Share extension. The app also uses a notification service extension for rich push notifications. Before submitting to the App Store for the first time, the engineering lead wants a thorough review to catch any issues that could cause rejection or delays.

The project source is in the `inputs/` directory. It contains the Expo configuration (`app.json`), a config plugin that adds the Share extension target (`plugins/withShareExtension.js`), the `package.json` listing all dependencies, and a draft of the App Store metadata (`app-metadata.md`). The native iOS directory has not been generated yet — the team runs `expo prebuild` only at CI time.

The engineering lead wants to know: is the app ready to submit, and how strong is the product's App Store positioning? They also want to understand what the most impactful changes would be before launch.

## Output Specification

Produce a single Markdown report file named `shareflow-review.md` in your working directory. The report should contain:

1. A complete pre-submission configuration audit covering the Expo config, config plugins, privacy manifest, entitlements, and permission declarations — citing specific file paths and keys for every finding.
2. A human-craft assessment of the App Store product page and product differentiation, including grades for each dimension reviewed and the five highest-impact interventions the team should make before launch.

The report must be read-only — do not modify any of the input files. After the report, append a section titled `## Fix Plan` that groups the recommended changes and notes which ones require approval before implementation.
