# Additional derivation sources

This directory contains 17 labelled teaching supplements and their offline KaTeX fragments.
The original authored draft is preserved in `derivation-supplements.original.md`;
`derivation-supplements.render.md` adds explicit inline TeX for typesetting.

L7-A explicitly adds the one-dimensional Gaussian recurrence, independent
three-dimensional moments and traceless contractions. All 65 original display
formulas remain unchanged and in order. The expanded version has 69 display
formulas and 197 inline formulas, rendered with KaTeX 0.16.22 and strict errors.

`index.json` maps each block to its original learning section. All blocks are
appended, including L7-A, so no original formula or learning note is replaced.
Three longer calculations use labelled disclosure controls; the original 63
self-tests remain separate. `cross-links.json` avoids repeating derivations.

Rebuild from this directory:

    python3 normalize.py
    KATEX_PATH=/path/to/katex node render.cjs
    python3 ../../../../scripts/plasma_prose.py

Use `node render.cjs --preview` only when standalone visual preview files are
needed; those extra HTML files are not part of the published source record.

The integrated course uses only local, embedded HTML/MathML/fonts. No runtime
network access is needed for mathematical rendering. Run `npm run test:content`
from the repository root for structure, source coverage, math and focused
physical regressions; `npm run test:browser` also checks interactive and narrow
screen behavior when a supported Chromium environment is available.

The supplements explain intermediate calculations under their stated
assumptions; they are not a full Balescu–Lenard or Braginskii theory proof.
