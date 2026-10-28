#!/usr/bin/env python3
"""Rebuild and replay the original C++ ambient search with UBSan enabled.

Requires GCC/Clang with __int128 and undefined-behavior sanitizer support.
The fresh output is compared with every archived count and witness.
"""
from pathlib import Path
import subprocess, hashlib, json, time, platform, argparse, shutil
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SRC=ROOT/'even-lattices-ranks-9-10/certificates/research_20261007/embeddings'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cxx', default='g++')
parser.add_argument('--output', type=Path)
args=parser.parse_args()
if shutil.which(args.cxx) is None:
 parser.error('Requested C++ compiler is not available; no verification was performed.')
if not (SRC/'search_all_fixed_K9_extensions.cpp').is_file():
 parser.error('The complete repository checkout is required.')
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
OUT=args.output.resolve() if args.output else HERE/'runs'/stamp/'ambient_cpp'
if OUT.exists() and any(OUT.iterdir()):
 parser.error('Output directory must be new or empty; archived reports are never overwritten.')
OUT.mkdir(parents=True,exist_ok=True)
EXE=OUT/'ambient_ubsan'
source=SRC/'search_all_fixed_K9_extensions.cpp'
inputs=SRC/'all_fixed_K9_extension_inputs.txt'
compile_cmd=[args.cxx,'-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=undefined',str(source),'-o',str(EXE)]
record={'status':'RUNNING','started_utc':datetime.now(timezone.utc).isoformat(),'compile_command':compile_cmd,
 'compiler':subprocess.check_output([args.cxx,'--version'],text=True).splitlines()[0],
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'input_sha256':hashlib.sha256(inputs.read_bytes()).hexdigest(),
 'scope':'Fresh sanitized execution of the original C++ integer ambient-fiber enumerator; not a new implementation.'}
(OUT/'cpp_execution.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.monotonic()
compiled=subprocess.run(compile_cmd,capture_output=True,text=True)
(OUT/'cpp_compile.log').write_text(compiled.stdout+compiled.stderr)
record['compile_exit_code']=compiled.returncode
if compiled.returncode:
 record['status']='FAIL_COMPILE'
else:
 with inputs.open() as f,(OUT/'cpp_console.log').open('w') as log,(OUT/'cpp_stderr.log').open('w') as err:
  result=subprocess.run([str(EXE)],stdin=f,stdout=log,stderr=err)
 record['exit_code']=result.returncode
 def parse(p):
  cases={};witnesses={};completed=None
  for line in p.read_text().splitlines():
   v=line.split()
   if not v:continue
   if v[0]=='CASE':cases[int(v[1])]=tuple(map(int,[v[3],v[5],v[7]]))
   elif v[0]=='EXACT_NORM6_WITNESS':witnesses.setdefault(int(v[1]),[]).append(tuple(map(int,v[2:])))
   elif v[0]=='ALL_FIXED_K9_FIBERS_COMPLETED':completed=int(v[1])
  return cases,{k:sorted(v)for k,v in witnesses.items()},completed
 fresh=parse(OUT/'cpp_console.log');old=parse(SRC/'search_all_fixed_K9_extensions.log')
 record['matches_archived_counts_and_witnesses']=fresh==old
 record['cases']=len(fresh[0]);record['nodes']=sum(v[0]for v in fresh[0].values())
 record['leaves']=sum(v[1]for v in fresh[0].values());record['witnesses']=sum(v[2]for v in fresh[0].values())
 record['stderr_bytes']=(OUT/'cpp_stderr.log').stat().st_size
 record['status']='PASS'if result.returncode==0 and fresh==old and fresh[2]==281 and record['stderr_bytes']==0 else 'FAIL'
record.update(elapsed_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat())
(OUT/'cpp_execution.json').write_text(json.dumps(record,indent=2)+'\n')
if EXE.exists():
 EXE.unlink()
print(json.dumps(record,indent=2),flush=True)
raise SystemExit(0 if record['status']=='PASS'else 1)
