#!/usr/bin/env python3

"""Verify that workflow action SHAs match their moving major-version tags."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
MAJOR_TAG_PATTERN = re.compile(r"^v[0-9]+$")
MAJOR_TAG_COMMENT_PATTERN = re.compile(r"#\s*(v[0-9]+)\s*$")
USES_HELPER = Path(__file__).with_name("list_workflow_uses.rb")


def fail(message: str) -> None:
    print(f"Action pin check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def fetch_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        fail(f"could not read {url}: {error}")

    if not isinstance(payload, dict):
        fail(f"unexpected response from {url}")
    return payload


def current_tag_sha(api_base: str, action: str, tag: str) -> str:
    encoded_tag = quote(tag, safe="")
    ref_url = f"{api_base}/repos/{action}/git/ref/tags/{encoded_tag}"
    ref = fetch_json(ref_url)
    target = ref.get("object")
    if not isinstance(target, dict):
        fail(f"{action} {tag} response has no object")

    object_type = target.get("type")
    sha = target.get("sha")
    if not isinstance(sha, str) or not FULL_SHA_PATTERN.fullmatch(sha):
        fail(f"{action} {tag} response has no valid SHA")
    if object_type == "commit":
        return sha
    if object_type != "tag":
        fail(f"{action} {tag} points to unsupported object type {object_type!r}")

    tag_url = f"{api_base}/repos/{action}/git/tags/{sha}"
    annotated_tag = fetch_json(tag_url)
    annotated_target = annotated_tag.get("object")
    if not isinstance(annotated_target, dict):
        fail(f"{action} {tag} annotated tag has no object")
    commit_sha = annotated_target.get("sha")
    if annotated_target.get("type") != "commit" or not isinstance(commit_sha, str):
        fail(f"{action} {tag} annotated tag does not point to a commit")
    if not FULL_SHA_PATTERN.fullmatch(commit_sha):
        fail(f"{action} {tag} annotated tag has no valid commit SHA")
    return commit_sha


def workflow_action_pins(workflow_dir: Path) -> list[tuple[str, str, str]]:
    pins: set[tuple[str, str, str]] = set()
    workflows = sorted((*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")))
    if not workflows:
        fail(f"no workflow files found in {workflow_dir}")

    parsed = subprocess.run(
        ["ruby", str(USES_HELPER), *(str(path) for path in workflows)],
        capture_output=True,
        text=True,
        check=False,
    )
    if parsed.returncode != 0:
        fail(f"workflow YAML could not be inspected: {parsed.stderr.strip()}")
    try:
        entries = json.loads(parsed.stdout)
    except json.JSONDecodeError as error:
        fail(f"workflow inspector returned invalid JSON: {error}")

    workflow_lines = {
        str(path): path.read_text(encoding="utf-8").splitlines() for path in workflows
    }
    for entry in entries:
        workflow = entry.get("path")
        line_number = entry.get("line")
        value = entry.get("value")
        if (
            not isinstance(workflow, str)
            or not isinstance(line_number, int)
            or not isinstance(value, str)
            or workflow not in workflow_lines
            or not 1 <= line_number <= len(workflow_lines[workflow])
        ):
            fail("workflow inspector returned an invalid uses entry")
        if value.startswith("./"):
            continue
        if "@" not in value:
            fail(f"{value} has no immutable reference ({workflow}:{line_number})")

        source, action_ref = value.rsplit("@", 1)
        parts = source.split("/")
        if len(parts) < 2 or not all(parts[:2]):
            fail(f"unsupported external uses target {source!r} ({workflow}:{line_number})")
        action = "/".join(parts[:2])
        if not FULL_SHA_PATTERN.fullmatch(action_ref):
            fail(f"{source} is not pinned to a full commit SHA ({workflow}:{line_number})")

        source_line = workflow_lines[workflow][line_number - 1]
        tag_match = MAJOR_TAG_COMMENT_PATTERN.search(source_line)
        tag = tag_match.group(1) if tag_match else None
        if tag is None or not MAJOR_TAG_PATTERN.fullmatch(tag):
            fail(f"{source} pin has no moving major tag comment ({workflow}:{line_number})")
        pins.add((action, action_ref, tag))
    if not pins:
        fail(f"no pinned third-party Actions found in {workflow_dir}")
    return sorted(pins)


def main() -> None:
    workflow_dir = Path(os.environ.get("ASR_WORKFLOW_DIR", ".github/workflows"))
    api_base = os.environ.get("ASR_GITHUB_API_BASE", "https://api.github.com").rstrip("/")

    pins = workflow_action_pins(workflow_dir)
    for action, observed_sha, tag in pins:
        expected_sha = current_tag_sha(api_base, action, tag)
        if observed_sha != expected_sha:
            fail(
                f"{action} pin is stale for {tag}: "
                f"observed {observed_sha}, current {expected_sha}"
            )
        print(f"{action}: {tag} at {observed_sha}")
    print(f"Action pins: {len(pins)} verified")


if __name__ == "__main__":
    main()
