# Landing asset provenance

## Barlow Condensed Black Italic

- Upstream family record: https://github.com/google/fonts/tree/5e35378e6bda803962ee6fd257e444a7d459660d/ofl/barlowcondensed
- Exact WOFF2 source: https://fonts.gstatic.com/s/barlowcondensed/v13/HTxyL3I-JCGChYJ8VI-L6OO_au7B6xTrW3bmu4kGQLhExw.woff2
- Exact license source: https://raw.githubusercontent.com/google/fonts/5e35378e6bda803962ee6fd257e444a7d459660d/ofl/barlowcondensed/OFL.txt
- Retrieved: 2026-09-05
- License: SIL Open Font License 1.1; copied as `Barlow-OFL.txt`
- Transformation: none. The versioned Latin WOFF2 is shipped byte-for-byte.
- Output SHA-256: `83282bcfc9df534b070d8231f10e511ba0c60ae63af9b5e096e4de089454bc88`
- License SHA-256: `186d750eb496a4c17a76385f82be6aea2ac1cf2de074a811d63786cf374ea73f`

## Geist Sans variable

- Upstream: https://github.com/vercel/geist-font/tree/8b8b75fa63e339db10a3cd52fb28536615b5cc63
- Release: v1.7.1
- Exact WOFF2 source: https://raw.githubusercontent.com/vercel/geist-font/8b8b75fa63e339db10a3cd52fb28536615b5cc63/fonts/Geist/webfonts/Geist%5Bwght%5D.woff2
- Exact license source: https://raw.githubusercontent.com/vercel/geist-font/8b8b75fa63e339db10a3cd52fb28536615b5cc63/OFL.txt
- License: SIL Open Font License 1.1; copied as `Geist-OFL.txt`
- Transformation: none. The release WOFF2 is shipped byte-for-byte.
- Output SHA-256: `2ffebe993e969069a9789d15164b7715d42491b5835516c5e3b935d5f81b05f1`
- License SHA-256: `c683bfbcc7e087f5d37a54ef628f10387c451a83ddc459b151403a164ac46c90`

## Reproduce the shipped font inputs

Run from the repository root. These commands download immutable revision or versioned asset URLs; there is no local font transformation step.

```sh
curl -L --fail --silent --show-error \
  'https://fonts.gstatic.com/s/barlowcondensed/v13/HTxyL3I-JCGChYJ8VI-L6OO_au7B6xTrW3bmu4kGQLhExw.woff2' \
  -o site/assets/fonts/BarlowCondensed-BlackItalic.woff2
curl -L --fail --silent --show-error \
  'https://raw.githubusercontent.com/google/fonts/5e35378e6bda803962ee6fd257e444a7d459660d/ofl/barlowcondensed/OFL.txt' \
  -o site/assets/fonts/Barlow-OFL.txt
curl -L --fail --silent --show-error \
  'https://raw.githubusercontent.com/vercel/geist-font/8b8b75fa63e339db10a3cd52fb28536615b5cc63/fonts/Geist/webfonts/Geist%5Bwght%5D.woff2' \
  -o site/assets/fonts/Geist-Variable.woff2
curl -L --fail --silent --show-error \
  'https://raw.githubusercontent.com/vercel/geist-font/8b8b75fa63e339db10a3cd52fb28536615b5cc63/OFL.txt' \
  -o site/assets/fonts/Geist-OFL.txt
```

Verify all four inputs:

```sh
printf '%s  %s\n' \
  '83282bcfc9df534b070d8231f10e511ba0c60ae63af9b5e096e4de089454bc88' 'site/assets/fonts/BarlowCondensed-BlackItalic.woff2' \
  '186d750eb496a4c17a76385f82be6aea2ac1cf2de074a811d63786cf374ea73f' 'site/assets/fonts/Barlow-OFL.txt' \
  '2ffebe993e969069a9789d15164b7715d42491b5835516c5e3b935d5f81b05f1' 'site/assets/fonts/Geist-Variable.woff2' \
  'c683bfbcc7e087f5d37a54ef628f10387c451a83ddc459b151403a164ac46c90' 'site/assets/fonts/Geist-OFL.txt' \
  | shasum -a 256 -c -
```

## Review-gate responsive derivatives

- Source: `../review-gate-cinematic.png`, the repository's original 1536×1024 artwork.
- Toolchain: `sharp-cli@5.2.0`
- Transformation: responsive east-weighted crop and AVIF/WebP encoding only.
- Semantic text and report evidence remain HTML; these files are decorative plates.
- `review-gate-cinematic-768.avif` SHA-256: `28adf780f1cd63d72ddd0d255a14f0e6eccec77b7ce19c96ff21b2582cff1650`
- `review-gate-cinematic-768.webp` SHA-256: `e5231eadea8ce2e9b9bfee7473de5ea21b570b76cfc05626343fddc225170292`
- `review-gate-cinematic-1440.avif` SHA-256: `748343a6187cec1179c7b357a3f19fcec34b2a519f5fe47d257e69b94a3b5763`
- `review-gate-cinematic-1440.webp` SHA-256: `3534d149c5f84e41ed0efe4db4fde17fd1c538b354ee0b7c60e5a009d9d1961b`

The previous Hubot-based typography plan is retained as history and explicitly marked superseded. This file is canonical for the font binaries that ship with the campaign-poster landing page.
