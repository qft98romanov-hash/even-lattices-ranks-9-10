#!/usr/bin/env python3
"""Exact equality addendum to the released rank-nine lower-bound certificate.

Run with assertions enabled (never python -O):
  python verify_equality.py --baseline /path/to/original/certificate

This re-executes every NEW endpoint search, then all equality-class searches.
It depends on the released exhaustive lower-rank certificate for completeness
of the 118 rank-five parents and 138 rank-six parents, the 2235 old rank-seven
extensions, and the previously verified classifications below d8=15909.
It does not claim to regenerate those old searches by itself.
"""
from pathlib import Path
import argparse,json,sys,time,hashlib
from fractions import Fraction as F
from collections import Counter,deque

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--baseline',type=Path,default=HERE.parent/'recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate')
parser.add_argument('--output',type=Path,default=HERE/'equality_verification.json')
args=parser.parse_args()
assert __debug__, 'Assertions must be enabled'
BASE=args.baseline.resolve()
sys.path.insert(0,str(BASE))
import verify_e7_branch_exact as e
from exact_lattice import determinant,enumerate_vectors,ldl
from extend_flag import extend_parent
from verify_rank9_extremal_example_exact import K9


def load(name):return json.loads((BASE/name).read_text())
def transpose(a):return list(map(list,zip(*a)))
def multiply(a,b):return [[sum(a[i][k]*b[k][j]for k in range(len(b)))for j in range(len(b[0]))]for i in range(len(a))]
def iso_check(source,target,U):
 assert abs(determinant(U))==1
 assert multiply(multiply(transpose(U),target),U)==source

def exact_root_floor(value,n):
 lo,hi=0,1
 while hi**n<=value:hi*=2
 while lo+1<hi:
  m=(lo+hi)//2
  if m**n<=value:lo=m
  else:hi=m
 assert lo**n<=value<(lo+1)**n
 return lo

