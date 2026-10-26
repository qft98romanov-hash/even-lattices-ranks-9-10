#!/usr/bin/env python3
"""Exact isometry deduplication with cached pairings and bit-set backtracking.
Reuses exact vector enumeration; every accepted identification has a checked
unimodular integral Gram isometry. Signatures only split, never identify.
"""
from collections import Counter
from pathlib import Path
import json,sys,time
from exact_lattice import determinant,enumerate_vectors

def mv(g,v):return tuple(sum(a*b for a,b in zip(row,v))for row in g)
def dot(u,v):return sum(a*b for a,b in zip(u,v))
def signpos(v):return next((x>0 for x in v if x),False)
def sig(g):
    data=enumerate_vectors(g,6,include_zero=False)
    vv=[v for v,q in data];qv=[int(q)for v,q in data];gv=[mv(g,v)for v in vv]
    local=[]
    for i,v in enumerate(vv):
        hist=Counter((qv[j],dot(v,gv[j]))for j in range(len(vv)))
        local.append((qv[i],tuple(sorted(hist.items()))))
    return (determinant(g),tuple(sorted(Counter(qv).items())),tuple(sorted(Counter(local).items())))

class Target:
    def __init__(self,g,bound):
        self.g=g;self.bound=bound
        data=enumerate_vectors(g,bound,include_zero=False)
        self.vv=[v for v,q in data];self.qv=[int(q)for v,q in data]
        self.norm={};self.pos=0
        for i,(v,q)in enumerate(zip(self.vv,self.qv)):
            self.norm[q]=self.norm.get(q,0)|(1<<i)
            if signpos(v):self.pos|=1<<i
        gv=[mv(g,v)for v in self.vv]
        self.compat=[]
        for v in self.vv:
            co={}
            for j,gg in enumerate(gv):
                p=dot(v,gg);co[p]=co.get(p,0)|(1<<j)
            self.compat.append(co)
    def iso(self,a):
        n=len(a);assigned={}
        def rec():
            if len(assigned)==n:
                X=[[self.vv[assigned[j]][i]for j in range(n)]for i in range(n)]
                assert abs(determinant(X))==1
                assert all(dot(self.vv[assigned[i]],mv(self.g,self.vv[assigned[j]]))==a[i][j]for i in range(n)for j in range(n))
                return X
            best=None
            for k in range(n):
                if k in assigned:continue
                mask=self.norm.get(a[k][k],0)
                for j,index in assigned.items():mask &=self.compat[index].get(a[k][j],0)
                if not assigned:mask &=self.pos
                count=mask.bit_count()
                if not count:return None
                if best is None or count<best[0]:best=(count,k,mask)
            _,k,mask=best
            while mask:
                bit=mask & -mask;mask-=bit
                assigned[k]=bit.bit_length()-1
                out=rec()
                if out is not None:return out
                del assigned[k]
            return None
        return rec()

def main():
    source=Path(sys.argv[1]);target=Path(sys.argv[2]);input_data=json.loads(source.read_text());forms=input_data['representatives']
    reps=[];groups={};targets={};classes=[];maps=[];start=time.monotonic()
    for index,g in enumerate(forms):
        key=sig(g);found=None;U=None
        bound=max(g[i][i]for i in range(len(g)))
        for j in groups.get(key,[]):
            ck=(j,bound)
            if ck not in targets:targets[ck]=Target(reps[j],bound)
            U=targets[ck].iso(g)
            if U is not None:found=j;break
        if found is None:
            found=len(reps);reps.append(g);groups.setdefault(key,[]).append(found)
            U=[[int(i==j)for j in range(len(g))]for i in range(len(g))]
        classes.append(found);maps.append(U)
        if index%1000==0:print('PROGRESS',index,'CLASSES',len(reps),'SECONDS',round(time.monotonic()-start,2),flush=True)
    payload={'rank':len(reps[0]) if reps else input_data.get('rank'),'raw_count':len(forms),'class_count':len(reps),'representatives':reps,'raw_to_class':classes,'isometry_maps':maps,'deduplication':'exact finite basis-imaging with bit masks'}
    target.write_text(json.dumps(payload)+'\n')
    print('COMPLETE',len(forms),len(reps),'SECONDS',round(time.monotonic()-start,2),flush=True)
if __name__=='__main__':main()
