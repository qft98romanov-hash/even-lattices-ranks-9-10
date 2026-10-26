# Validation of this repository preparation

These records describe checks actually performed on 26 October 2026. They are
separate from the historical mathematical evidence in `certificates/`.

- `routine_verification.json` and `routine_suite.log`: the original 21-check
  routine suite passed from a copied evidence tree (about 143 seconds).
- `wrapper_run.json` and `repository_wrapper.log`: the repository verification
  wrapper also completed all 21 checks (about 119 seconds).
- `wrapper_log_selection_check.json` and `routine_logs/`: exactly the 21 logs
  associated with that successful run. The final wrapper's selective log-copy
  change was checked against the actual trace after the full invocation; the
  mathematical subprocesses and arguments were unchanged by that change.
- `audit.md` and `inventory.json`: dependencies, historical path limitations,
  language inventory, and original-package byte checks.
- `manuscript_editorial_QA.json`: comparison against the complete current
  English report. The theorem/proof environments and all 54 labels are kept.
- `manuscript_build_QA.json`: three XeLaTeX passes, 37 PDF pages, no TeX
  warnings or unresolved references, source identity, and completed layout
  review.
- `EDITORIAL_CHANGES.txt`: the changes to presentation and scope explanations.

No optional full regeneration was repeated during this preparation. The
package preserves the earlier regeneration records and their exact commands.
Internal implementation checks are not external mathematical peer review.
