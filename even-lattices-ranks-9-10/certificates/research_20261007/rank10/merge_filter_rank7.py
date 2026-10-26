#!/usr/bin/env python3
"""Verify complete rank7 checkpoint coverage and apply exact rank8 lifting prune."""
from pathlib import Path
import hashlib,json
from exact_lattice import determinant
here=Path(__file__).resolve().parent/'early_flags';src=here/'rank7_parents'
summary=json.loads((src/'complete_summary.json').read_text())
for line in (src/'SHA256SUMS.txt').read_text().splitlines():
    h,n=line.split('  ');assert hashlib.sha256((src/n).read_bytes()).hexdigest()==h
parents=json.loads((here/'rank6_fast.json').read_text())['representatives']
pruned6=json.loads((src/'exact_prunes.json').read_text())['prunes']
covered=set(x['parent_index']for x in pruned6);eligible=[];origins=[];pruned7=[];raw=0
for path in sorted(src.glob('parent_*.json')):
    data=json.loads(path.read_text());i=data['parent_index']
    assert i not in covered;covered.add(i)
    assert data['parent_gram']==parents[i] and data['input_sha256']==summary['input_sha256']
    d6=determinant(parents[i]);assert len(data['representatives'])==data['raw_count']
    for j,g in enumerate(data['representatives']):
        assert [row[:6]for row in g[:6]]==parents[i]
        d7=determinant(g);assert 4374<=d7<=13938 and d7%2==0
        raw+=1
        if 3*d7*d7<=4*d6*24673:
            eligible.append(g);origins.append([i,j,d6,d7])
        else:pruned7.append([i,j,d6,d7,3*d7*d7,4*d6*24673])
assert covered==set(range(len(parents))) and raw==summary['raw_rank7_candidates']
(here/'rank7_eligible.json.raw').write_text(json.dumps({'representatives':eligible})+'\n')
(here/'rank7_lifting_prunes.json').write_text(json.dumps({'upper_rank8':24673,'format':['parent_index','child_index','d6','d7','lhs','rhs'],'prunes':pruned7})+'\n')
(here/'rank7_eligible_origins.json').write_text(json.dumps({'format':['parent_index','child_index','d6','d7'],'origins':origins})+'\n')
result={'complete_rank6_parent_coverage':len(covered),'raw_rank7_candidates':raw,'rank8_lifting_pruned':len(pruned7),'eligible_rank7_raw':len(eligible),'rank8_upper':24673,'rank7_isometry_count':'not yet deduplicated'}
(here/'rank7_filter_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(result)
