#!/usr/bin/env bash

set -euo pipefail

fail() {
  printf 'Registry health check failed: %s\n' "$1" >&2
  exit 1
}

fetch() {
  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    --retry 3 \
    --connect-timeout 10 \
    --max-time 30 \
    "$1"
}

claude_manifest=${ASR_CLAUDE_MANIFEST:-.claude-plugin/plugin.json}
tessl_manifest=${ASR_TESSL_MANIFEST:-.tessl-plugin/plugin.json}
claude_url=${ASR_CLAUDE_URL:-https://www.claudepluginhub.com/plugins/elxmaj-app-store-review}
tessl_tile_url=${ASR_TESSL_TILE_URL:-https://api.tessl.io/v1/tiles/maj-labs/app-store-review}

expected_claude_version=$(jq -er '.version | select(type == "string" and length > 0)' "$claude_manifest") \
  || fail "Claude plugin manifest has no valid version"
expected_tessl_version=$(jq -er '.version | select(type == "string" and length > 0)' "$tessl_manifest") \
  || fail "Tessl plugin manifest has no valid version"
tessl_version_url=${ASR_TESSL_VERSION_URL:-https://api.tessl.io/v1/tiles/maj-labs/app-store-review/versions/$expected_tessl_version}

claude_listing=$(fetch "$claude_url") || fail "ClaudePluginHub listing could not be downloaded"
claude_version_pattern='"softwareVersion"[[:space:]]*:[[:space:]]*"([^"]+)"'
if [[ $claude_listing =~ $claude_version_pattern ]]; then
  observed_claude_version=${BASH_REMATCH[1]}
else
  fail "ClaudePluginHub softwareVersion is missing"
fi

if [[ $observed_claude_version != "$expected_claude_version" ]]; then
  fail "ClaudePluginHub version mismatch: expected $expected_claude_version, observed $observed_claude_version"
fi

tessl_tile=$(fetch "$tessl_tile_url") || fail "Tessl tile could not be downloaded"
observed_tessl_version=$(jq -er '.data.attributes.latestVersion | select(type == "string" and length > 0)' <<<"$tessl_tile") \
  || fail "Tessl latest version is missing"
if [[ $observed_tessl_version != "$expected_tessl_version" ]]; then
  fail "Tessl version mismatch: expected $expected_tessl_version, observed $observed_tessl_version"
fi

tessl_version=$(fetch "$tessl_version_url") || fail "Tessl version details could not be downloaded"
version_detail=$(jq -er '.data.attributes.version | select(type == "string" and length > 0)' <<<"$tessl_version") \
  || fail "Tessl version detail is missing"
if [[ $version_detail != "$expected_tessl_version" ]]; then
  fail "Tessl detail mismatch: expected $expected_tessl_version, observed $version_detail"
fi

moderation_status=$(jq -er '.data.attributes.moderationStatus | select(type == "string" and length > 0)' <<<"$tessl_version") \
  || fail "Tessl moderation status is missing"
if [[ $moderation_status != "pass" ]]; then
  fail "Tessl moderation did not pass: observed $moderation_status"
fi

aggregate=$(jq -er '.data.attributes.scores.aggregate | numbers' <<<"$tessl_version") \
  || fail "Tessl aggregate score is missing"
impact=$(jq -er '.data.attributes.scores.impact | numbers' <<<"$tessl_version") \
  || fail "Tessl impact score is missing"
security_level=$(jq -er '.data.attributes.scores.securityLevel | select(type == "string" and length > 0)' <<<"$tessl_version") \
  || fail "Tessl security level is missing"
if [[ $security_level != "NONE" ]]; then
  fail "Tessl security findings are present: observed $security_level"
fi

multiplier=$(jq -er '
  (.data.attributes.evalImprovementMultiplier // .data.attributes.scores.evalImprovementMultiplier)
  | numbers
' <<<"$tessl_version") || fail "Tessl evaluation multiplier is missing"

aggregate_percent=$(jq -nr --argjson score "$aggregate" '$score * 100 | round')
impact_percent=$(jq -nr --argjson score "$impact" '$score * 100 | round')

printf 'ClaudePluginHub: %s\n' "$observed_claude_version"
printf 'Tessl: %s, aggregate %s%%, impact %s%%, security %s, multiplier %sx\n' \
  "$observed_tessl_version" \
  "$aggregate_percent" \
  "$impact_percent" \
  "$security_level" \
  "$multiplier"
