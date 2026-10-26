#!/usr/bin/env python3
"""Replay the assembled exact certificates with Python's standard library.

The historic --full-equality flag refers to rank-nine boundary equality.
Use --replay-rank10-equality for the later global rank-ten classification.
"""
from pathlib import Path
import subprocess,sys,argparse
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--full-equality',action='store_true',
 help='Regenerate the older rank-nine equality-boundary certificate.')
parser.add_argument('--full-local-extensions',action='store_true',
 help='Replay all 281 ambient fibers; takes several minutes.')
parser.add_argument('--full-global',action='store_true',
 help='Regenerate all 1897 parent lists of the global rank-ten proof.')
parser.add_argument('--replay-rank10-equality',action='store_true',
 help='Regenerate all additional endpoint jobs for global rank-ten equality.')
parser.add_argument('--workers',type=int,default=7)
a=parser.parse_args()
if not __debug__:
 raise SystemExit('Assertions must be enabled; do not use -O or -OO.')
if a.workers < 1:
 parser.error('--workers must be at least 1')
old_jobs=[
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
if a.full_equality:old_jobs.append(('equality/verify_equality.py',[]))
if a.full_local_extensions:
 old_jobs.append(('embeddings/verify_all_fixed_K9_extensions.py',[]))
if a.full_global:
 old_jobs.append(('rank10/verify_global_rank10_certificate.py',
  ['--replay','--workers',str(a.workers)]))
jobs=[('research_20261007/'+rel,args) for rel,args in old_jobs]
equality_args=['--skip-base']
if a.replay_rank10_equality:
 equality_args += ['--replay','--workers',str(a.workers)]
jobs += [
 ('research_20261008/rank10_equality/verify_equality_certificate.py',equality_args),
 ('research_20261008/independent_review/check_equality_windows_and_recovered_prunes.py',[]),
 ('research_20261008/independent_review/check_boundaries_by_quadratic_module.py',[]),
 ('research_20261008/independent_review/check_delta_chain_independent.py',[]),
 ('research_20261008/consequences/audit_two_types_and_cluster_gap.py',[]),
]
logs=root/'local_replay_logs';logs.mkdir(exist_ok=True)
for i,(rel,args) in enumerate(jobs):
 path=root/rel
 suffix='_control' if '--control' in args else '_replay' if '--replay' in args else ''
 log=logs/(f'{i+1:02d}_'+path.stem+suffix+'.log')
 print('RUN',rel,*args,flush=True)
 with log.open('w') as f:
  r=subprocess.run([sys.executable,str(path),*args],cwd=root,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:
  raise SystemExit(f'FAILED {rel}: see {log}; exit={r.returncode}')
 print('PASS',rel,flush=True)
print('ALL_SELECTED_NEW_RESULT_CHECKS_PASS')
print('Read README_EN.txt or README_RU.txt for the precise scope of each result.')
