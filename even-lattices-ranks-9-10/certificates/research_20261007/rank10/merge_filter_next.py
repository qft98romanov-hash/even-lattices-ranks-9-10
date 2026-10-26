#!/usr/bin/env python3
"""Verify complete checkpoint coverage; prune for the following flag step."""
from pathlib import Path
import argparse,hashlib,json
from exact_lattice import determinant
P=argparse.ArgumentParser();P.add_argument('--rank',type=int,required=True);P.add_argument('--input',type=Path,required=True);P.add_argument('--next-high',type=int,required=True);A=P.parse_args()
here=Path(__file__).resolve().parent/'early_flags';src=here/f'rank{A.rank}_parents'
summary=json.loads((src/'complete_summary.json').read_text())
for line in (src/'SHA256SUMS.txt').read_text().splitlines():
    h,n=line.split('  ');assert hashlib.sha256((src/n).read_bytes()).hexdigest()==h
parents=json.loads(A.input.read_text())['representatives']
assert hashlib.sha256(A.input.read_bytes()).hexdigest()==summary['input_sha256']
pruned_parent=json.loads((src/'exact_prunes.json').read_text())['prunes']
covered=set(x['parent_index']for x in pruned_parent);eligible=[];origins=[];pruned=[];raw=0
for path in sorted(src.glob('parent_*.json')):
    data=json.loads(path.read_text());i=data['parent_index']
    assert i not in covered;covered.add(i)
    assert data['parent_gram']==parents[i] and data['input_sha256']==summary['input_sha256']
    dp=determinant(parents[i]);assert len(data['representatives'])==data['raw_count']
    for j,g in enumerate(data['representatives']):
        assert [row[:A.rank-1]for row in g[:A.rank-1]]==parents[i]
        d=determinant(g);assert data['window'][0]<=d<=data['window'][1] and d%data['modulus']in data['residues']
        raw+=1
        if 3*d*d<=4*dp*A.next_high:
            eligible.append(g);origins.append([i,j,dp,d])
        else:pruned.append([i,j,dp,d,3*d*d,4*dp*A.next_high])
assert covered==set(range(len(parents))) and raw==summary['raw_candidates']
(here/f'rank{A.rank}_eligible.json.raw').write_text(json.dumps({'representatives':eligible})+'\n')
(here/f'rank{A.rank}_lifting_prunes.json').write_text(json.dumps({'next_upper':A.next_high,'prunes':pruned})+'\n')
(here/f'rank{A.rank}_eligible_origins.json').write_text(json.dumps({'origins':origins})+'\n')
result={'rank':A.rank,'complete_parent_coverage':len(covered),'raw_candidates':raw,'next_lifting_pruned':len(pruned),'eligible_raw':len(eligible),'next_upper':A.next_high,'eligible_isometry_classes':'not yet deduplicated','all_isometry_count':'NOT DETERMINED; some safely pruned before deduplication'}
(here/f'rank{A.rank}_filter_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(result)
