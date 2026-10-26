#!/usr/bin/env python3
"""Independent exact extraction and certification of printed ambient embeddings.
Uses only Python's standard library. No short-vector-shell enumeration assumed.
"""
import re,json,hashlib,time,sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent.parent/'source_extracted.txt'

def tr(A):return [list(a) for a in zip(*A)]
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def eye(n):return [[int(i==j) for j in range(n)]for i in range(n)]
def det(A):
    A=[r[:]for r in A];n=len(A);d=1;sign=1
    for k in range(n-1):
        if not A[k][k]:
            j=next((j for j in range(k+1,n) if A[j][k]),None)
            if j is None:return 0
            A[k],A[j]=A[j],A[k];sign=-sign
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                t=A[i][j]*p-A[i][k]*A[k][j]
                assert t%d==0
                A[i][j]=t//d
            A[i][k]=0
        d=p
    return sign*A[-1][-1]
def inv(A):
    n=len(A);M=[[Fraction(x)for x in row]+[Fraction(i==j)for j in range(n)]for i,row in enumerate(A)]
    for j in range(n):
        i=next(i for i in range(j,n)if M[i][j]);M[j],M[i]=M[i],M[j]
        p=M[j][j];M[j]=[x/p for x in M[j]]
        for i in range(n):
            if i!=j:
                p=M[i][j];M[i]=[a-p*b for a,b in zip(M[i],M[j])]
    out=[r[n:]for r in M];assert mm(A,out)==eye(n);return out

def ldlt(A):
    n=len(A);L=[[Fraction(i==j)for j in range(n)]for i in range(n)];D=[]
    for j in range(n):
        D.append(Fraction(A[j][j])-sum(L[j][k]**2*D[k]for k in range(j)))
        assert D[-1]>0,('not SPD',j,D[-1])
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*D[k]for k in range(j)))/D[j]
    assert mm(mm(L,[[D[i]if i==j else 0 for j in range(n)]for i in range(n)]),tr(L))==A
    return D

def snf(A):
    """Return D,U,V with D=U*A*V, diagonal positive divisibility SNF.
    Only swaps, row/col addition, and sign changes are used, so U,V unimodular.
    Equality and determinants are checked independently at return.
    """
    A0=[r[:]for r in A];A=[r[:]for r in A];m=len(A);n=len(A[0]);U=eye(m);V=eye(n)
    def sr(i,j):A[i],A[j]=A[j],A[i];U[i],U[j]=U[j],U[i]
    def sc(i,j):
        for Z in (A,V):
            for row in Z:row[i],row[j]=row[j],row[i]
    def ar(i,j,q):
        for Z in (A,U):Z[i]=[a+q*b for a,b in zip(Z[i],Z[j])]
    def ac(i,j,q):
        for Z in (A,V):
            for row in Z:row[i]+=q*row[j]
    for k in range(min(m,n)):
        nz=[(abs(A[i][j]),i,j)for i in range(k,m)for j in range(k,n)if A[i][j]]
        if not nz:break
        _,i,j=min(nz);sr(k,i);sc(k,j)
        while True:
            for i in range(k+1,m):
                if A[i][k]:
                    q=A[i][k]//A[k][k];ar(i,k,-q)
                    if A[i][k]:sr(i,k)
                    break
            else:
                for j in range(k+1,n):
                    if A[k][j]:
                        q=A[k][j]//A[k][k];ac(j,k,-q)
                        if A[k][j]:sc(j,k)
                        break
                else:
                    bad=next(((i,j)for i in range(k+1,m)for j in range(k+1,n)if A[i][j]%A[k][k]),None)
                    if bad is None:break
                    ar(k,bad[0],1)
            assert A[k][k]
        if A[k][k]<0:ar(k,k,-2)
    assert mm(mm(U,A0),V)==A
    assert abs(det(U))==abs(det(V))==1
    assert all(A[i][j]==0 for i in range(m)for j in range(n)if i!=j)
    ds=[A[i][i]for i in range(min(m,n))]
    assert all(not a or b%a==0 for a,b in zip(ds,ds[1:]))
    return A,U,V

def extract(s,label):
    block=s[s.index(label):]
    block=block[block.index('[['):block.index(']]')+2]
    rows=[list(map(int,row.split()))for row in re.findall(r'\[([-\d\s]+)\]',block)]
    assert all(len(r)==48 for r in rows),(label,list(map(len,rows)))
    return rows

