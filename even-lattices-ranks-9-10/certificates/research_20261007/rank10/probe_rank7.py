from pathlib import Path
import json,time
from extend_flag import extend_parent
here=Path(__file__).parent/'early_flags'
p=json.loads((here/'rank6_fast.json').read_text())['representatives']
a=json.loads((here/'rank7_active_parents.json').read_text())['active']
selected=[a[0],a[len(a)//2],a[-1]]
records=[]
for i,d,d5 in selected:
    start=time.monotonic();print('START',i,d,d5,flush=True)
    children,stats=extend_parent(p[i],4374,13938,2,{0})
    elapsed=time.monotonic()-start
    rec={'parent_index':i,'parent_det':d,'rank5_det':d5,'seconds':elapsed,'raw_children':len(children),'stats':stats}
    records.append(rec)
    (here/f'rank7_probe_parent_{i}.json').write_text(json.dumps({'representatives':children,'statistics':rec})+'\n')
    (here/'rank7_probe_summary.json').write_text(json.dumps(records,indent=2)+'\n')
    print('FINISH',rec,flush=True)
