# Course source and build record

This directory preserves the user-supplied Lecture07.pdf (updated 2026-11-03),
the corresponding Chinese translation and its explicit editorial corrections,
and the source coverage record. Lecture 7 has 12 original pages, 73 numbered
equation labels, 5 footnotes, 14 quiz questions, 2 references and no source figures.

The website adds 19 learning units and 14 expandable answers. Added explanations
are labelled “学习补充”; the original formula is followed by its correction rather
than silently replaced. The translation's supplementary diagrams are not added.

Rebuild the chapter text with Pandoc:

    python3 scripts/prepare-plasma-l7.py

Render and integrate with KaTeX 0.16.x (set KATEX_PATH to an installed package
directory when it is not available through the local Node module resolution):

    node scripts/integrate-plasma-l7.cjs

The chapter integration is idempotent. Its subsequent reviewed prose/additions
layer may change ordinary wording in the first six lectures but never their
original formulas or embedded PDF records. It adds the navigation, filter, progress inputs,
original PDF and source metadata to the existing single-file offline course.

Validation:

    npm run test:content
    npm run test:browser

The content tests reconstruct the pre-Lecture-7 course by removing only the
documented additions and reversing the known summary metadata changes, then
compare the entire original course byte-for-byte after reversing the explicitly
audited prose edits. The Lecture 7 test also checks
all equation labels in sequence, every original footnote and correction, original
PDF bytes and SHA-256, unique HTML IDs, internal links and pre-rendered math.

Browser tests include 1440px, 390px and 320px widths, source PDF controls, all seven
filters, local progress persistence, footnote return links, every Lecture 7 quiz,
themes, long formulas, print mode and no-JavaScript reading. A passing static test
does not itself establish that the browser tests ran successfully.

## Reviewed prose compaction

The original PDF and TeX translation are unchanged. Website wording is shortened
through `prose-edits.json`, an explicit, reversible allowlist of ordinary text
node edits against commit `2b51e16`. No formula, MathML, diagram, derivation step,
self-test, source link or HTML element is removed. Per-unit coverage is recorded
in `prose-coverage.md`.

`integrate-plasma-l7.cjs` reapplies this layer after rebuilding Lecture 7. It can
also be applied with `python3 scripts/plasma_prose.py`. The operation is
idempotent and rejects unexpected source changes instead of overwriting them.
If the source wording changes, review and update the corresponding allowlist
entry rather than bypassing its assertion.

`tests/plasma-prose.py` compares protected HTML bytes and original formulas for
each lecture, checks all headings/learning units/self-tests, and proves that
reversing the exact allowlisted edits reproduces the whole baseline page. The
previous regression tests still compare against their independent older
baselines after reversing only documented additions and prose edits.

## Added derivation bridges and course map

`derivations/` preserves the authored draft, explicit TeX typesetting source,
17 rendered fragments and their section-to-source mapping. All additions are
labelled “推导补充” and appended to the original text. The 266 new formulas
include the full BGK Gaussian-moment calculation; three long derivations use
native disclosures. Six cross-links connect shared calculations without
repeating them. `supplements.json` adds these blocks and the separately labelled
mirror-work sign correction (three formulas). The complete page has 2,122
pre-rendered formulas, including all 1,853 original expressions.

`course-map.html`, `.css` and `.js` define the seven-node, eight-connection map
at the top of the course. Native anchors work without JavaScript. Desktop uses
a network layout; narrow screens use sequential cards with dependency text.
Ordinary map and cross-link clicks clear stale filters while preserving native
hash history, keyboard operation and modified-click behavior. No animation or
new runtime dependency is added.

`plasma_prose.py` composes all three source-backed layers in a repeatable order.
`tests/plasma-enhancements.py` checks insertion targets, source math coverage,
unique IDs and links. `tests/plasma-physics.py` checks representative algebra,
Gaussian contractions and limiting cases for all 17 bridges and the mirror sign.
`tests/plasma-enhancements-browser.cjs` exercises the new map and disclosures,
narrow-screen overflow, offline rendering, dark mode, print and no-JS behavior.
These checks complement, rather than replace, the original course tests.
