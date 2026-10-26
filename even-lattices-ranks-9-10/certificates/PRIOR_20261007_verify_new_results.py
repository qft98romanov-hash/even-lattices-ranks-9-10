#!/usr/bin/env python3
"""Run completed new checks; does not assert all original problems solved."""
from pathlib import Path
import subprocess,sys,argparse
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--full-equality',action='store_true')
parser.add_argument('--full-local-extensions',action='store_true',
 help='Replay all 281 ambient fibers; takes several minutes.')
parser.add_argument('--full-global',action='store_true',
 help='Regenerate all 1897 parent lists of the global rank-ten proof.')
parser.add_argument('--workers',type=int,default=7)
a=parser.parse_args()
if not __debug__:
 raise SystemExit('Assertions must be enabled; do not use -O or -OO.')
base=root/'research_20261007'
jobs=[
 ('independent_review/check_k9_perfect.py',[]),
 ('independent_review/check_equality_independent.py',[]),
 ('equality/rank9_gap.py',[]),
 ('rank10/verify_rank10_e8_classification.py',[]),
 ('independent_review/check_rank10_global_chain.py',[]),
 ('rank10/verify_rank9_low_spectrum.py',[]),
 ('independent_review/check_rank9_low_orbits.py',[]),
 ('rank10_theory/verify_rank10_bounds.py',[]),
 ('clusters/verify_fixed_section_cluster_optimality.py',[]),
 ('clusters/verify_all_E8_rank9_cluster_optimality.py',[]),
 ('clusters/verify_rank10_single_projection.py',[]),
 ('independent_review/check_all_e8_rank9_clusters.py',[]),
 ('embeddings/verify_ambient_embeddings.py',['--json']),
 ('embeddings/verify_A10_extension_exact.py',[]),
 ('embeddings/verify_A10_extension_exact.py',['--control']),
 ('independent_review/check_fixed_k9_extension_coverage.py',[]),
]
if a.full_equality:jobs.append(('equality/verify_equality.py',[]))
if a.full_local_extensions:
 jobs.append(('embeddings/verify_all_fixed_K9_extensions.py',[]))
if a.full_global:
 jobs.append(('rank10/verify_global_rank10_certificate.py',
  ['--replay','--workers',str(a.workers)]))
logs=root/'local_replay_logs';logs.mkdir(exist_ok=True)
for i,(rel,args) in enumerate(jobs):
 path=base/rel
 suffix='_control' if '--control' in args else '_replay' if '--replay' in args else ''
 log=logs/(f'{i+1:02d}_'+path.stem+suffix+'.log')
 print('RUN',rel,*args,flush=True)
 with log.open('w') as f:
  r=subprocess.run([sys.executable,str(path),*args],cwd=root,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:
  raise SystemExit(f'FAILED {rel}: see {log}; exit={r.returncode}')
 print('PASS',rel,flush=True)
print('ALL_SELECTED_NEW_RESULT_CHECKS_PASS')
print('This is not a proof that the unresolved global problems are solved.')
