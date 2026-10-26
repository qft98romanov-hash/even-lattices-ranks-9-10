#!/usr/bin/env python3
"""Full exact arbitrary-precision replay of all optimal extensions of fixed K9.
Not a classification of all embeddings of K9 in P48p. No floating pruning.
"""
import json,sys,time,math
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from verify_ambient_embeddings import mm,tr,det,inv,snf,ldlt
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'rank10'))
from exact_lattice import enumerate_vectors
started=time.monotonic();j=json.loads((ROOT/'all_fixed_K9_extension_inputs.json').read_text());m=json.loads((ROOT/'printed_matrices.json').read_text());G=m['P48p_G'];T=m['P48p_T9'];A=mm(T,G);K=mm(A,tr(T));Ki=inv(K);dk=det(K);assert dk==21870
assert G==tr(G) and all(G[i][i]%2==0 for i in range(48)) and det(G)==1;ldlt(G)
st,_,_=snf(T);assert[st[i][i]for i in range(9)]==[1]*9
n=j['rank'];S=j['scale'];B=j['basis_B'];C=j['gram_C'];df=j['lower_D_scaled'];lr=j['round_L'];L=[[F(x)for x in row]for row in j['exact_L']];D=[F(x)for x in j['exact_D']]
assert n==39 and mm(A,tr(B))==[[0]*n for _ in T]
assert C==mm(mm(B,G),tr(B))and det(C)==dk;Ci=inv(C)
assert all(D[i]>0 and L[i][i]==1 and all(L[i][k]==0 for k in range(i+1,n))for i in range(n))
assert mm(mm(L,[[D[i]if i==k else 0 for k in range(n)]for i in range(n)]),tr(L))==C
for i in range(n):
 assert 0<F(df[i],S)<=D[i]
 for h in range(n):assert abs(F(lr[h][i],S)-L[h][i])<=F(1,2*S)
