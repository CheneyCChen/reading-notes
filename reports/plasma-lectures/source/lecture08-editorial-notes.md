# Lecture 08 integration

Source: user-provided `Lecture08.pdf`, dated 2026-11-10, 13 pages.
SHA-256: `7f0e3852b9cfb582c82dd37664d09fb7f99bfb638cd0cacdcd38ca379ce32903`.

The new chapter contains 28 learning units, 12 answered source quiz questions, 3 source figures, 213 pre-rendered KaTeX expressions (70 display expressions), and coverage of source equation numbers 1–55. Content is authored in `lecture08-content.py`; executing it only emits the editable section JSON and does not modify the website. Formulas are rendered with KaTeX, and all original PDF bytes are embedded into the page. Images are cropped from source PDF pages 10–12, not AI-generated.

The chapter clearly separates source material from teaching supplements. Review notes:
- Source equation 25 has the wrong epsilon factor; the characteristic electric/magnetic force ratio is VA²/c², still small.
- Source equations 31–32 have heat-flux dimensional inconsistencies; the chapter states the original expressions and labels dimensional corrections.
- The stress normalization in equation 29 is explicit; gyroviscosity is non-dissipative.
- A phenomenological momentum-friction rate does not automatically provide a temperature-equilibration rate.
- The symmetric wave matrix includes a constraint-violating longitudinal zero root; physical zero-frequency degeneracies are treated separately.
- Scalar pressure is a separate closure, not a consequence of magnetization alone.

`tests/plasma_l8_baseline.py` reverses only the documented chapter-8 integration. `tests/plasma-l8-content.py` requires the reversal to reproduce the exact previously published page at a51309d004c52408f643d7069ef3d08e47bee96d; all legacy fidelity tests run on that reversed page. Current-page tests separately verify the eight-chapter integration and new source fidelity. Legacy regressions are not removed.
