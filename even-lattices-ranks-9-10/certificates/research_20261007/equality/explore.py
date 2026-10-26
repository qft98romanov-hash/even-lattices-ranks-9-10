import sys,json,time
from pathlib import Path
from fractions import Fraction as F
BASE=Path('/workspace/scratch/e3fcbd7c9568/research_20261007/recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate')
sys.path.insert(0,str(BASE))
import verify_e7_branch_exact as e
from verify_rank9_extremal_example_exact import K9
from exact_lattice import determinant,enumerate_vectors,isometry

D=21870
lo,hi=0,20000
while lo+1<hi:
 m=(lo+hi)//2
 if m**63<=2**72*D**56:lo=m
 else:hi=m
upper=lo
while upper%4 not in {0,1}:upper-=1
print('d8 floor',lo,'mod4 upper',upper,flush=True)
parents=[('E8',[r[:8] for r in K9[:8]],F(8,3))]
parents += [(name,e.extend(e.H,cross,last),rad) for name,cross,last,d,rad,b in e.EXPECTED if name in ('J14580','J15309a')]
results=[]
for name,G,rad in parents:
 t=time.time();print('parent',name,flush=True)
 d,adj,fp,mu,wit,pc=e.discriminant_data(G,rad)
 s=F(21870,d)
 candidates=[]
 for c,q in mu.items():
  last=s+q
  if last.denominator!=1 or last%2 or last<6:continue
  m=1
  while m*m*s<6:
   mc=tuple((m*x)%d for x in c)
   if m*m*s+mu[mc]<6:break
   m+=1
  else:
   C=e.extend(G,list(wit[c]),int(last));assert determinant(C)==21870
   candidates.append({'class':c,'cross':wit[c],'last':int(last),'gram':C})
 print('done',name,'points',pc,'classes',len(mu),'deep',sum(q==rad for q in mu.values()),'admissible',len(candidates),'seconds',time.time()-t,flush=True)
 results.append({'name':name,'gram':G,'det':d,'radius':str(rad),'count':len(candidates),'candidates':candidates})
 Path(__file__).with_name('equality_candidates.json').write_text(json.dumps(results,indent=2))
