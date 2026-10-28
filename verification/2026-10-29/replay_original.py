#!/usr/bin/env python3
"""Replay every supported original verification mode and preserve fresh logs.

Requires the complete repository checkout and Python with assertions enabled.
Run on Linux/macOS/WSL; the original full regenerations use fork.
This repeats the existing algorithms, not an independent reimplementation.
"""
from pathlib import Path
from datetime import datetime, timezone
import subprocess, sys, os, json, time, shutil, hashlib, platform, argparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT / 'even-lattices-ranks-9-10'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workers', type=int, default=3)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
if not __debug__:
    parser.error('Assertions must be enabled; do not use -O or -OO.')
if args.workers < 1:
    parser.error('--workers must be positive')
if os.name == 'nt':
    parser.error('Run full regenerations on Linux, macOS, or Linux under WSL.')
if not (PROJECT/'scripts/verify.py').is_file():
    parser.error('The complete repository checkout is required.')
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
OUT = args.output.resolve() if args.output else HERE/'runs'/stamp/'original_replay'
if OUT.exists() and any(OUT.iterdir()):
    parser.error('Output directory must be new or empty; archived reports are never overwritten.')
WORK = OUT/'work'
OUT.mkdir(parents=True, exist_ok=True)
(WORK / 'tmp').mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env['TMPDIR'] = str(WORK / 'tmp')
env['PYTHONDONTWRITEBYTECODE'] = '1'
command = [sys.executable, 'scripts/verify.py', '--full-global',
           '--replay-rank10-equality', '--full-local-extensions',
           '--full-equality', '--workers', str(args.workers)]
previous_runs = set((PROJECT/'verification_runs').glob('*/run.json'))
start = time.monotonic()
record = {'started_utc': datetime.now(timezone.utc).isoformat(),
          'command': command, 'python': platform.python_version(),
          'platform': platform.platform(), 'status': 'RUNNING',
          'scope': 'Fresh rerun of the existing verification algorithms and every optional regeneration; not a new independent implementation.',
          'jobs': []}
running = None

def write_record():
    (OUT / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')

def save_generated_reports():
    temps = sorted((WORK/'tmp').glob('lattice-certificates-*/certificates'))
    if not temps:
        return
    evidence = temps[-1]
    reports = [
      'research_20261007/equality/equality_verification.json',
      'research_20261007/embeddings/all_fixed_K9_extensions_verified.json',
      'research_20261007/embeddings/all_fixed_K9_extensions_checkpoint.json',
      'research_20261007/rank10/global_rank10_certificate_verified.json',
      'research_20261007/rank10/global_replay_progress.json',
      'research_20261008/rank10_equality/equality_certificate_verified.json',
      'research_20261008/rank10_equality/equality_full_replay_record.json',
    ]
    for rel in reports:
        source = evidence / rel
        # Preserve only reports belonging to a verifier already completed now.
        name = Path(rel).name
        owner = ('verify_equality.py' if 'equality_verification' in name else
                 'verify_all_fixed_K9_extensions.py' if 'fixed_K9' in name else
                 'verify_global_rank10_certificate.py' if 'global_' in name else
                 'verify_equality_certificate.py')
        if any(j.get('status') == 'PASS' and Path(j['path']).name == owner for j in record['jobs']) and source.is_file():
            dest = OUT / 'generated_reports' / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
    for rel, owner in [
        ('research_20261007/rank10/global_replay_records', 'verify_global_rank10_certificate.py'),
        ('research_20261008/rank10_equality/replay_records', 'verify_equality_certificate.py')]:
        if any(j.get('status') == 'PASS' and Path(j['path']).name == owner for j in record['jobs']):
            source = evidence / rel
            dest = OUT / 'generated_reports' / rel
            if source.is_dir() and not dest.exists():
                shutil.copytree(source, dest)

write_record()
with (OUT/'console.log').open('w') as log, (OUT/'events.jsonl').open('w') as events:
    proc = subprocess.Popen(command, cwd=PROJECT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding='utf-8')
    for line in proc.stdout:
        elapsed = time.monotonic() - start
        log.write(line); log.flush()
        event = {'elapsed_seconds': round(elapsed, 3), 'line': line.rstrip()}
        events.write(json.dumps(event)+'\n'); events.flush()
        print(line, end='', flush=True)
        if line.startswith('RUN '):
            parts=line.split()
            running={'path':parts[1], 'args':parts[2:], 'started_seconds':elapsed, 'status':'RUNNING'}
            record['jobs'].append(running)
        elif line.startswith('PASS ') and running is not None:
            running.update(status='PASS', elapsed_seconds=round(elapsed-running['started_seconds'],3))
            save_generated_reports()
            running=None
        write_record()
    code=proc.wait()
record.update(exit_code=code, status='PASS' if code==0 else 'FAIL',
              finished_utc=datetime.now(timezone.utc).isoformat(),
              elapsed_seconds=round(time.monotonic()-start,3))
if running is not None:
    running['status']='FAIL'
    running['elapsed_seconds']=round(time.monotonic()-start-running['started_seconds'],3)
runs=sorted(set((PROJECT/'verification_runs').glob('*/run.json')) - previous_runs)
if runs:
    run=runs[-1]
    shutil.copyfile(run,OUT/'wrapper_run.json')
    shutil.copytree(run.parent/'logs',OUT/'logs',dirs_exist_ok=True)
check=subprocess.run([sys.executable,'verify_file_hashes.py'],cwd=PROJECT/'certificates',env=env,capture_output=True,text=True)
(OUT/'hashes_after.log').write_text(check.stdout+check.stderr)
record['source_manifest_recheck_exit_code']=check.returncode
if check.returncode:
    record['status']='FAIL'
write_record()
shutil.rmtree(WORK, ignore_errors=True)
print(json.dumps({k:v for k,v in record.items() if k!='jobs'},indent=2),flush=True)
sys.exit(0 if record['status']=='PASS' else 1)
