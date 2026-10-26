#!/usr/bin/env python3
"""Targeted exact certificate for the residual H_6318 branch.

This wrapper deliberately skips the already certified full E6 subtree.  It
starts from the standard Gram matrix H_6318, enumerates every even integral
one-vector extension of minimum at least six in the rank-eight determinant
window, identifies the two resulting isometry types by explicit unimodular
maps, and computes their exact discriminant glue radii.  All arithmetic and
ellipsoid membership decisions are exact.
"""

from collections import Counter
from fractions import Fraction as F

from verify_e6_branch_exact import (
    H6318,
    J12393,
    J13689,
    classify_one_vector_extensions,
    det_bareiss,
    discriminant_data,
    find_isometry,
    minimum_vectors,
)


def main() -> None:
    print("EXACT CERTIFICATE: H_6318 RESIDUAL BRANCH")
    print("arithmetic = integers and fractions only")
    assert det_bareiss(H6318) == 6318
    assert minimum_vectors(H6318, 6)

    d, _fp, minima, _witnesses, points, children = (
        classify_one_vector_extensions(H6318, F(9, 2), 6564, 15908)
    )
    assert d == 6318
    rho = max(minima.values())
    assert rho == F(105, 26)
    assert len(children) == 12
    assert Counter(x["det"] for x in children) == Counter({13689: 10, 12393: 2})

    targets = {12393: J12393, 13689: J13689}
    type_counts = Counter()
    for child in children:
        target = targets[child["det"]]
        x = find_isometry(child["gram"], target)
        assert x is not None
        assert abs(det_bareiss(x)) == 1
        type_counts[child["det"]] += 1
    assert type_counts == Counter({13689: 10, 12393: 2})

    target_data = []
    for name, gram, expected_det, expected_rho, search_bound, expected_floor in (
        ("J12393", J12393, 12393, F(58, 17), F(7, 2), 32076),
        ("J13689", J13689, 13689, F(10, 3), F(7, 2), 36504),
    ):
        det, _fp2, minima2, _w2, point_count = discriminant_data(
            gram, search_bound
        )
        assert det == expected_det
        radius = max(minima2.values())
        assert radius == expected_rho
        floor = det * (6 - radius)
        assert floor.denominator == 1 and floor.numerator == expected_floor
        target_data.append((name, det, radius, point_count, floor.numerator))

    print("det(H6318) =", d)
    print("dual points for H6318 =", points)
    print("discriminant classes =", len(minima))
    print("rho(H6318)^2 =", rho)
    print("labelled rank-8 extensions =", len(children))
    print("determinant counts =", sorted(type_counts.items()))
    for name, det, radius, point_count, floor in target_data:
        print(
            name,
            "det =", det,
            "rho^2 =", radius,
            "dual points =", point_count,
            "rank-9 floor =", floor,
        )
    print("H6318_BRANCH_EXACT_OK")


if __name__ == "__main__":
    main()
