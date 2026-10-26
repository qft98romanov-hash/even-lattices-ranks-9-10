from fractions import Fraction as F
import json
from pathlib import Path
# Exact floor of rational pth root.
def floor_root(q,p):
    lo=0;hi=1
    while F(hi**p)<=q:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if F(mid**p)<=q:lo=mid
        else:hi=mid
    assert F(lo**p)<=q<F((lo+1)**p)
    return lo
U={10:54672};rows=[]
# gamma10<=2^(9/8): d9^40<=2^45*d10^36.
raw=floor_root(F(2**45*U[10]**36),40);U[9]=raw-raw%2
rows.append({'rank':9,'raw':raw,'upper':U[9],'power':40,'rhs':str(2**45*U[10]**36)})
# gamma9=2 external result for this set of windows.
gpowers={9:F(512),8:F(256),7:F(64),6:F(64,3),5:F(8),4:F(4),3:F(2),2:F(4,3)}
for n in range(9,1,-1):
    rhs=gpowers[n]*U[n]**(n-1)
    raw=floor_root(rhs,n)
    r=n-1;v=raw
    if r%2:residues={0};mod=2
    else:residues={0,(-1)**(r//2)%4};mod=4
    while v%mod not in residues:v-=1
    U[r]=v
    rows.append({'rank':r,'raw':raw,'upper':v,'power':n,'rhs':str(rhs)})
payload={'top_upper':54672,'external_input':'gamma9=2, gamma10<=gamma9^(9/8)','windows':rows}
Path(__file__).with_name('rank10_windows.json').write_text(json.dumps(payload,indent=2)+'\n')
for row in rows:print(row['rank'],row['raw'],row['upper'])
print('EXACT_WINDOWS_OK')
