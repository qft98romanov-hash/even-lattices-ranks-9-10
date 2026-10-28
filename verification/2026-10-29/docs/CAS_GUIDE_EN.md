# Additional computer algebra checks

These adapters independently reconstruct the **explicit** lattices from
`data/lattices.json`. They do not import the original Python verifier.
The JSON records source paths, hashes, and expected values. Expected values are
assertion targets, never preassigned lattice minima or cached answers.

**Magma, SageMath, and OSCAR/Hecke were not installed in the audit environment.**
Their adapters received source/API review, but their mathematical checks have
not been executed here. The accompanying `*_static_review.json` files say
`NOT_RUN`. A local success requires a zero exit status **and** the final marker
listed below. A source review or Python syntax check is not a CAS run.

## Conventions and expected checks

Every input matrix is a Gram matrix: the squared norm of an integer column
vector is `v^T G v`. Determinants are Gram determinants, not covolumes.

| Lattice | Determinant | Minimum | Norm-6 vectors | Norm-8 vectors | Norm-10 vectors |
|---|---:|---:|---:|---:|---:|
| K9 | 21870 | 6 | 258 | computed, no assertion target | computed, no assertion target |
| K10 | 54675 | 6 | 294 | 216 | 756 |
| K10_alt | 54675 | 6 | 294 | 216 | 762 |

The two rank-ten lattices have different ranks modulo 3, respectively 4 and 3,
and different Smith invariants. Either difference proves nonisometry. Their
actual, unscaled duals have minimum `2/5` and six shortest vectors spanning a
two-dimensional rational space. The E8 input has determinant 1 and shell sizes
240, 2160, 6720, 17520 in squared norms 2, 4, 6, 8.

Magma checks minima, theta coefficients, duals, Smith forms, isometry to a
standard E8, nonisometry of the two rank-ten examples, and automorphism groups.
It prints an exact E8 isometry matrix, Smith transformation matrices, and
automorphism generators; the matrix identities are asserted directly.

SageMath checks the same matrix invariants, shell counts, and dual minima,
with exact checks of every returned vector and of its E8 isometry certificate.
It writes `results/sage_run.json`. Its short-vector and isometry searches use
PARI, so this is not independent of the accompanying PARI adapter at the
enumeration-backend level.

OSCAR/Hecke additionally computes discriminant quadratic modules and checks the
explicit primitive inclusions of K9 and `sqrt(3) E8` in both rank-ten examples.
The orthogonal complements are identified as `sqrt(15) A2` and `sqrt(5) A2`;
the corresponding indices are 9 and 3. It constructs the actual quotient of
each supplied lattice by the sum of these orthogonal sublattices and checks
that this glue quotient is isotropic. This reconstructs the displayed
overlattice descriptions; it does not enumerate all possible glue maps.

## Running the adapters

Run the commands from `verification/2026-10-29` in a checkout or a temporary
copy. The Magma and Julia inputs are deterministic literal exports of the JSON.

```sh
python export_adapters.py
python export_adapters.py --check
```

Use an installed, licensed Magma distribution:

```sh
magma -b check_magma.m > results/magma_run.log 2>&1
```

Required final marker: `ALL_MAGMA_EXPLICIT_CHECKS_PASS`.
`SetQuitOnError(true)` makes syntax/runtime errors terminate the script.
The script explicitly requests `Proof := true`, supplies no heuristic `Prune`
and no truncating `Max`, and constructs the dual using `Rescale := false`.
Magma's default `Dual(L)` rescales and would check a different metric.
`ShortestVectors` returns one representative per sign pair, so its count is
doubled. Theta-series exponents already represent squared norms.

Use SageMath's Python interpreter, not ordinary CPython:

```sh
sage -python check_sage.py > results/sage_run.log 2>&1
```

Required final marker: `ALL_SAGE_EXPLICIT_CROSS_CHECKS_PASS`.
Its result status is deliberately called `PASS_CROSS_CHECK`. Sage interprets
the matrix constructor for `QuadraticForm` as a Hessian: the adapter therefore
uses `QuadraticForm(2*G)`. Its shell bound is strict, hence bound 11 includes
squared norm 10. Both signs are returned and must not be doubled. The dual
Gram matrix is inverted exactly, then multiplied by a recorded integer scale
only for the integer-form enumeration; the reported dual minimum is divided
by that scale.

