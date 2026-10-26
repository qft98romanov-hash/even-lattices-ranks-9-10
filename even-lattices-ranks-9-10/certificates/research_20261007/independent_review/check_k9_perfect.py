from pathlib import Path
import sys, json
from fractions import Fraction as F
base=Path(__file__).resolve().parents[1]
cert=base/'recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate'
sys.path.insert(0,str(cert))
from verify_rank9_extremal_example_exact import K9
from exact_lattice import enumerate_vectors, determinant
V=[v for v,q in enumerate_vectors(K9,6,include_zero=False) if q==6]
Vplus=[v for v in V if next(x for x in v if x)!=0 and next(x for x in v if x)>0]
rows=[[v[i]*v[j] for i in range(9) for j in range(i,9)] for v in Vplus]
echelon={}
independent=[]
for idx,row in enumerate(rows):
    r=list(map(F,row))
    for pivot,v in sorted(echelon.items()):
        if r[pivot]:
            a=r[pivot]
            r=[x-a*y for x,y in zip(r,v)]
    pivot=next((i for i,x in enumerate(r) if x),None)
    if pivot is not None:
        a=r[pivot]
        echelon[pivot]=[x/a for x in r]
        independent.append(idx)
rank=len(echelon)
assert len(V)==258 and len(Vplus)==129 and rank==45
minor_rows=[rows[i] for i in independent]
minor_det=determinant(minor_rows)
assert minor_det!=0
result={'rank':9,'minimal_vectors':258,'antipodal_pairs':129,'outer_product_span_rank':rank,'independent_pair_indices':list(independent),'independent_45_by_45_determinant':str(minor_det),'minimal_vectors_positive':Vplus,'scope':'K9 is a perfect form. This alone does not prove determinant minimality or equality classification.'}
(base/'independent_review/k9_perfect_certificate.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='minimal_vectors_positive'},indent=2))
