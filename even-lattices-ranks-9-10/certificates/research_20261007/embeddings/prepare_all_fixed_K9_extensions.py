#!/usr/bin/env python3
"""Enumerate all optimal rank10 candidate fibers over the printed K9 section.
Completeness is the 2D equality argument and E8 discriminant bound, not a
heuristic assumption that every rank10 lattice contains E8.
"""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from verify_ambient_embeddings import mm,tr,det,inv
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'rank10'))
from exact_lattice import enumerate_vectors
m=json.loads((ROOT/'printed_matrices.json').read_text());e=json.loads((ROOT/'ambient_embedding_certificates.json').read_text())['embeddings']['P48p_K9'];j=json.loads((ROOT/'A10_exact_cvp_input.json').read_text());G=m['P48p_G'];T=m['P48p_T9'];A=mm(T,G);K=mm(A,tr(T));Ki=inv(K);G8=[r[:8]for r in K[:8]];CE=[[v//3 for v in r]for r in G8];p=[r[-1]for r in K[:8]];Cei=inv(CE);w=[sum(Cei[i][h]*p[h]for h in range(8))for i in range(8)];assert all(x.denominator==1 for x in w);w=[int(x)for x in w];a=tuple(x%3 for x in w)
points=enumerate_vectors(CE,8);best={};rep={}
for v,q in points:
 b=tuple(int(x)%3 for x in v)
 if b not in best or q<best[b]:best[b]=q;rep[b]=list(v)
assert len(best)==6561 and Counter(best.values())=={0:1,2:240,4:2160,6:2240,8:1920}
deep={b for b,v in best.items()if v==8};allowed={b for b in deep if tuple((x-y)%3 for x,y in zip(a,b))in deep};assert len(allowed)==561
selected=[];seen=set()
for b in sorted(allowed):
 if b in seen:continue
 mate=tuple((x-y)%3 for x,y in zip(a,b));assert mate in allowed
 seen|={b,mate};selected.append((b,mate))
assert len(selected)==281 and len(seen)==561
C=j['gram_C'];Ci=inv(C);B=j['basis_B'];Q=e['glue_lifts_Q'];n=39;S=j['scale'];L=[[F(x)for x in r]for r in j['exact_L']];D=[F(x)for x in j['exact_D']];df=j['lower_D_scaled'];lr=j['round_L'];cases=[];classes=set()
def roundint(q):return (q+F(1,2)).numerator//(q+F(1,2)).denominator
for b,mate in selected:
 v=rep[b];q=[sum(CE[i][h]*v[h]for h in range(8))for i in range(8)];corner=F(sum(pi*vi for pi,vi in zip(p,v))+5,3);assert corner.denominator==1;target=q+[int(corner)];coeff9=[sum(Ki[i][h]*target[h]for h in range(9))for i in range(9)];assert sum(target[i]*coeff9[i]for i in range(9))==F(7,2)
 key=tuple(x%1 for x in coeff9);negative=tuple(-x%1 for x in coeff9);assert key not in classes and negative not in classes;classes|={key,negative}
 w0=[sum(Q[i][h]*target[h]for h in range(9))for i in range(48)];g=[r[0]for r in mm(mm(B,G),[[x]for x in w0])];wn=mm(mm([w0],G),[[x]for x in w0])[0][0];co=[-sum(Ci[i][h]*g[h]for h in range(n))for i in range(n)];assert F(wn)-sum(g[i]*Ci[i][h]*g[h]for i in range(n)for h in range(n))==F(7,2);ys=[sum(co[h]*L[h][i]for h in range(i,n))for i in range(n)];bounds=[]
 for i in range(n):
  z=0
  while z<abs(co[i])or(F(z)-abs(co[i]))**2<F(5,2)*Ci[i][i]:z+=1
  bounds.append(z)
 yr=[roundint(y*S)for y in ys];E=[(2+sum(bounds[i+1:]))//2 for i in range(n)]
 # Global overflow bounds for the optional C++ runner.
 for i in range(n):
  cm=abs(yr[i])+sum(bounds[h]*abs(lr[h][i])for h in range(i+1,n));am=S*bounds[i]+cm+E[i]
  assert cm<2**62 and am<2**62 and am*am*df[i]<2**127
 assert abs(wn)+2*sum(abs(g[i])*bounds[i]for i in range(n))+sum(bounds[i]*abs(C[i][h])*bounds[h]for i in range(n)for h in range(n))<2**126
 cases.append({'class_E8':list(b),'mate_E8':list(mate),'target':target,'order':2 if b==mate else 6,'lift_w0':w0,'constant_norm':wn,'linear_g':g,'coefficient_bounds':bounds,'round_y':yr,'center_error_scaled':E,'exact_coefficients':[str(x)for x in co],'exact_y':[str(x)for x in ys]})
assert len(classes)==561
out={'scope':'all optimal determinant54675 rank10 supersections containing printed K9 in P48p','rank':n,'scale':S,'class_pair_count':len(cases),'all_class_count':len(classes),'basis_B':B,'gram_C':C,'lower_D_scaled':df,'round_L':lr,'exact_D':[str(x)for x in D],'exact_L':[[str(x)for x in r]for r in L],'cases':cases}
(ROOT/'all_fixed_K9_extension_inputs.json').write_text(json.dumps(out,indent=2)+'\n')
with(ROOT/'all_fixed_K9_extension_inputs.txt').open('w')as f:
 print(n,S,len(cases),file=f);print(*df,file=f)
 for row in lr:print(*row,file=f)
 for row in C:print(*row,file=f)
 for case in cases:
  print(case['constant_norm'],file=f)
  for key in['round_y','center_error_scaled','coefficient_bounds','linear_g']:print(*case[key],file=f)
print('ALL_FIXED_K9_FIBERS_PREPARED',len(cases),'unsignedclasses',len(classes),'order_distribution',dict(Counter(c['order']for c in cases)))
