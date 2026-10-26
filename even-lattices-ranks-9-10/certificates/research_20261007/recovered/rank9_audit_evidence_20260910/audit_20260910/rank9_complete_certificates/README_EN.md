# Exact certificates for the rank-nine determinant theorem

## Certified statement

The intended final certificate proves the following computer-assisted
theorem.

> If `L` is a positive-definite even integral lattice of rank 9 and
> `min(L) >= 6`, then `det(L) >= 21870`.

The preprint supplies an example `K_9` with minimum 6 and determinant 21870.
Consequently, once the lower bound is combined with that independent example,
the minimum possible determinant is exactly 21870.

The bundle includes a separate exact verification of the displayed example
`K_9`. It does **not** claim uniqueness of this optimizer or a classification
of all rank-nine lattices.

## Proof architecture

Assume for contradiction that `det(L_9) < 21870`.  Successive primitive
hyperplane sections selected by shortest dual vectors give a saturated flag

```text
L_1 < L_2 < ... < L_9
```

whose determinants lie in the exact windows

| rank | determinant window | congruence |
|---:|---:|---:|
| 1 | 6 | -- |
| 2 | 27--39 | 0 or 3 modulo 4 |
| 3 | 108--178 | 0 modulo 2 |
| 4 | 324--633 | 0 or 1 modulo 4 |
| 5 | 972--1894 | 0 modulo 2 |
| 6 | 2187--4647 | 0 or 3 modulo 4 |
| 7 | 4374--9492 | 0 modulo 2 |
| 8 | 6564--15908 | 0 or 1 modulo 4 |

The exact lower-chain enumeration yields respectively

```text
rank:       1   2   3   4    5    6
classes:    1   5  14  47  118  138
raw new:        7  52 279 1456 1905
```

Extending all 138 rank-six classes gives 2235 raw rank-seven forms.  If
`d_i = det(L_i)` and `lambda_1(L_7^*) = d_6/d_7`, the shortest-normal
condition at the next step implies

```text
d_8 >= 3 d_7^2 / (4 d_6).
```

Of 31 determinant pairs, this leaves only six (96 of the 2235 raw forms),
and eliminates the other 25 pairs (2139 raw forms). Exact integral
isometries collapse the 96 raw survivors to six rank-seven classes;
independent exact branch certificates then show that none has a rank-nine
continuation of determinant below 21870.

| `(d_6,d_7)` | rank-seven class | exact exclusion |
|---:|---|---:|
| `(2187,4374)` | `sqrt(3)E_7` | `d_9 >= 21870` |
| `(2187,6318)` | `H_6318` | `d_9 >= 32076` |
| `(2835,7722)` | `D_7722` | no flag-compatible `L_8`; the redundant unrestricted candidate has `d_9 >= 36504` |
| `(4096,8192)` | `4E_7^*` | `d_8 >= 20480 > 15908` |
| `(3240,8100)` | `R_8100` | `d_8 >= 18225 > 15908` |
| `(3267,7986)` | `R_7986` | unique flag-compatible `L_8` class, `d_8=14641`; then `d_9 >= 39930` |

The flag windows use the classical exact Hermite constants in dimensions at
most eight together with Mordell's inequality. These mathematical inputs are
assumptions of the finite certificate and are not reproved by the programs.

## Arithmetic and software

All decisions relevant to the theorem use integers or Python
`fractions.Fraction`.  Ellipsoid enumeration uses exact LDL bounds and exact
integer square roots.  Isometries are accompanied by explicit unimodular
integer matrices.  No floating-point comparison is used as a proof step.

Required software:

- CPython 3.12 or later;
- the Python standard library only for the final certificate scripts;
- a POSIX shell and `sha256sum` for the convenience runner.

Some historical exploratory scripts use NumPy.  They are not part of the
logical certificate and are omitted from the release bundle.

## Reproduction

The release contains `run_all_checks.sh`. From the extracted root,
run

```bash
./run_all_checks.sh
```

The runner verifies pinned input hashes and executes the exact audit scripts.
The expensive rank-six-to-rank-seven enumeration is distributed as saved
chunks and is audited exactly; commands for regenerating the chunks from
scratch are documented in `RUN_ORDER.md`.

For a byte-for-byte regeneration of the complete lower flag and all four
rank-seven chunks, run `./run_full_regeneration.sh`. This is substantially
slower than auditing the saved certificates.

The archive also contains the passing supplemental full-`sqrt(3)E_6` branch
certificate. Its targeted E7 and H6318 consequences are rerun by
`run_all_checks.sh`; the larger redundant computation is retained with its
transcript and hashes but is not rerun by default.

See also:

- `ASSUMPTIONS_EN.md` for the human mathematical inputs and scope limits;
- `RUN_ORDER.md` for the exact regeneration and audit order;
- `CLAIMS_TO_CERTIFICATES.md` for the mathematical claim-to-file map;
- `SHA256SUMS` for the released-file manifest.

## Release status

All certificate families listed in `CLAIMS_TO_CERTIFICATES.md` are present.
The release ZIP was checked with `unzip -t`, extracted into a fresh temporary
directory, and verified there with `sha256sum -c SHA256SUMS`.