Install Julia and OSCAR according to their official installation instructions.
For a separate project, choose a directory such as `cas-env`:

```sh
julia --project=cas-env -e 'using Pkg; Pkg.add("Oscar"); Pkg.status()'
julia --project=cas-env check_oscar.jl > results/oscar_run.log 2>&1
```

Required final marker: `ALL_OSCAR_EXPLICIT_CHECKS_PASS`.
The script records Julia and OSCAR versions and checks the JSON SHA256 against
the generated input. It calls Hecke through `Oscar.Hecke`. Short-vector
iterators return sign pairs, so counts are doubled. Retain the environment's
`Project.toml` and `Manifest.toml` with any published run for reproducibility.

Never infer success from an empty log, a missing executable, a partial run, or
the existence of a static-review report. Preserve the command, software
version, exit code, complete log, and input hash for each real run. Existing
review statuses should remain historical; save execution results separately.

## What these checks do and do not establish

Exact determinant, parity, Sylvester-criterion, finite-field rank, Smith-form,
and matrix-congruence checks have elementary exact certificates. A returned
isometry matrix can be verified without trusting the search that found it.
Checking the norm of each enumerated vector certifies membership and length;
it does not alone certify that enumeration was exhaustive.

Magma documents a correctness guarantee for the short-vector/minimum/theta
intrinsics used here when proof mode is enabled and heuristic pruning is not
used. That statement is not extended to every Magma lattice routine, notably
closest-vector routines. Sage's `qfminim` backend is a separate issue: PARI's
floating-point enumeration is useful corroboration, but this adapter does not
turn it into an exact exhaustion certificate. OSCAR's documented operations
are checked as an additional backend; this unexecuted adapter is not itself
an external proof review. The independent rational enumeration in
`check_exact.py` is a separate check, with its own scope and report.

These scripts do **not** prove a universal determinant lower bound, classify
all rank-ten equality cases outside a prescribed subclass, enumerate
primitive embeddings into each specific rank-48 ambient lattice, settle all
cluster-extension inequalities, establish scientific novelty, or replace
human review of the theoretical argument. An equality search in a bounded or
structured family is not a classification of all even lattices.

## Official API references used in the source review

- [Magma lattice construction](https://magma.maths.usyd.edu.au/magma/handbook/text/331)
- [Magma enumeration and proof parameters](https://magma.maths.usyd.edu.au/magma/handbook/text/336)
- [Magma dual lattices and dual quotient](https://magma.maths.usyd.edu.au/magma/handbook/text/334)
- [Magma isometries and automorphism groups](https://magma.maths.usyd.edu.au/magma/handbook/text/356)
- [Magma Smith form](https://magma.maths.usyd.edu.au/magma/handbook/text/280)
- [Magma error termination](https://magma.maths.usyd.edu.au/magma/handbook/text/49)
- [Sage quadratic forms: constructor, vectors, equivalence](https://doc.sagemath.org/html/en/reference/quadratic_forms/sage/quadratic_forms/quadratic_form.html)
- [Sage integer Smith form](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
- [PARI linear algebra and quadratic forms](https://pari.math.u-bordeaux.fr/dochtml/html-stable/Linear_algebra__Vectors__matrices_and_sets.html)
- [OSCAR/Hecke integer lattices](https://docs.oscar-system.org/stable/Hecke/manual/quad_forms/integer_lattices/)
- [Hecke discriminant quadratic modules](https://docs.hecke.thofma.com/stable/manual/quad_forms/discriminant_group)
- [OSCAR installation](https://docs.oscar-system.org/stable/Installation/)

The review checks APIs and conventions against the available official
documentation; it cannot promise compatibility with every past or future CAS
release. Runtime errors must be investigated and fixed, never silently turned
into skipped assertions or reported as successful verification.
