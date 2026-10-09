#!/usr/bin/env python3
"""Refresh installable resources from the canonical skill, without publishing."""
from pathlib import Path
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[2]
COPILOT = ROOT / "copilot-plugin/skills/app-store-review"
ARCHIVE = ROOT / "app-store-review-skill.skill"


def main():
    resources = sorted([
        *ROOT.glob("references/*.md"),
        *ROOT.glob("scripts/*.py"),
    ])
    for source in resources:
        destination = COPILOT / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    appendix = "\n## Packaged resources\n\n"
    appendix += "Read the relevant resources below using paths relative to this skill.\n\n"
    appendix += "\n".join(
        f"- [{source.relative_to(ROOT).as_posix()}]({source.relative_to(ROOT).as_posix()})"
        for source in resources
    ) + "\n"
    (COPILOT / "SKILL.md").write_text(skill + appendix, encoding="utf-8")

    # Stable ordering, timestamps, permissions and compression make byte-level
    # parity checks reproducible. Only runtime resources enter the portable ZIP.
    sources = sorted([ROOT / "SKILL.md", ROOT / "agents/openai.yaml", *resources])
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sources:
            name = "app-store-review/" + source.relative_to(ROOT).as_posix()
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, source.read_bytes(), compresslevel=9)
    print(f"Refreshed {len(resources)} resources and {ARCHIVE.name}.")


if __name__ == "__main__":
    main()
