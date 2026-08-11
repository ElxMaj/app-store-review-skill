# Install App Store Review

Choose one installation route. The Skills CLI is the simplest option across compatible coding agents. Claude Code users can also install the complete plugin, which adds direct slash commands.

## Skills CLI

```bash
npx skills add ElxMaj/app-store-review-skill
```

## ClaudePluginHub

```bash
npx claudepluginhub elxmaj/app-store-review-skill --plugin app-store-review
```

## Claude Code marketplace

Run these inside Claude Code:

```text
/plugin marketplace add ElxMaj/app-store-review-skill
/plugin install app-store-review@app-store-review-skill
```

Start a review with normal language or the direct skill command:

```text
/app-store-review Audit this iOS project before submission. Report first and do not edit files.
```

The explicit plugin names are also available:

```text
/app-store-review:app-store-review <review request>
/app-store-review:review <review request>
```

Verify the installed version and component inventory:

```bash
claude plugin details app-store-review@app-store-review-skill
```

Update or remove the Claude Code plugin:

```bash
claude plugin update app-store-review@app-store-review-skill
claude plugin uninstall app-store-review@app-store-review-skill
```

## Tessl

```bash
npx tessl install maj-labs/app-store-review
```

The skill does not need credentials for a source audit. Keep App Store Connect credentials, signing material, private rejection attachments, and customer data out of prompts and issue reports.
