#!/usr/bin/env python3
"""Build exact integer enclosing ellipsoid for the specified A10 extension fiber."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from verify_ambient_embeddings import mm,tr,inv,det
ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'A10_integer_fiber_basis.json').read_text());m=json.loads((ROOT/'printed_matrices.json').read_text());B=j['B'];w0=j['w0'];G=m['P48p_G'];T=m['P48p_T9'];A=mm(T,G);K=mm(A,tr(T));target=[-K[i][-1]for i in range(8)]+[-1];prefix='A10_exact_cvp';control='--control' in sys.argv
if control:
    cert=json.loads((ROOT/'ambient_embedding_certificates.json').read_text())['embeddings']['P48p_K9'];Q=cert['glue_lifts_Q'];target=[r[0]for r in mm(A,[[x]for x in m['P48p_T10'][-1]])];w0=[r[0]for r in mm(Q,[[x]for x in target])];prefix='K10_control_exact_cvp'
assert mm(A,[[x]for x in w0])==[[x]for x in target]
assert mm(A,tr(B))==[[0]*39 for _ in range(9)]
C=mm(mm(B,G),tr(B));assert det(C)==det(K)==21870
n=len(C);g=mm(mm(B,G),[[x]for x in w0]);g=[r[0]for r in g];wn=mm(mm([w0],G),[[x]for x in w0])[0][0];Ci=inv(C);coeff=[-sum(Ci[i][k]*g[k]for k in range(n))for i in range(n)]
L=[[F(i==k)for k in range(n)]for i in range(n)];D=[]
for i in range(n):
 D.append(F(C[i][i])-sum(L[i][k]**2*D[k]for k in range(i)));assert D[-1]>0
 for h in range(i+1,n):L[h][i]=(C[h][i]-sum(L[h][k]*L[i][k]*D[k]for k in range(i)))/D[i]
y=[sum(coeff[k]*L[k][i]for k in range(i,n))for i in range(n)]
residual=F(wn)-sum(F(g[i])*Ci[i][k]*g[k]for i in range(n)for k in range(n));assert residual==F(7,2),residual
bound=[]
for i in range(n):
 b=0
 while b<abs(coeff[i]) or (F(b)-abs(coeff[i]))**2<F(5,2)*Ci[i][i]:b+=1
 bound.append(b)
S=1<<24
def roundint(q):return (q+F(1,2)).numerator//(q+F(1,2)).denominator
lr=[[roundint(v*S)for v in row]for row in L];yr=[roundint(v*S)for v in y];df=[(d*S).numerator//(d*S).denominator for d in D];E=[(2+sum(bound[i+1:]))//2 for i in range(n)]
for i in range(n):
 assert 0<F(df[i],S)<=D[i]
 assert abs(F(yr[i],S)-y[i])<=F(1,2*S)
 assert F(E[i],S)>=F(1+sum(bound[i+1:]),2*S)
 for h in range(n):assert abs(F(lr[h][i],S)-L[h][i])<=F(1,2*S)
assert F(5,2)*S**3/min(df)<2**64
out={'target_pairings':target,'is_control':control,'rank':n,'scale':S,'basis_B':B,'lift_w0':w0,'gram_C':C,'linear_g':g,'constant_norm':wn,'projection_norm':str(residual),'residual_bound':'5/2','coefficient_bounds':bound,'round_L':lr,'round_y':yr,'lower_D_scaled':df,'center_error_scaled':E,'exact_D':[str(d)for d in D],'exact_L':[[str(x)for x in row]for row in L],'exact_y':[str(x)for x in y],'exact_coefficients':[str(x)for x in coeff],'exact_inverse_diagonal':[str(Ci[i][i])for i in range(n)]}
(ROOT/(prefix+'_input.json')).write_text(json.dumps(out,indent=2)+'\n')
with (ROOT/(prefix+'_input.txt')).open('w')as f:
 print(n,S,wn,file=f)
 for row in[df,yr,E,bound,g]:print(*row,file=f)
 for row in lr:print(*row,file=f)
 for row in C:print(*row,file=f)
print('EXACT_CVP_INPUT_PASS','rank',n,'max_coordinate_bound',max(bound),'max_center_error',max(E),'/ 2^24','projection_norm',residual)