def congruence_upper(x,r):
 if r%2:return x-x%2
 while x%4 not in {0,(-1)**(r//2)%4}:x-=1
 return x

start=time.time();result={}
# At equality the old bound floor15908 must NOT be reused blindly.
raw8=exact_root_floor(F(2**72*21870**56),63)
assert raw8==15910
windows={8:{'raw':raw8,'upper':congruence_upper(raw8,8)}}
gamma={2:F(4,3),3:F(2),4:F(4),5:F(8),6:F(64,3),7:F(64),8:F(256)}
for r in range(8,1,-1):
 raw=exact_root_floor(gamma[r]*windows[r]['upper']**(r-1),r)
 windows[r-1]={'raw':raw,'upper':congruence_upper(raw,r-1)}
assert [windows[r]['upper']for r in range(1,9)]==[6,39,178,633,1894,4648,9494,15909]
result['equality_windows']=windows
print('EQUALITY_UPPER_WINDOWS',windows,flush=True)

# These are the only extra lower-rank determinants relative to the archive.
boundaries=[]
for rank,filename,target,mod,res in [(6,'rank5_isometry_classes.json',4648,4,{0,3}),(7,'rank6_isometry_classes.json',9494,2,{0})]:
 parents=load(filename)['representatives'];stats=[]
 assert len(parents)=={6:118,7:138}[rank]
 for i,G in enumerate(parents):
  children,st=extend_parent(G,target,target,mod,res)
  assert not children,(rank,i,'new boundary lattice must be classified')
  stats.append(st)
 print('EMPTY_ENDPOINT',rank,target,'parents',len(parents),flush=True)
 boundaries.append({'rank':rank,'determinant':target,'parent_count':len(parents),'children':0,'stats':stats})
result['lower_endpoints']=boundaries

# The larger d8 upper bound leaves exactly the same six rank-seven classes.
merged=load('rank7_merged.json');parents6=load('rank6_isometry_classes.json')['representatives']
assert len(merged['children'])==2235
survivors=set();pairs=Counter()
for i,(G,j)in enumerate(zip(merged['children'],merged['child_parent_indices'])):
 d6,d7=determinant(parents6[j]),determinant(G)
 if F(3*d7*d7,4*d6)<=15909:survivors.add(i);pairs[d6,d7]+=1
assert pairs==Counter({(2187,4374):2,(2187,6318):54,(2835,7722):32,(4096,8192):1,(3240,8100):1,(3267,7986):6})
linkage=load('rank7_survivor_linkage_exact.json');covered=set()
for group in linkage['groups']:
 for item in group['maps']:
  i=item['merged_serial'];iso_check(merged['children'][i],group['target_gram'],item['X']);covered.add(i)
assert survivors==covered and len(survivors)==96
result['lifting_survivors']=[{'d6':a,'d7':b,'count':c}for(a,b),c in sorted(pairs.items())]
print('LIFTING_SURVIVORS_96_SIX_CLASSES',flush=True)

boundary8=[]
for group in linkage['groups']:
 children,stats=extend_parent(group['target_gram'],15909,15909,4,{0,1})
 assert not children,(group['label'],'new rank8 boundary must be classified')
 boundary8.append({'label':group['label'],'children':0,'stats':stats})
 print('EMPTY_RANK8_ENDPOINT',group['label'],flush=True)
result['rank8_endpoint_15909']=boundary8

# Original branch classifications now apply throughout the equality window.
# Their strict bounds leave only the following three equality parents.
parent_list=[('sqrt3E8',[r[:8]for r in K9[:8]],F(8,3))]
parent_list += [(name,e.extend(e.H,cross,last),rho)for name,cross,last,d,rho,bound in e.EXPECTED if name in {'J14580','J15309a'}]
saved_isometries=json.loads((HERE/'equality_isometries.json').read_text())
equality=[]
for name,G,rho in parent_list:
 assert not enumerate_vectors(G,5,include_zero=False)
 d,adj,fp,mu,wit,point_count=e.discriminant_data(G,rho)
 assert max(mu.values())==rho
 s=F(21870,d);candidates=[]
 for c,q in mu.items():
  last=s+q
  if last.denominator!=1 or last%2:continue
  m=1
  while m*m*s<6:
   if m*m*s+mu[tuple((m*x)%d for x in c)]<6:break
   m+=1
  else:
   child=e.extend(G,list(wit[c]),int(last))
   assert determinant(child)==21870
   candidates.append((c,child))
 assert len(candidates)=={'sqrt3E8':1920,'J14580':1,'J15309a':2}[name]
 entry={'parent':name,'parent_gram':G,'parent_determinant':d,'schur':str(s),'radius':str(rho),'dual_points':point_count,'class_count':len(mu),'equality_class_count':len(candidates)}
 if name=='sqrt3E8':
  C=[[x//3 for x in row]for row in G]
  generators=[]
  for k in range(8):
   R=[[int(i==j)-(C[k][j]if i==k else 0)for j in range(8)]for i in range(8)]
   iso_check(G,G,R);generators.append(R)
  p0=tuple(row[-1]for row in K9[:8]);c0=fp(p0)
  assert mu[c0]==rho
  queue=deque([c0]);seen={c0};orbit_tree=[]
  while queue:
   c=queue.popleft();p=wit[c]
   for k in range(8):
    pnew=tuple(p[j]-p[k]*C[k][j]for j in range(8));cc=fp(pnew)
    assert mu[cc]==mu[c]
    if cc not in seen:
     seen.add(cc);queue.append(cc);orbit_tree.append({'from':c,'to':cc,'reflection':k})
  assert seen=={c for c,_ in candidates}
  entry['reflection_generators']=generators;entry['orbit_tree']=orbit_tree
  entry['canonical_cross']=p0;entry['orbit_size']=len(seen)
 else:
  isometries=[]
  for c,child in candidates:
   saved=next(row for row in saved_isometries if row['gram']==child)
   U=saved['to_K9'];iso_check(child,K9,U)
   isometries.append({'class':c,'gram':child,'U':U})
  entry['isometries_to_K9']=isometries
 equality.append(entry)
 print('EQUALITY_PARENT',name,'classes',len(candidates),'all_isometric_K9',flush=True)
result['equality_parents']=equality

assert determinant(K9)==21870
ldl(K9)
short=enumerate_vectors(K9,6,include_zero=False)
assert len(short)==258 and all(q==6 for _,q in short)
result['unique_representative']=K9
result['minimal_vectors']=258
result['conclusion']='Relative to the released exhaustive lower-bound certificate, every even integral positive definite rank9 lattice with squared minimum at least6 and Gram determinant21870 is integrally isometric to K9.'
used=['exact_lattice.py','extend_flag.py','verify_e7_branch_exact.py','verify_rank9_extremal_example_exact.py','rank5_isometry_classes.json','rank6_isometry_classes.json','rank7_merged.json','rank7_survivor_linkage_exact.json']
result['baseline_sha256']={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest()for name in used}
result['elapsed_seconds']=time.time()-start
args.output.write_text(json.dumps(result,indent=2))
print('RANK9_EQUALITY_UNIQUE_K9_EXACT_PASS',flush=True)
print('SECONDS',result['elapsed_seconds'],flush=True)
