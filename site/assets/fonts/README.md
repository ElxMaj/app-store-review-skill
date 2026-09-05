# Landing asset provenance

## Hubot Sans display subset

- Upstream: https://github.com/github/hubot-sans
- Release: v1.0.1
- Release asset: Hubot-Sans.zip
- Source ZIP SHA-256: `b460d36097a5c9a3e45710cbe1554589eaa5765d7c2c88df364516f3e27159b1`
- License: SIL Open Font License 1.1; copied as `OFL.txt`
- Toolchain: `fonttools[woff]==4.64.0`
- Transformation: remove the unused slant axis, retain variable weight and width, subset to the Latin and interface characters listed in the implementation plan, and preserve the source timestamp for deterministic output.
- Output SHA-256: `d48383a1e421d6bec4b5e7a578ede43398047c637fa1311e5a9558e35e2dd9ee`

## Review-gate responsive derivatives

- Source: `../review-gate-cinematic.png`, the repository's original 1536×1024 artwork.
- Toolchain: `sharp-cli@5.2.0`
- Transformation: responsive east-weighted crop and AVIF/WebP encoding only.
- Semantic text and report evidence remain HTML; these files are decorative plates.
- `review-gate-cinematic-768.avif` SHA-256: `28adf780f1cd63d72ddd0d255a14f0e6eccec77b7ce19c96ff21b2582cff1650`
- `review-gate-cinematic-768.webp` SHA-256: `e5231eadea8ce2e9b9bfee7473de5ea21b570b76cfc05626343fddc225170292`
- `review-gate-cinematic-1440.avif` SHA-256: `748343a6187cec1179c7b357a3f19fcec34b2a519f5fe47d257e69b94a3b5763`
- `review-gate-cinematic-1440.webp` SHA-256: `3534d149c5f84e41ed0efe4db4fde17fd1c538b354ee0b7c60e5a009d9d1961b`

The exact commands and output budgets are recorded in `docs/superpowers/plans/2026-09-05-from-alarm-to-evidence.md`.
