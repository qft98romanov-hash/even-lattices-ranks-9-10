exec(open(__file__.replace('boundary8.py','explore.py')).read().split('D=21870')[0])
from extend_flag import extend_parent
rows=json.loads((BASE/'rank7_survivor_linkage_exact.json').read_text())['groups'];out=[]
for row in rows:
 t=time.time();g=row['target_gram'];label=row['label']
 children,stats=extend_parent(g,15909,15909,4,{0,1})
 out.append({'label':label,'gram':g,'children':children,'stats':stats})
 print('PARENT',label,'children',len(children),'time',time.time()-t,flush=True)
 Path(__file__).with_name('boundary8_results.json').write_text(json.dumps(out,indent=2))
assert all(not x['children'] for x in out)
print('RANK8_BOUNDARY_15909_EMPTY')