# Independent reconstruction of the complete E8 candidate-class set.
CE=[[x//3 for x in row[:8]]for row in K[:8]];assert [[3*x for x in row]for row in CE]==[row[:8]for row in K[:8]];assert det(CE)==1;CEi=inv(CE);p=[row[-1]for row in K[:8]];ww=[sum(CEi[i][h]*p[h]for h in range(8))for i in range(8)];assert all(x.denominator==1 for x in ww);a=tuple(int(x)%3 for x in ww)
best={}
for v,q in enumerate_vectors(CE,8):
 key=tuple(x%3 for x in v)
 if key not in best or q<best[key]:best[key]=q
assert len(best)==6561 and Counter(best.values())=={0:1,2:240,4:2160,6:2240,8:1920}
deep={b for b,q in best.items()if q==8};allowed={b for b in deep if tuple((x-y)%3 for x,y in zip(a,b))in deep};assert len(allowed)==561
assert len(j['cases'])==281
covered=set();class_keys=set();totalnodes=0;totalleaves=0;catalog=[];case_results=[];normals=set()
cpp_stats={};cpp_solutions={}
for line in(ROOT/'search_all_fixed_K9_extensions.log').read_text().splitlines():
 z=line.split()
 if z[0]=='CASE':cpp_stats[int(z[1])]=tuple(map(int,[z[3],z[5],z[7]]))
 if z[0]=='EXACT_NORM6_WITNESS':cpp_solutions.setdefault(int(z[1]),[]).append(list(map(int,z[2:])))
assert len(cpp_stats)==281
for caseid,case in enumerate(j['cases']):
 b=tuple(case['class_E8']);mate=tuple(case['mate_E8']);assert b in allowed and mate==tuple((x-y)%3 for x,y in zip(a,b))and mate in allowed;assert b not in covered and mate not in covered;covered|={b,mate}
 target=case['target'];v=[sum(CEi[i][h]*target[h]for h in range(8))for i in range(8)];assert all(x.denominator==1 for x in v);v=[int(x)for x in v];assert tuple(x%3 for x in v)==b;assert sum(v[i]*CE[i][h]*v[h]for i in range(8)for h in range(8))==8;assert 3*target[-1]==sum(x*y for x,y in zip(p,v))+5
 coeff9=[sum(Ki[i][h]*target[h]for h in range(9))for i in range(9)];assert sum(target[i]*coeff9[i]for i in range(9))==F(7,2);key=tuple(x%1 for x in coeff9);negative=tuple(-x%1 for x in coeff9);assert key not in class_keys and negative not in class_keys;class_keys|={key,negative};assert case['order']==(2 if b==mate else 6)
 w=case['lift_w0'];g=case['linear_g'];wn=case['constant_norm'];bounds=case['coefficient_bounds'];yr=case['round_y'];E=case['center_error_scaled'];assert mm(A,[[x]for x in w])==[[x]for x in target];assert g==[r[0]for r in mm(mm(B,G),[[x]for x in w])];assert wn==mm(mm([w],G),[[x]for x in w])[0][0]
 co=[-sum(Ci[i][h]*g[h]for h in range(n))for i in range(n)];assert F(wn)-sum(F(g[i])*Ci[i][h]*g[h]for i in range(n)for h in range(n))==F(7,2);y=[sum(co[h]*L[h][i]for h in range(i,n))for i in range(n)]
 for i in range(n):
  assert bounds[i]>=abs(co[i])and(F(bounds[i])-abs(co[i]))**2>=F(5,2)*Ci[i][i]
  assert abs(F(yr[i],S)-y[i])<=F(1,2*S)
  assert F(E[i],S)>=F(1+sum(bounds[i+1:]),2*S)
 nodes=leaves=0;solutions=[];x=[0]*n
 def rec(k,rem):
  global nodes,leaves
  nodes+=1
  if k<0:
   leaves+=1;val=wn+2*sum(x[i]*g[i]for i in range(n))+sum(x[i]*C[i][h]*x[h]for i in range(n)for h in range(n))
   if val==6:solutions.append(x[:])
   return
  center=yr[k]-sum(x[h]*lr[h][k]for h in range(k+1,n));rad=math.isqrt(rem//df[k])+E[k];lo=max(-bounds[k],-(-(center-rad)//S));hi=min(bounds[k],(center+rad)//S)
  for xi in range(lo,hi+1):
   z=max(0,abs(S*xi-center)-E[k]);term=z*z*df[k]
   if term<=rem:x[k]=xi;rec(k-1,rem-term)
 rec(n-1,5*S**3//2)
 assert(nodes,leaves,len(solutions))==cpp_stats[caseid]
 assert sorted(solutions)==sorted(cpp_solutions.get(caseid,[]))
 totalnodes+=nodes;totalleaves+=leaves
 for sol in solutions:
  ambient=[w[h]+sum(sol[i]*B[i][h]for i in range(n))for h in range(48)];assert mm(A,[[x]for x in ambient])==[[x]for x in target];assert mm(mm([ambient],G),[[x]for x in ambient])[0][0]==6
  TT=T+[ambient];GG=mm(mm(TT,G),tr(TT));assert det(GG)==54675;ss,_,_=snf(TT);assert[ss[i][i]for i in range(10)]==[1]*10
  # A section is determined by the unoriented normal line to K9. All normals
  # here have the same squared length5/2, hence lines agree exactly iff +/-.
  normal=tuple(int(dk*(ambient[h]-sum(T[i][h]*coeff9[i]for i in range(9))))for h in range(48));neg=tuple(-x for x in normal);assert normal not in normals and neg not in normals;normals|={normal,neg}
  assert case['order']==6
  catalog.append({'case_id':caseid,'target_pairings':target,'new_ambient_vector':ambient,'gram_matrix':GG,'primitive_smith':[1]*10,'normal_numerator':list(normal),'normal_denominator':dk})
 case_results.append({'case_id':caseid,'nodes':nodes,'leaves':leaves,'norm6_count':len(solutions)})
 if caseid%10==0 or solutions:print('CASE',caseid,'NODES',nodes,'LEAVES',leaves,'SOLUTIONS',len(solutions),'ELAPSED',round(time.monotonic()-started,2),flush=True)
 checkpoint={'completed_cases':caseid+1,'total_nodes':totalnodes,'total_leaves':totalleaves,'sections':catalog,'case_results':case_results}
 (ROOT/'all_fixed_K9_extensions_checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
assert covered==allowed and len(class_keys)==561
assert len(catalog)==19 and len(normals)==38
result={'result':'EXACTLY_19_OPTIMAL_RANK10_SUPERSECTIONS_OF_PRINTED_K9_IN_P48p','scope':'fixed printed K9 sublattice; does not classify all K9 embeddings or all ambient automorphism orbits','determinant':54675,'source_minimum':6,'E8_admissible_classes':561,'signed_class_pairs':281,'total_nodes':totalnodes,'total_leaves':totalleaves,'number_distinct_supersections':len(catalog),'all_19_isometric_to_original_K10_by_E8_equality_classification':True,'alternative_A10_count':0,'elapsed_seconds':time.monotonic()-started,'sections':catalog,'case_results':case_results,'arithmetic':'exact Python integers/Fraction/math.isqrt; every case matches independent C++ enumeration; sections deduplicated by unoriented residual normal'}
(ROOT/'all_fixed_K9_extensions_verified.json').write_text(json.dumps(result,indent=2)+'\n');print('ALL_281_FIBERS_VERIFIED',totalnodes,totalleaves,'EXACTLY_19_DISTINCT_SUPERSECTIONS',flush=True)
