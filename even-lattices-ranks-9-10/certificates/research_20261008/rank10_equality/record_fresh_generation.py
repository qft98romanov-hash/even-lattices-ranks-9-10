#!/usr/bin/env python3
"""Archive actual fresh-production evidence separately from optional reruns."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent

def read(p):return json.loads(Path(p).read_text())
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 checked=read(R/'equality_certificate_verified.json');assert checked['status'].startswith('PASS_')
 names=['rank6_boundary','rank7_boundary','rank7_from_new6','rank8_boundary','rank8_from_new7','rank9_boundary','rank9_from_new8']
 rows=[]
 for name in names:
  x=read(R/(name+'.json'));jobs=[R/'jobs'/f'{name}_{i:04d}.json'for i in range(x['parent_count'])]
  assert all(p.exists()for p in jobs)
  rows.append({'name':name,'parents':x['parent_count'],'raw':x['raw_count'],'wall_seconds':x['seconds'],'data_sha256':digest(R/(name+'.json')),'jobs_sha256':{p.name:digest(p)for p in jobs}})
 assert sum(x['parents']for x in rows)==5010 and sum(x['raw']for x in rows)==78
 report={'status':'PASS_FRESH_EXACT_BOUNDARY_GENERATION','generation_date_UTC':'2026-10-07','statement':'All 5010 extension jobs were generated afresh in the newly created research_20261008/rank10_equality/jobs directory; no old equality jobs existed. This records initial actual generation, not a separate --replay execution.','parent_window_jobs':5010,'boundary_pairs_excluding_58_immediate_prunes':4952,'raw_children':78,'terminal_non_E8_survivors':0,'separate_replay_run':False,'generations':rows,'static_verifier_result_sha256':digest(R/'equality_certificate_verified.json'),'source_hashes':{p.name:digest(p)for p in[R/'run_delta.py',R/'process_delta.py',R/'verify_equality_certificate.py']},'generation_logs':{name:digest(R/name)for name in['run_delta_initial.log','run_delta_r8.log','run_delta_r9.log']}}
 (R/'equality_fresh_generation_record.json').write_text(json.dumps(report,indent=2)+'\n')
 print(report['status'],'jobs',5010,'raw',78,'survivors',0)
if __name__=='__main__':main()