def main():
    if '--json' in sys.argv:
        matrices=json.loads((ROOT/'printed_matrices.json').read_text())
        Gp=matrices['P48p_G'];Gm=matrices['P48m_G'];T8=matrices['P48p_T8'];T9=matrices['P48p_T9'];T10=matrices['P48p_T10'];T5=matrices['P48m_T5'];T3=matrices['P48m_T3'];W5=matrices['P48m_W5'];W3=matrices['P48m_W3']
        source_hash=None
    else:
        s=SOURCE.read_text();S=s[s.index('A      Certificates'):]
        Gp=extract(S,'(the Gram matrix of P48p )')
        Gm=extract(S,'(the Gram matrix of P48m )')
        T8=extract(S,'(8 × 48)');T9=extract(S,'(9 × 48)');T10=extract(S,'(10 × 48)')
        T5=extract(S,'(5 × 48)');T3=extract(S,'(3 × 48)')
        W5=extract(S,'(6 × 48)');W3=extract(S,'(4 × 48)')
        matrices={'P48p_G':Gp,'P48m_G':Gm,'P48p_T8':T8,'P48p_T9':T9,'P48p_T10':T10,'P48m_T5':T5,'P48m_T3':T3,'P48m_W5':W5,'P48m_W3':W3}
        source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    (ROOT/'printed_matrices.json').write_text(json.dumps(matrices,indent=2)+'\n')
    K8=mm(mm(T8,Gp),tr(T8));U8=mm(mm(mm(T9[:8],Gp),tr(T8)),inv(K8));assert all(x.denominator==1 for row in U8 for x in row);U8=[[int(x)for x in row]for row in U8];assert abs(det(U8))==1 and mm(U8,T8)==T9[:8];assert T10[:9]==T9
    report={'E8_basis_transition_T9_prefix_from_T8':U8,'source_sha256':source_hash,'ambients':{},'embeddings':{},'limitations':['Ambient minima 6 and identification with named lattices not independently re-enumerated.','No exhaustive classification of ambient automorphism orbits performed.','Other ambients P48q and P48n not available in the supplied printed data.']}
    for name,G in [('P48p',Gp),('P48m',Gm)]:
        assert len(G)==48 and G==tr(G)
        assert all(G[i][i]%2==0 for i in range(48))
        ds=ldlt(G);dg=det(G);assert dg==1
        report['ambients'][name]={'rank':48,'determinant':dg,'positive_ldl_pivots':[str(x)for x in ds],'symmetric_even_unimodular':True}
        print(name,'ambient EXACT PASS',flush=True)
    for name,G,T,expected in [('P48p_K8',Gp,T8,6561),('P48p_K9',Gp,T9,21870),('P48p_K10',Gp,T10,54675),('P48m_K5',Gm,T5,3072),('P48m_K3',Gm,T3,128)]:
        k=len(T);K=mm(mm(T,G),tr(T));dk=det(K)
        assert dk==expected,(name,dk,expected)
        St,Ut,Vt=snf(T);assert [St[i][i]for i in range(k)]==[1]*k
        Sk,Uk,Vk=snf(K)
        A=mm(T,G);Sa,Ua,Va=snf(A);assert [Sa[i][i]for i in range(k)]==[1]*k
        B=tr([r[k:]for r in Va])
        assert mm(A,tr(B))==[[0]*(48-k)for _ in range(k)]
        C=mm(mm(B,G),tr(B));dc=det(C);assert dc==dk
        combined=T+B;idx=abs(det(combined));assert idx==dk
        disc=[Sk[i][i]for i in range(k)if Sk[i][i]>1]
        # Explicit lift of each dual basis vector and exact anti-isometry.
        Q=mm([r[:k]for r in Va],Ua);assert mm(A,Q)==eye(k)
        Ki=inv(K);Adj=[[int(x*dk)for x in row]for row in Ki];assert mm(K,Adj)==[[dk*int(i==j)for j in range(k)]for i in range(k)]
        proj=mm(tr(T),Adj);N=[[dk*q-p for q,p in zip(qr,pr)]for qr,pr in zip(Q,proj)]
        assert mm(A,N)==[[0]*k for _ in range(k)]
        pair=mm(mm(B,G),N);assert all(x%dk==0 for row in pair for x in row)
        H=mm(mm(tr(Q),G),Q);assert all(H[i][i]%2==0 for i in range(k))
        lhs=mm(mm(tr(N),G),N);assert lhs==[[dk*dk*H[i][j]-dk*Adj[i][j]for j in range(k)]for i in range(k)]
        report['embeddings'][name]={'rank':k,'gram':K,'determinant':dk,'primitive':True,'smith_T':[St[i][i]for i in range(k)],'discriminant_group_invariants':disc,'complement_rank':48-k,'complement_determinant':dc,'complement_norm6_witness':next((B[i]for i in range(48-k)if C[i][i]==6),None),'direct_sum_index_in_ambient':idx,'complement_basis_B':B,'complement_gram':C,'kernel_smith_U':Ua,'kernel_smith_V':Va,'kernel_smith_diagonal':[Sa[i][i]for i in range(k)],'glue_lifts_Q':Q,'glue_complement_generators_numerator':N,'glue_complement_generators_denominator':dk,'dual_gram_K_inverse':[[str(x)for x in r]for r in Ki],'glue_pairing_gram_H':H,'exact_discriminant_anti_isometry':True}
        (ROOT/'ambient_embedding_certificates.json').write_text(json.dumps(report,indent=2)+'\n')
        print(name,'EXACT PASS det',dk,'disc',disc,'complement_rank',48-k,flush=True)
        if name.endswith('K5') or name.endswith('K3'):
            W=W5 if name.endswith('K5')else W3
            pairing=mm(mm(W,G),tr(T));assert pairing==[[0]*k]+eye(k)
            report['embeddings'][name]['cluster_lifts_pairing_identity']=True
    (ROOT/'ambient_embedding_certificates.json').write_text(json.dumps(report,indent=2)+'\n')
    print('ALL_PRINTED_EMBEDDING_CERTIFICATES_PASS',flush=True)
if __name__=='__main__':main()
