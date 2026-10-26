exec(open(__file__.replace('e8_orbit.py','explore.py')).read().split('D=21870')[0])
from collections import deque
G=[r[:8] for r in K9[:8]];C=[[x//3 for x in r]for r in G]
d,adj,fp,mu,wit,pc=e.discriminant_data(G,F(8,3))
p0=tuple(r[8] for r in K9[:8]);c0=fp(p0)
assert mu[c0]==F(8,3)
# Basis reflections are integral parent isometries.
def mm(a,b):return [[sum(a[i][k]*b[k][j]for k in range(len(b)))for j in range(len(b[0]))]for i in range(len(a))]
def tr(a):return list(map(list,zip(*a)))
R=[]
for k in range(8):
 r=[[int(i==j)-(C[k][j]if i==k else 0)for j in range(8)]for i in range(8)]
 assert mm(mm(tr(r),G),r)==G and determinant(r)==-1
 R.append(r)
seen={c0:0};queue=deque([c0]);tree=[{'class':c0,'witness':p0,'parent':None,'generator':None}]
while queue:
 c=queue.popleft();p=wit[c]
 for k in range(8):
  pp=tuple(p[j]-p[k]*C[k][j]for j in range(8));cc=fp(pp)
  assert mu[cc]==mu[c]
  if cc not in seen:
   seen[cc]=len(tree);tree.append({'class':cc,'witness':wit[cc],'parent':seen[c],'generator':k});queue.append(cc)
deep={c for c,q in mu.items()if q==F(8,3)}
assert set(seen)==deep and len(deep)==1920
Path(__file__).with_name('e8_orbit_certificate.json').write_text(json.dumps({'gram':G,'generators':R,'tree':tree,'root_cross':p0,'class_count':1920},indent=2))
print('E8_DEEP_CLASSES_1920_SINGLE_CERTIFIED_REFLECTION_ORBIT')
