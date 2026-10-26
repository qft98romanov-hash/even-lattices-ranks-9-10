#!/usr/bin/env python3
from pathlib import Path
import json,sys
from exact_lattice import determinant
src=Path(sys.argv[1]);dst=Path(sys.argv[2])
a=json.loads(src.read_text())['representatives'];d=json.loads(dst.read_text());reps=d['representatives'];ids=d['raw_to_class'];maps=d['isometry_maps']
assert len(a)==len(ids)==len(maps)==d['raw_count']
for k,(G,j,U) in enumerate(zip(a,ids,maps)):
    H=reps[j];n=len(G)
    assert abs(determinant(U))==1
    HU=[[sum(H[i][z]*U[z][j]for z in range(n))for j in range(n)]for i in range(n)]
    assert [[sum(U[z][i]*HU[z][j]for z in range(n))for j in range(n)]for i in range(n)]==G
print('ALL_RAW_CANDIDATES_HAVE_CHECKED_UNIMODULAR_ISOMETRY',len(a),'REPRESENTATIVES',len(reps))
