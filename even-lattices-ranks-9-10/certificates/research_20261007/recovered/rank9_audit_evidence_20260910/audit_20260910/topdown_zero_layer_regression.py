"""Exact non-application example showing why the added layer guard matters.

G=diag(22,6,6,6,6), c=(1/2,0,0,0,0), s=1/2 and last norm6 give a
rank-six extension of determinant14256.  Its first layer has norm6, but
the second layer contains a norm2 vector.  The old general helper accepts
this presentation; the hardened helper excludes it.  All discriminant
minima supplied below are the exact full table of the diagonal parent.
This does not occur for any of the actual rank-seven parents.
"""
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'rank9_complete_certificates' / 'certificate'))
from verify_rank7_topdown import allowed_one_vector_extensions as old
from verify_rank7_topdown import bareiss_det, border, quadratic_value
from verify_rank7_topdown_hardened import allowed_one_vector_extensions as new

diagonal = [22, 6, 6, 6, 6]
g = [[v * (i == j) for j in range(5)] for i, v in enumerate(diagonal)]
d = bareiss_det(g)
assert d == 28512
best, witnesses = {}, {}
for residue in product(*(range(v) for v in diagonal)):
    z = tuple(r if 2 * r <= v else r - v for r, v in zip(residue, diagonal))
    c = tuple((d // v) * r for r, v in zip(residue, diagonal))
    best[c] = sum((d // v) * x * x for x, v in zip(z, diagonal))
    witnesses[c] = z
assert len(best) == d
target = (d // 2, 0, 0, 0, 0)
assert target in best
old_output = old(g, best, witnesses)
new_output = new(g, best, witnesses)
assert any(row[0] == 14256 and row[1] == target for row in old_output)
assert not any(row[0] == 14256 and row[1] == target for row in new_output)
bad = border(g, [11, 0, 0, 0, 0], 6)
assert bareiss_det(bad) == 14256
assert quadratic_value(bad, [1, 0, 0, 0, 0, -2]) == 2
print('FULL_DIAGONAL_DISCRIMINANT_TABLE', len(best))
print('OLD_HELPER_ACCEPTS_TARGET True')
print('HARDENED_HELPER_ACCEPTS_TARGET False')
print('TARGET_DETERMINANT 14256 SECOND_LAYER_NORM 2')
print('ZERO_CLASS_LAYER_REGRESSION_PASS')
