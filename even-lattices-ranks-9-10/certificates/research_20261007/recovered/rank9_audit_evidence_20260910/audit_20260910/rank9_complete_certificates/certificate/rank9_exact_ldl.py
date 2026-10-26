"""Small exact-arithmetic helpers for positive quadratic forms.

The enumerator uses an exact LDL^T decomposition and integer square roots.
No floating-point comparison is used for pruning or endpoints.
"""

from fractions import Fraction
from math import isqrt


def exact_ldl(matrix):
    """Return L,D with matrix = L*diag(D)*L^T over Fraction."""
    n = len(matrix)
    L = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    D = [Fraction(0) for _ in range(n)]
    for j in range(n):
        D[j] = Fraction(matrix[j][j]) - sum(
            L[j][k] * L[j][k] * D[k] for k in range(j)
        )
        if D[j] <= 0:
            raise ValueError("matrix is not positive definite")
        for i in range(j + 1, n):
            L[i][j] = (
                Fraction(matrix[i][j])
                - sum(L[i][k] * L[j][k] * D[k] for k in range(j))
            ) / D[j]
    return L, D


def _ceil_div(a, b):
    return -((-a) // b)


def _integer_interval(center, radius_squared):
    """All integers z with (z-center)^2 <= radius_squared, exactly."""
    if radius_squared < 0:
        return range(0)
    center = Fraction(center)
    radius_squared = Fraction(radius_squared)
    a, b = center.numerator, center.denominator
    # |b*z-a|^2 <= b^2 * radius_squared.
    num = b * b * radius_squared.numerator
    den = radius_squared.denominator
    radius_numerator = isqrt(num // den)
    lo = _ceil_div(a - radius_numerator, b)
    hi = (a + radius_numerator) // b
    return range(lo, hi + 1)


def enumerate_vectors(matrix, bound, center=None):
    """Yield all z in Z^n with (z-center)^T Q (z-center) <= bound.

    The output order is deterministic but otherwise unspecified.
    """
    n = len(matrix)
    L, D = exact_ldl(matrix)
    center = [Fraction(0) for _ in range(n)] if center is None else [
        Fraction(x) for x in center
    ]
    if len(center) != n:
        raise ValueError("wrong center dimension")
    z = [0] * n

    def visit(i, remaining):
        if i < 0:
            yield tuple(z)
            return
        adjusted_center = center[i] - sum(
            L[j][i] * (Fraction(z[j]) - center[j])
            for j in range(i + 1, n)
        )
        radius_squared = Fraction(remaining) / D[i]
        for value in _integer_interval(adjusted_center, radius_squared):
            cost = D[i] * (Fraction(value) - adjusted_center) ** 2
            if cost <= remaining:
                z[i] = value
                yield from visit(i - 1, remaining - cost)

    yield from visit(n - 1, Fraction(bound))


def quadratic_value(matrix, vector):
    return sum(
        Fraction(vector[i]) * matrix[i][j] * vector[j]
        for i in range(len(matrix))
        for j in range(len(matrix))
    )


if __name__ == "__main__":
    q = [[2, 1], [1, 2]]
    points = list(enumerate_vectors(q, 6))
    assert all(quadratic_value(q, z) <= 6 for z in points)
    assert set(points) == {
        (x, y)
        for x in range(-3, 4)
        for y in range(-3, 4)
        if 2 * x * x + 2 * x * y + 2 * y * y <= 6
    }
    print("exact LDL enumerator self-test: OK")
