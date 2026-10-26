#!/usr/bin/env python3
"""Exact finite checks for all-diameter cluster optimality over the displayed K9,K10.

Uses integers, Fraction and exhaustive combinations only. The accompanying
proof supplies the infinite-to-finite geometric bounds. No floating-point
calculation decides any assertion. The tiny triangular-lattice clique checks
have no vertex cap, clique cap, timeout or omitted diameter.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, isqrt
import json
from pathlib import Path

K9=[
[6,-3,-3,-3,-3,-3,-3,3,-2],
[-3,6,3,3,3,3,3,0,1],
[-3,3,6,0,3,0,0,-3,3],
[-3,3,0,6,3,3,3,0,-1],
[-3,3,3,3,6,3,3,-3,1],
[-3,3,0,3,3,6,3,0,0],
[-3,3,0,3,3,3,6,0,1],
[3,0,-3,0,-3,0,0,6,-1],
[-2,1,3,-1,1,0,1,-1,6]]
p=[1,-1,1,0,-1,-2,-2,1,2]
K10=[row+[p[i]] for i,row in enumerate(K9)]+[p+[6]]
p9=[row[8] for row in K9[:8]]
K10_alt=[row[:8]+[p9[i],-p9[i]] for i,row in enumerate(K9[:8])]+[p9+[6,-1],[-v for v in p9]+[-1,6]]

def inverse(M):
 n=len(M);A=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(M)]
 for j in range(n):
  i=next(i for i in range(j,n) if A[i][j]);A[i],A[j]=A[j],A[i]
  t=A[j][j];A[j]=[v/t for v in A[j]]
  for i in range(n):
   if i!=j:
    t=A[i][j];A[i]=[a-t*b for a,b in zip(A[i],A[j])]
 return [r[n:] for r in A]

def determinant(M):
 A=[[F(v) for v in r] for r in M];n=len(A);d=F(1)
 for j in range(n):
  i=next(i for i in range(j,n) if A[i][j])
  if i!=j:A[i],A[j]=A[j],A[i];d=-d
  t=A[j][j];d*=t
  for i in range(j+1,n):
   s=A[i][j]/t;A[i]=[a-s*b for a,b in zip(A[i],A[j])]
 return d

def short_vectors(M,bound):
 # Rational LDL decomposition and exact integer intervals, independent copy.
 n=len(M);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
 for k in range(n):
  d=F(M[k][k])-sum(L[k][h]**2*D[h] for h in range(k));assert d>0;D.append(d)
  for i in range(k+1,n):L[i][k]=(F(M[i][k])-sum(L[i][h]*L[k][h]*D[h] for h in range(k)))/d
 x=[0]*n;answer=[]
 def rec(k,left):
  if k<0:
   if any(x):answer.append(tuple(x))
   return
  c=-sum(L[i][k]*x[i] for i in range(k+1,n));v=left/D[k]
  den=c.denominator;num=c.numerator;r=isqrt((den*den*v.numerator)//v.denominator)
  lo=-((-(num-r))//den);hi=(num+r)//den
  for a in range(lo,hi+1):
   term=D[k]*(a-c)**2
   assert term<=left
   x[k]=a;rec(k-1,left-term)
  x[k]=0
 rec(n-1,F(bound));return answer

def schur(G,r=8):
 I=inverse([row[:r] for row in G[:r]])
 return [[F(G[i][j])-sum(G[i][a]*I[a][b]*G[b][j] for a in range(r) for b in range(r)) for j in range(r,len(G))] for i in range(r,len(G))]

# C is the Gram matrix of an even positive-definite unimodular rank-eight lattice.
C=[[F(v,3) for v in row[:8]] for row in K9[:8]]
assert all(v.denominator==1 for row in C for v in row)
assert all(C[i][i]%2==0 for i in range(8))
assert all(determinant([r[:i] for r in C[:i]])>0 for i in range(1,9))
assert determinant(C)==1
Ci=inverse(C)
assert all(v.denominator==1 for row in Ci for v in row)
assert all(Ci[i][i]%2==0 for i in range(8))
assert determinant(K9)==21870 and determinant(K10)==54675
assert short_vectors(K9,5)==[] and short_vectors(K10,5)==[]
assert K9[0][0]==K10[0][0]==6
assert determinant(K10_alt)==54675
assert short_vectors(K10_alt,5)==[] and K10_alt[0][0]==6
assert inverse(schur(K9))==[[F(3,10)]]
assert inverse(schur(K10))==[[F(2,5),F(-1,5)],[F(-1,5),F(2,5)]]
assert schur(K10_alt)==schur(K10)

# Exact anticodes in T = A2/sqrt(5), Q(a,b) = 2(a²-ab+b²).
# Q(a,b)>=3a²/2 and >=3b²/2; Q<14 implies |a|,|b|<=3.
def Q(v):a,b=v;return 2*(a*a-a*b+b*b)
def dist(u,v):return Q((u[0]-v[0],u[1]-v[1]))
all13=[(a,b) for a in range(-3,4) for b in range(-3,4) if Q((a,b))<14]
assert sorted(set(Q(v) for v in all13))==[0,2,6,8]
tri=[]
for cap,maximum in [(2,3),(6,4),(8,7)]:
 pts=[v for v in all13 if 0<Q(v)<=cap]
 def clique(vs):return all(dist(u,v)<=cap for u,v in combinations(vs,2))
 witness=next(vs for vs in combinations(pts,maximum-1) if clique(vs))
 # Any larger cluster translates to one containing zero; it would include
 # maximum nonzero points forming a clique. Exhaust every such combination.
 tested=0
 for vs in combinations(pts,maximum):
  tested+=1
  assert not clique(vs)
 assert tested==comb(len(pts),maximum)
 tri.append({'squared_diameter':str(F(cap,5)),'max_size':maximum,'points_in_ball':len(pts)+1,'forbidden_subsets_checked':tested,'witness':[[0,0]]+[list(v) for v in witness]})

# Cross-fiber lower bound for T: for nonzero a,b in T,
# max(||a+b||²,||a-b||²)/4 >= 3/10.
# If one norm >=6/5, sum norms/4 >=2/5. Otherwise both are roots.
roots=[v for v in all13 if Q(v)==2]
root_bounds=[]
for a in roots:
 for b in roots:
  v=F(max(Q((a[0]+b[0],a[1]+b[1])),Q((a[0]-b[0],a[1]-b[1]))),20)
  assert v>=F(3,10);root_bounds.append(v)
assert min(root_bounds)==F(3,10)

# Elementary projected r-distance polynomial dimension bounds.
assert sum(comb(8+2-j,2-j) for j in range(3))==55
assert sum(comb(8+3-j,3-j) for j in range(4))==220

# Each row covers [left,right), with cardinality <=B for a nontrivial cluster.
# Ratio squared = s²(1-beta/6)^(48-rank); monotone in beta.
intervals9=[(F(3,10),F(2,3),2),(F(2,3),F(7,10),9),(F(7,10),F(29,30),10),(F(29,30),F(4,3),27),(F(4,3),F(28,15),111),(F(28,15),F(2),165),(F(2),F(5,2),660),(F(5,2),F(6),21870)]
intervals10=[(F(2,5),F(2,3),3),(F(2,3),F(23,30),9),(F(23,30),F(29,30),11),(F(29,30),F(6,5),27),(F(6,5),F(4,3),36),(F(4,3),F(8,5),82),(F(8,5),F(49,30),109),(F(49,30),F(2),385),(F(2),F(8,3),1540),(F(8,3),F(6),54675)]
out={'scope':'Displayed K9 and both rank-ten determinant-54675 equality types containing primitive sqrt(3)E8; all finite clusters in their duals with squared diameter beta<6, density at the guaranteed antipode radius. Does not cover higher-determinant sections or rank-ten sections lacking sqrt(3)E8.','rank10_original_Gram':K10,'rank10_alternative_Gram':K10_alt,'triangular_fiber_anticodes':tri,'intervals':{}}
for name,k,rows in [('K9',9,intervals9),('K10',10,intervals10)]:
 assert all(rows[i][1]==rows[i+1][0] for i in range(len(rows)-1))
 out['intervals'][name]=[]
 for left,right,B in rows:
  rho2=B*B*(1-left/6)**(48-k)
  assert rho2<1,(name,left,right,B,rho2)
  out['intervals'][name].append({'left':str(left),'right':str(right),'cardinality_bound':B,'strict_integer_inequality':f'{B*B*(1-left/6).numerator**(48-k)} < {(1-left/6).denominator**(48-k)}','ratio_upper_squared':str(rho2),'ratio_upper_display_only':float(rho2)**.5})
out['status']='ALL_EXACT_CHECKS_PASS'
Path(__file__).with_name('fixed_section_cluster_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
