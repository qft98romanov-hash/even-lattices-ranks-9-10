exec(open(__file__.replace('identify.py','explore.py')).read().split('D=21870')[0])
rows=json.loads(Path(__file__).with_name('equality_candidates.json').read_text())
res=[]
for r in rows:
 cand=r['candidates'][:1] if r['name']=='E8' else r['candidates']
 for i,c in enumerate(cand):
  C=c['gram'];t=time.time()
  pts=enumerate_vectors(C,6,include_zero=False)
  print('testing',r['name'],i,'min',min(q for v,q in pts),'kissing',len(pts),flush=True)
  U=isometry(C,K9)
  print('iso?',U is not None,'seconds',time.time()-t,flush=True)
  res.append({'parent':r['name'],'index':i,'gram':C,'to_K9':U,'kissing':len(pts)})
  Path(__file__).with_name('equality_isometries.json').write_text(json.dumps(res,indent=2))
