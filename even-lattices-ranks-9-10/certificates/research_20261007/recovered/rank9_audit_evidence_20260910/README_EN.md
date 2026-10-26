# Rank-nine determinant audit: supplementary evidence

Confidential research material. Audit date: 10 September 2026.

This package records the renewed theoretical, code and computational audit
of the claimed determinant bound

    det(L) >= 21870

for positive definite even integral lattices of rank nine and minimum
squared norm at least six, together with the sharp example K9.

## Outcome and scope

All mandatory released verification programs passed in a fresh isolated
copy. The complete lower-flag search through rank six and all rank-seven
chunks were actually regenerated, with byte-identical results. This is
stronger evidence than re-reading an archived PASS transcript. The
recovered source archive was left unchanged.

The audit also found an actual generic helper defect and several exposition
issues. The helper's centered residue test omitted the nonzero zero-class
layer m=h, where h is the order of the discriminant class. Its required
condition is h^2*s >= 6. An explicit regression demonstrates that the old
helper can accept a minimum-two extension outside the actual proof branches.
In the four actual top-down rank-seven parents, the discriminant radii imply
s >= 6-93/22 = 39/22 > 3/2 whenever h>=2; hence h^2*s>6 automatically. For
h=1, the first layer has s>=6. The omission therefore does not change the
claimed rank-nine bound.

The isolated `verify_rank7_topdown_hardened.py` adds exactly this missing
guard; the remaining changes are explanatory comments. Its focused diff is
included. Its complete fresh execution passed and its transcript is
byte-for-byte identical to the archived top-down transcript. The original
archive remains available as an exact record rather than being silently
overwritten. The lattice labelled `4 E7*` in legacy output has Gram matrix
4 C_E7^{-1} and is Euclidean **2 E7***; the audit reports explain this and
the other necessary terminology/hypothesis corrections.

This package audits the rank-nine determinant subproblem and the specific
certificate chain. It does not audit every result of the source preprint,
the source's ambient rank-48 embeddings, global sphere-packing optimality,
clusters, uniqueness of K9, or rank-ten problems. The mathematical reports
state the imported classical assumptions and the precise packing scope.

## Reproduction

Use ordinary CPython 3 without `-O`; assertions are part of the checks.
No third-party Python packages are required. From this package root:

```bash
sha256sum -c SHA256SUMS
bash run_audit_checks.sh
```

The wrapper runs four new audit programs and the hardened top-down branch:

1. `test_enumeration_independent.py`: independent coordinate-box reference
   enumeration; 10000 interval cases, 36 large-center boundary cases,
   100 rational ellipsoids, 60 determinant checks, exact low-rank class
   minima, and complete rank-one-to-two / rank-two-to-three extension lists.
2. `branch_independent_checks.py`: 51 independent ellipsoid comparisons,
   exact root-reflection identities, direct minimum checks, and an
   independently evaluated determinant and minimum for K9.
3. `verify_theory_and_sharpness.py`: exact Hermite-window arithmetic,
   lifting bounds, and a transparent 64-point residue proof of K9's
   sharpness, without importing any archived module.
4. `topdown_zero_layer_regression.py`: a complete 28512-class diagonal
   example detecting the omitted layer; the old helper accepts the target
   and the hardened helper rejects it.
5. `verify_rank7_topdown_hardened.py`: exact replay of the affected branch
   after adding the missing guard.

To repeat the **original complete certificate replay** and **full search
regeneration**, use a disposable copy because some verifiers rewrite
deterministic reports:

```bash
cp -R audit_20260910/rank9_complete_certificates /your/scratch/rank9-replay
cd /your/scratch/rank9-replay
bash run_all_checks.sh
bash run_full_regeneration.sh
```

Replace `/your/scratch/rank9-replay` with a new writable directory. The
original README and RUN_ORDER give detailed commands. The full regeneration
script creates and removes its own temporary generated data directory.
The supplementary full E6 cross-check is optional and was not rerun in the
renewed audit; its necessary conclusions were checked by the targeted E7
and H6318 programs.

## What was independently implemented, and what was replayed

The full large search replay deliberately reuses the archived generator.
The new independent implementations cover the specified arithmetic kernels,
low-rank extensions, branch checks and 64-point sharpness argument; they do
not constitute a separate implementation of the entire rank-seven search.
The reports separate the mathematical completeness argument, code review,
independent tests, full regeneration and branch replay.

The measured concurrent wall times were 252.900911 seconds for the original
mandatory runner and 230.929221 seconds for full regeneration, on CPython
3.12.14, Linux x86_64, with assertions enabled. These are audit run times,
not dedicated benchmark measurements. Both runners exited 0 with markers
`ALL_RELEASED_EXACT_CERTIFICATES_PASS` and
`FULL_EXACT_REGENERATION_BYTE_IDENTICAL` respectively. All 83 released hashes
passed before and after replay. The five raw lower-flag files were also
compared independently and matched byte for byte.

The line `generator rerun = False` at the end of the regeneration transcript
belongs only to the final static verifier. The preceding transcript records
the actual fresh generation and byte comparisons.

## Contents and integrity

* `audit_20260910/`: theoretical, enumeration, branch and replay reports;
  new scripts, fresh transcripts, focused patch, metadata and local hashes.
* `audit_20260910/rank9_complete_certificates/`: unchanged extracted original
  certificate package, preserving the relative paths used by audit imports.
* `recovered/rank9_complete_certificates.zip`: exact original ZIP, SHA-256
  `608cf4b022d448476028d56f002485ec39c1893b2a2e797458838c64db11d8b3`.
* `manuscripts/`: the final English manuscript (31 PDF pages) and Russian
  manuscript (41 PDF pages), each supplied as a LaTeX `.txt` source and PDF.
  The four files are also delivered separately. The audit reports include
  their final mathematical review; the additional
  `RU_appendix64_extracted.py` and `.transcript` record a successful check
  of the 64-point verification extracted from the Russian appendix.
* `SHA256SUMS`: global hashes of all regular files except this manifest.

For local manifests, run the original certificate manifest from its package
root, `replay_evidence_SHA256SUMS` from `audit_20260910/`, and
`topdown_hardening_sha256.txt` from this supplementary package root. The
global manifest avoids any ambiguity about these working directories.

Recorded absolute scratch paths in historical logs describe the execution
environment; they are not required to reproduce the portable scripts.
To use either LaTeX `.txt` file in Overleaf, copy its entire contents into
`main.tex` and select **XeLaTeX** as the compiler. The English and Russian
sources are independent complete documents. Their ready-to-read PDFs are
included alongside them.
