# Lecture 7 source and build record

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

The integration is idempotent and never rewrites the first six lecture articles
or their embedded PDF records. It adds the navigation, filter, progress inputs,
original PDF and source metadata to the existing single-file offline course.

Validation:

    npm run test:content
    npm run test:browser

The content tests reconstruct the pre-Lecture-7 course by removing only the
documented additions and reversing the known summary metadata changes, then
compare the entire original course byte-for-byte. The Lecture 7 test also checks
all equation labels in sequence, every original footnote and correction, original
PDF bytes and SHA-256, unique HTML IDs, internal links and pre-rendered math.

Browser tests include 1440px, 390px and 320px widths, source PDF controls, all seven
filters, local progress persistence, footnote return links, every Lecture 7 quiz,
themes, long formulas, print mode and no-JavaScript reading. A passing static test
does not itself establish that the browser tests ran successfully.
