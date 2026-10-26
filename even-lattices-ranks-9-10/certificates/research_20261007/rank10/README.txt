Confidential rank-nine/rank-ten research continuation, 7 October 2026.

NEW GLOBAL RESULT, WITH EXPLICIT EXTERNAL INPUT
Assuming gamma9<=2, the completed exact search proves e10(6)=54675.
No prior rank-nine determinant theorem or gap certificate is needed.
Read global_rank10_proof_EN.txt. The final certificate entry point is
  python verify_global_rank10_certificate.py
For complete actual regeneration of all extension lists:
  python verify_global_rank10_certificate.py --replay --workers 7
Read global_rank10_certificate_verified.json for the actual replay status;
an intermediate progress file is not a completion certificate.
The strict search does NOT classify all global rank-ten equality cases.

UNCONDITIONAL E8-CONTAINING SUBCLASS
All even integral rank-ten min-six lattices containing sqrt(3)E8 have
determinant>=54675, and exactly TWO isometry classes attain it.
Read rank10_e8_theorem.txt; run
  python verify_rank10_e8_classification.py
The second type is an index3gluing of sqrt(3)E8 perpendicular sqrt(5)A2.
The explicit K9 deepest classes are in k9_deep_class_pairings.json.

RANK-NINE SPECTRAL COROLLARY (under gamma9<=2)
Below32076 the exact determinant spectrum is21870,26244,30618, one
isometry class at each. The smallest no-E8 determinant is32076.
Read rank9_spectral_corollary_EN.txt; run
  python verify_rank9_low_spectrum.py

COMPUTATIONAL COVERAGE
ranks2--6 raw/classes:9/6,102/31,729/161,6934/925,28284/3752.
rank7:56269 raw,52208 liftingprunes,4061eligible ->224classes.
rank8:19481 raw,18110 liftingprunes,1371eligible ->47classes.
rank9 low19684..24450:47parents,45prunes,2exhaustivejobs,0children.
rank9 high24452..40054:47parents,3819children,ALL3819excluded by final
lifting. No rank-ten extension stage is required: no parent survives.
The least final lifting lower bound is12966723/212>54672.

All Python uses standard-library integer/rational arithmetic. The main
vector enumerator is the archived exact LDL kernel. The static checker
has its own independent short-dual enumerator. No independent complete
second implementation of every discriminant enumeration, external referee
review, or formal proof-assistant verification is claimed.

The local 19-section ambient embedding theorem is maintained separately
by the embeddings part of the research package. No classification of all
rank48 embedding orbits follows from the present determinant search.

REPRODUCTION HELPERS
run_early_flags.py regenerates the low-rank prefix with fast exact dedup;
run_rank7_parallel.py is the original complete raw rank7 run;
run_next_rank_fast_parallel.py resumes generic later-rank searches;
fast_extension_proof.txt explains its integer shortest-normal test.
Only final files named above should be cited for current mathematical
status. analyze_e8_optimal.py and early probes are exploratory history.
The harmless empty-list dedup metadata bug discovered after the terminal
zero count is documented in postprocessing_empty_list_note.txt and fixed.
