from itertools import product
from collections import Counter

C = [
 [ 2,-1,-1,-1,-1,-1,-1, 1],
 [-1, 2, 1, 1, 1, 1, 1, 0],
 [-1, 1, 2, 0, 1, 0, 0,-1],
 [-1, 1, 0, 2, 1, 1, 1, 0],
 [-1, 1, 1, 1, 2, 1, 1,-1],
 [-1, 1, 0, 1, 1, 2, 1, 0],
 [-1, 1, 0, 1, 1, 1, 2, 0],
 [ 1, 0,-1, 0,-1, 0, 0, 2],
]
w = (-1,-1,2,-1,0,0,1,1)
p = (-2,1,3,-1,1,0,1,-1)
assert tuple(sum(C[i][j]*w[j] for j in range(8))
             for i in range(8)) == p

def q(x):
    return sum(x[i]*C[i][j]*x[j]
               for i in range(8) for j in range(8))

choices = [(-1,2)]*4 + [(0,),(0,)] + [(-2,1)]*2
hist = Counter(q(r) for r in product(*choices))
assert sum(hist.values()) == 64
assert q(w) == 8
assert 2 not in hist
assert hist == {
    8:5,14:9,20:14,26:10,32:8,38:5,
    44:4,50:4,56:1,62:3,86:1
}
print("K9_64_POINT_COSET_CHECK_PASS")
