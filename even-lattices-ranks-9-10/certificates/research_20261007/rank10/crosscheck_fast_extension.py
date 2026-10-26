from pathlib import Path
import json,time,hashlib
from fast_extend import extend_parent
root=Path(__file__).parent/'early_flags'/'rank8_parents'
files=sorted(root.glob('parent_*.json'))
positive=[p for p in files if json.loads(p.read_text())['raw_count']]
zero=[p for p in files if not json.loads(p.read_text())['raw_count']]
chosen=positive[:3]+zero[:3]
records=[]
for p in chosen:
 d=json.loads(p.read_text());start=time.monotonic()
 children,stats=extend_parent(d['parent_gram'],6564,24673,4,{0,1})
 assert children==d['representatives'],p
 records.append({'parent':d['parent_index'],'raw_count':len(children),'original_seconds':d['seconds'],'fast_seconds':time.monotonic()-start,'exact_ordered_children_equal':True})
 print(records[-1],flush=True)
Path(__file__).with_name('fast_extension_crosscheck.json').write_text(json.dumps(records,indent=2)+'\n')
print('EXACT_FAST_EXTENSION_CROSSCHECK_PASS',len(records),flush=True)
