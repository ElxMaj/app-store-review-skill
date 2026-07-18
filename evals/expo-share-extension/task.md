# Pre-Launch Review: ShareFlow iOS App

## Problem/Feature Description

Your team has been building ShareFlow, an iOS productivity app built with Expo that lets users share photos and videos from any app via a Share extension. The app also uses a notification service extension for rich push notifications. Before submitting to the App Store for the first time, the engineering lead wants a thorough review to catch any issues that could cause rejection or delays.

The project source is in the `inputs/` directory. It contains the Expo configuration (`app.json`), a config plugin that adds the Share extension target (`plugins/withShareExtension.js`), the `package.json` listing all dependencies, and a draft of the App Store metadata (`app-metadata.md`). The native iOS directory has not been generated yet — the team runs `expo prebuild` only at CI time.

The engineering lead wants to know whether the app is ready to submit, how strong its App Store positioning is, and what should change before launch.

## Output Specification

Use the installed App Store review skill and produce `shareflow-review.md` in the working directory. Do not change the supplied project.
