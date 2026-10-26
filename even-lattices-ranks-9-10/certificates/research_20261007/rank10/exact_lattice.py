"""Small exact-arithmetic tools for positive-definite integral lattices.

The routines here deliberately have no non-standard dependencies.  Vector
enumeration uses a rational LDL^T decomposition and *exact* inequality tests;
floating point is not used to decide membership in an ellipsoid.  The
isometry test is the elementary exhaustive test obtained by mapping a basis
to vectors with the prescribed Gram matrix.

This is intended for ranks <= 9 and the very short shells occurring in the
rank-9 saturated-flag search, not as a replacement for a general lattice
package.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import isqrt
from typing import Iterable, Sequence


Matrix = list[list[int]]
Vector = tuple[int, ...]


def determinant(a: Sequence[Sequence[int]]) -> int:
    """Bareiss determinant over Z."""
    n = len(a)
    if n == 0:
        return 1
    m = [list(map(int, row)) for row in a]
    sign = 1
    previous = 1
    for k in range(n - 1):
        if m[k][k] == 0:
            pivot_row = next((i for i in range(k + 1, n) if m[i][k]), None)
            if pivot_row is None:
                return 0
            m[k], m[pivot_row] = m[pivot_row], m[k]
            sign = -sign
        pivot = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = m[i][j] * pivot - m[i][k] * m[k][j]
                assert numerator % previous == 0
                m[i][j] = numerator // previous
        previous = pivot
    return sign * m[-1][-1]


def ldl(a: Sequence[Sequence[int]]) -> tuple[list[list[Fraction]], list[Fraction]]:
    """Return L,D with A=L diag(D) L^T, all entries exact."""
    n = len(a)
    ell = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    dia = [Fraction(0) for _ in range(n)]
    for k in range(n):
        dia[k] = Fraction(a[k][k]) - sum(
            ell[k][h] * ell[k][h] * dia[h] for h in range(k)
        )
        if dia[k] <= 0:
            raise ValueError("matrix is not positive definite")
        for i in range(k + 1, n):
            ell[i][k] = (
                Fraction(a[i][k])
                - sum(ell[i][h] * ell[k][h] * dia[h] for h in range(k))
            ) / dia[k]
    return ell, dia


def qform(a: Sequence[Sequence[int]], x: Sequence[int]) -> int:
    return sum(x[i] * a[i][j] * x[j] for i in range(len(a)) for j in range(len(a)))


def bilinear(a: Sequence[Sequence[int]], x: Sequence[int], y: Sequence[int]) -> int:
    return sum(x[i] * a[i][j] * y[j] for i in range(len(a)) for j in range(len(a)))


def _floor_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator


def _ceil_sqrt_fraction(x: Fraction) -> int:
    """Smallest integer s with s^2 >= x for x>=0."""
    if x <= 0:
        return 0
    # This deliberately overestimates first, then corrects exactly.
    s = isqrt(x.numerator // x.denominator)
    while Fraction(s * s) < x:
        s += 1
    while s and Fraction((s - 1) * (s - 1)) >= x:
        s -= 1
    return s


def _ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def _integer_interval(centre: Fraction, radius_squared: Fraction) -> range:
    """All z in Z with (z-centre)^2 <= radius_squared, exactly."""
    if radius_squared < 0:
        return range(0)
    centre = Fraction(centre)
    radius_squared = Fraction(radius_squared)
    a, b = centre.numerator, centre.denominator
    # |b z-a|^2 is an integer, so flooring the rational right-hand side
    # before integer square root is exact, not an inward approximation.
    rhs_floor = (b * b * radius_squared.numerator) // radius_squared.denominator
    radius_numerator = isqrt(rhs_floor)
    lo = _ceil_div(a - radius_numerator, b)
    hi = (a + radius_numerator) // b
    return range(lo, hi + 1)


def enumerate_vectors(
    a: Sequence[Sequence[int]], bound: int | Fraction, *, include_zero: bool = True
) -> list[tuple[Vector, int]]:
    """Enumerate all x in Z^n with x^T A x <= bound, exactly.

    Completeness follows directly from

        x^T A x = sum_k D[k] (x[k] + sum_{i>k} L[i,k]x[i])^2.

    Every candidate coordinate interval is an integer superset obtained from
    an exact rational square-root ceiling, followed by an exact term test.
    """
    bnd = Fraction(bound)
    if bnd < 0:
        return []
    ell, dia = ldl(a)
    n = len(a)
    x = [0] * n
    answer: list[tuple[Vector, int]] = []

    def rec(k: int, used: Fraction) -> None:
        if k < 0:
            if include_zero or any(x):
                # By the exact LDL identity, used is q(x).  Recomputing the
                # O(n^2) quadratic form at every leaf dominates large class
                # tables and provides no additional completeness argument.
                assert used <= bnd
                answer.append((tuple(x), used))
            return
        remaining = bnd - used
        if remaining < 0:
            return
        centre_shift = sum(ell[i][k] * x[i] for i in range(k + 1, n))
        radius_squared = remaining / dia[k]
        for value in _integer_interval(-centre_shift, radius_squared):
            term = dia[k] * (Fraction(value) + centre_shift) ** 2
            if term <= remaining:
                x[k] = value
                rec(k - 1, used + term)
        x[k] = 0

    rec(n - 1, Fraction(0))
    answer.sort(key=lambda item: (item[1], item[0]))
    return answer


def shell_vectors(a: Sequence[Sequence[int]], norm: int) -> list[Vector]:
    return [x for x, q in enumerate_vectors(a, norm, include_zero=False) if q == norm]


def short_signature(a: Sequence[Sequence[int]], bound: int | None = None) -> tuple:
    """A fairly strong, rigorously isometry-invariant short-shell signature."""
    if bound is None:
        bound = max(a[i][i] for i in range(len(a)))
    points = enumerate_vectors(a, bound, include_zero=False)
    vectors = [x for x, _ in points]
    norms = [q for _, q in points]
    shell_count = tuple(sorted(Counter(norms).items()))
    local_types = []
    for i, v in enumerate(vectors):
        hist = Counter((norms[j], bilinear(a, v, w)) for j, w in enumerate(vectors))
        local_types.append((norms[i], tuple(sorted(hist.items()))))
    return (
        len(a),
        determinant(a),
        bound,
        shell_count,
        tuple(sorted(Counter(local_types).items())),
    )


def _first_nonzero_positive(v: Sequence[int]) -> bool:
    for x in v:
        if x:
            return x > 0
    return False


def isometry(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> Matrix | None:
    """Return integral X with X^T B X=A, or None, by exhaustive basis imaging."""
    n = len(a)
    if len(b) != n or determinant(a) != determinant(b):
        return None
    max_norm = max(a[i][i] for i in range(n))
    points = enumerate_vectors(b, max_norm, include_zero=False)
    by_norm: dict[int, list[Vector]] = {}
    for v, q in points:
        by_norm.setdefault(q, []).append(v)
    if any(a[i][i] not in by_norm for i in range(n)):
        return None

    assigned: dict[int, Vector] = {}
    unused = set(range(n))

    def candidates(i: int) -> list[Vector]:
        result = []
        for v in by_norm[a[i][i]]:
            if not assigned and not _first_nonzero_positive(v):
                # -I is always an automorphism, so this removes exactly the
                # redundant simultaneous sign choice for the first image.
                continue
            if all(bilinear(b, v, w) == a[i][j] for j, w in assigned.items()):
                result.append(v)
        return result

    def rec() -> Matrix | None:
        if not unused:
            # Columns are images of the source basis vectors.
            xmat = [[assigned[j][i] for j in range(n)] for i in range(n)]
            if abs(determinant(xmat)) != 1:
                return None
            for i in range(n):
                for j in range(n):
                    if bilinear(b, assigned[i], assigned[j]) != a[i][j]:
                        return None
            return xmat
        scored = [(len(candidates(i)), i) for i in unused]
        count, i = min(scored)
        if count == 0:
            return None
        cand = candidates(i)
        unused.remove(i)
        for v in cand:
            assigned[i] = v
            result = rec()
            if result is not None:
                return result
        assigned.pop(i, None)
        unused.add(i)
        return None

    return rec()


def deduplicate_isometry(forms: Iterable[Matrix]) -> tuple[list[Matrix], list[int], list[Matrix | None]]:
    """Deduplicate forms; return representatives, representative indices, maps.

    The returned index for input i points into the representatives list, and
    maps[i] is an explicit isometry matrix from input i to that representative
    in the convention X^T Rep X = Input.
    """
    forms = list(forms)
    if not forms:
        return [], [], []
    # A common shell cutoff is essential: two isometric lattices may be
    # presented by bases whose largest diagonal entries are different.
    # Use the common first shell rather than every shell up to the largest
    # basis norm.  The latter can create enormous quadratic-size signatures
    # for a presentation containing an unnecessarily long basis vector.
    # This remains a sound (possibly less discriminating) invariant; any
    # collision is resolved by the exhaustive isometry test below.
    signature_bound = min(min(g[i][i] for i in range(len(g))) for g in forms)
    representatives: list[Matrix] = []
    signatures: list[tuple] = []
    classes: list[int] = []
    maps: list[Matrix | None] = []
    for form in forms:
        sig = short_signature(form, signature_bound)
        found = None
        found_map = None
        for j, (rep, rep_sig) in enumerate(zip(representatives, signatures)):
            if sig != rep_sig:
                continue
            iso = isometry(form, rep)
            if iso is not None:
                found = j
                found_map = iso
                break
        if found is None:
            found = len(representatives)
            representatives.append(form)
            signatures.append(sig)
            found_map = [[int(i == j) for j in range(len(form))] for i in range(len(form))]
        classes.append(found)
        maps.append(found_map)
    return representatives, classes, maps
