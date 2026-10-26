#!/usr/bin/env python3
"""Conditional on gamma9=2 and archived lower-rank exhaustive certificate."""
import json,sys,time,argparse
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path,default=HERE.parent/'recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate');args=parser.parse_args()
sys.path.insert(0,str(args.baseline))
import verify_e7_branch_exact as e
from exact_lattice import determinant
from verify_rank9_extremal_example_exact import K9

def rootfloor(a,k):
 lo,hi=0,1
 while hi**k<=a:hi*=2
 while lo+1<hi:
  m=(lo+hi)//2
  if m**k<=a:lo=m
  else:hi=m
 return lo
# Conservative threshold exactly requested, so 2D^(8/9)<=15908.
raw=rootfloor(7954**9,8);upper=raw-raw%2
assert upper**8<=7954**9<(raw+1)**8
print('RAW_THRESHOLD',raw,'EVEN_THRESHOLD',upper,flush=True)
# Sharper threshold: floor(2D^(8/9))<=15908 iff 2^9 D^8<15909^9.
sharp_raw=rootfloor((15909**9-1)//2**9,8);sharp=sharp_raw-sharp_raw%2
assert 2**9*sharp**8<15909**9
print('OLD_WINDOW_SHARPER_EVEN_THRESHOLD',sharp,flush=True)
old_sharp=sharp
# The equality addendum additionally establishes completeness for rank8<=15909.
# Rank8 determinant residues0,1 mod4 let us require raw Hermite upper<15912.
sharp_raw=rootfloor((15912**9-1)//2**9,8);sharp=sharp_raw-sharp_raw%2
assert sharp==24450 and 2**9*sharp**8<15912**9
print('EXPANDED_WINDOW_EVEN_THRESHOLD',sharp,flush=True)
parents=[('E8',[r[:8]for r in K9[:8]],F(8,3))]
parents += [(name,e.extend(e.H,cross,last),rho)for name,cross,last,d,rho,bound in e.EXPECTED if name in {'J14580','J15309a'}]
out={'gamma9_assumption':'gamma9<=2','conservative_threshold_raw':raw,'conservative_even_threshold':upper,'old_window_sharp_even_threshold':old_sharp,'sharp_even_threshold':sharp,'uses_equality_endpoint_addendum':True,'parents':[]}
for name,G,rho in parents:
 d,adj,fp,mu,wit,pc=e.discriminant_data(G,rho)
 found=[];first_above=None;first_m1_above=None
 assert d*(8-rho)>sharp # Hence any admissible even last diagonal is6.
 for c,q in mu.items():
  for last in (6,):
   s=F(last)-q;D=d*s
   assert D.denominator==1
   if not(21870<=D):continue
   if D>sharp:
    if first_m1_above is None or D<first_m1_above:first_m1_above=int(D)
    continue
   m=1
   while m*m*s<6:
    if m*m*s+mu[tuple(m*x%d for x in c)]<6:break
    m+=1
   else:found.append({'class':c,'cross':wit[c],'last':last,'determinant':int(D)})
 counts=Counter(r['determinant']for r in found)
 print('PARENT',name,'COUNTS',dict(counts),'NEXT_M1_CANDIDATE',first_m1_above,flush=True)
 assert set(counts)=={21870}
 out['parents'].append({'name':name,'gram':G,'class_count':len(mu),'searched_dual_vectors':pc,'determinant_counts':dict(counts),'first_m1_candidate_above':first_m1_above,'admissible':found})
(HERE/'rank9_gap.json').write_text(json.dumps(out,indent=2))
print('RANK9_DETERMINANT_GAP_EXACT_PASS',flush=True)
