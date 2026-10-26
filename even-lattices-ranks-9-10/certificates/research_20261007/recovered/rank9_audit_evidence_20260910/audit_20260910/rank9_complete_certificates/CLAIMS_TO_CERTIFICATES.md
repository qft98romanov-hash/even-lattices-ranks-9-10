# Mathematical claims and exact certificates

| Claim | Exact certificate(s) | Expected terminal assertion |
|---|---|---|
| Complete lower saturated-flag enumeration through rank 6; 3699 raw forms and class counts `1,5,14,47,118,138` | `extend_flag.py`; regenerated JSON/raw files; `verify_lower_flag_chain_exact.py`; bridge verifier | `ALL_LOWER_FLAG_RAW_FORMS_AND_GL_MAPS_EXACT_OK`; `ALL_REGENERATED_FROZEN_EXACT_BRIDGES_OK` |
| Exact equivalence between freshly regenerated and frozen representative sets | `regenerated_frozen_bridges_exact.json`; bridge verifier | bijective explicit `GL_n(Z)` maps for every listed rank/set |
| Exhaustive rank 6 to rank 7 enumeration; 138 parents and 2235 raw children | four `rank7_chunk_*.json`; `merge_flag_chunks.py`; `verify_flag_chunks.py` and transcript | parent ranges cover `[0,138)` once; `RAW 2235`; `RANK6_TO_RANK7_CHUNKS_EXACT_OK` |
| Lifting inequality eliminates 25 of 31 determinant pairs and 2139 of 2235 raw forms | `verify_rank7_survivor_linkage_exact.py`; `rank7_survivor_linkage_exact.json` | exactly six displayed `(d_6,d_7)` pairs and 96 forms survive |
| All 96 surviving raw forms belong to six rank-seven classes | `rank7_survivor_linkage_exact.json`; independent linkage verifier and transcript | `ALL_96_SURVIVORS_LINKED_TO_6_EXACT_CLASSES` |
| Branch `(2187,4374)` cannot give `det(L_9)<21870` | `verify_e7_branch_exact.py` and transcript | `CONCLUSION: every rank-9 continuation in this branch has det >= 21870` |
| Branch `(2187,6318)` cannot give `det(L_9)<21870` | `verify_h6318_branch_exact.py` and transcript | `H6318_BRANCH_EXACT_OK` |
| Branch `(2835,7722)` has no flag-compatible rank-eight continuation (the redundant unrestricted `J13689` candidate has rank-nine floor 36504); branch `(4096,8192)` also has none | `verify_rank7_topdown.py` and transcript | exact assertions in transcript; script exits 0 |
| Branch `(3240,8100)` has `d_8>=18225>15908` | `verify_rank7_residuals_exact.py`; `rank7_residuals_exact.json`; transcript | exact glue radius `15/4`, lower bound 18225, and `ALL_RESIDUAL_RANK7_CERTIFICATES_OK` |
| Branch `(3267,7986)` has a unique flag-compatible rank-eight class of determinant 14641 and `d_9>=39930` | same residual certificate | exact radii `25/6`, `36/11`; bounds 14641 and 39930; same terminal assertion |
| Independent exact check `rho(sqrt(3)E_8)^2=8/3` | `verify_sqrt3_e8_covering_radius_exact.py` and transcript | `SQRT3_E8_COVERING_RADIUS_EXACT_OK` |
| Every one of the six survivors is closed | linkage, E7, H6318, top-down, residual and E8 certificates jointly; see `README_EN.md` | all six pairs linked to a passing branch certificate |
| The lower bound is sharp: the displayed `K_9` is even, positive definite, has determinant 21870 and minimum 6 | `verify_rank9_extremal_example_exact.py` and transcript | `RANK9_EXTREMAL_EXAMPLE_EXACT_OK` |

The programs do not reprove the classical Hermite constants or Mordell's
inequality used to derive the determinant windows. They do not prove
uniqueness of the optimizer, a complete rank-nine classification, any
rank-ten analogue, or any statement about cluster improvements.
