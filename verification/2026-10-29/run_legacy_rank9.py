#!/usr/bin/env python3
"""Replay the earlier rank-nine base and its hardened audit in disposable copies.

Uses at most two sequential shell runners at once; each runner itself uses one
process at a time. The preserved source archive is hashed before and after.
No package source is overwritten. This closes a historical coverage gap in
verify_new_results.py, whose --full-equality option regenerates only additions.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent


def package_root():
    suffix = Path('certificates/research_20261007/recovered/rank9_audit_evidence_20260910')
    for parent in HERE.parents:
        for root in (parent / 'even-lattices-ranks-9-10', parent):
            if (root / suffix / 'run_audit_checks.sh').is_file():
                return root / suffix
    raise FileNotFoundError('Cannot locate the preserved September rank-nine audit package')


def manifest(root):
    return {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=2, choices=(1, 2))
    parser.add_argument('--output', type=Path,
                        help='Empty output directory; defaults to a new UTC-stamped runs directory')
    args = parser.parse_args()
    if sys.flags.optimize:
        raise SystemExit('Assertions must be enabled')
    source = package_root()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out = (args.output or HERE/'runs'/stamp/'legacy_rank9_replay').resolve()
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise SystemExit(f'Refusing to overwrite nonempty output: {out}')
    out.mkdir(parents=True, exist_ok=True)
    before = manifest(source)
    (out/'source_manifest.json').write_text(json.dumps(before, indent=2)+'\n')
    nested = Path('audit_20260910/rank9_complete_certificates')
    jobs = [
        ('full_regeneration', nested, 'run_full_regeneration.sh',
         'FULL_EXACT_REGENERATION_BYTE_IDENTICAL'),
        ('mandatory_certificate_checks', nested, 'run_all_checks.sh',
         'ALL_RELEASED_EXACT_CERTIFICATES_PASS'),
        ('supplementary_hardened_audit', Path('.'), 'run_audit_checks.sh',
         'ALL_SUPPLEMENTARY_AUDIT_CHECKS_PASS'),
    ]
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'workers': args.workers,
              'source_files_hashed': len(before), 'jobs': [],
              'scope': 'Fresh replay of the legacy strict rank-nine base, complete lower-flag generation through rank seven, all mandatory residual branches, and all five supplementary audit programs including the known zero-layer regression and hardened branch. Reuses archived algorithms; not independent external refereeing.'}
    start = time.monotonic()

    def run(job):
        name, cwd_rel, script, marker = job
        with tempfile.TemporaryDirectory(prefix='legacy-rank9-') as tmp:
            copied = Path(tmp)/'package'
            shutil.copytree(source, copied, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            command = ['bash', script]
            env = os.environ.copy()
            env.pop('PYTHONOPTIMIZE', None)
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            env['PYTHONUNBUFFERED'] = '1'
            log = out/f'{name}.log'
            t = time.monotonic()
            print('RUN', name, flush=True)
            with log.open('w') as stream:
                result = subprocess.run(command, cwd=copied/cwd_rel, env=env,
                                        stdout=stream, stderr=subprocess.STDOUT)
            body = log.read_text(errors='replace')
            item = {'name': name, 'command': command, 'cwd_relative_to_copy': str(cwd_rel),
                    'exit_code': result.returncode, 'marker': marker,
                    'marker_found': marker in body, 'seconds': time.monotonic()-t,
                    'log_sha256': sha256(log.read_bytes()).hexdigest(),
                    'status': 'PASS' if result.returncode == 0 and marker in body else 'FAIL'}
            after_copy = manifest(copied)
            changes = {rel: h for rel, h in after_copy.items() if before.get(rel) != h}
            item['changed_copy_files'] = changes
            for rel in changes:
                target = out/'generated'/name/rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(copied/rel, target)
            print(item['status'], name, round(item['seconds'], 3), flush=True)
            return item

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(run, job) for job in jobs]):
            report['jobs'].append(future.result())
            (out/'progress.json').write_text(json.dumps(report, indent=2)+'\n')
    if all(row['status'] == 'PASS' for row in report['jobs']):
        text = (out/'supplementary_hardened_audit.log').read_text()
        first = '[5/5] Hardened top-down branch verification\n'
        last = 'ALL_SUPPLEMENTARY_AUDIT_CHECKS_PASS\n'
        if text.count(first) != 1 or text.count(last) != 1:
            raise RuntimeError('Cannot isolate the fresh hardened transcript')
        fresh = text.split(first, 1)[1].split(last, 1)[0]
        audit = source/'audit_20260910'
        targets = [audit/'verify_rank7_topdown_hardened.transcript',
                   audit/'rank9_complete_certificates/certificate/verify_rank7_topdown.transcript']
        same = {str(p.relative_to(audit)): fresh == p.read_text() for p in targets}
        regression_markers = ['OLD_HELPER_ACCEPTS_TARGET True',
                              'HARDENED_HELPER_ACCEPTS_TARGET False',
                              'TARGET_DETERMINANT 14256 SECOND_LAYER_NORM 2',
                              'ZERO_CLASS_LAYER_REGRESSION_PASS']
        regression = all(marker in text for marker in regression_markers)
        postcheck = {'checked_utc': datetime.now(timezone.utc).isoformat(),
                     'fresh_hardened_transcript_sha256': sha256(fresh.encode()).hexdigest(),
                     'byte_equal_to_archived_transcripts': same,
                     'regression_reproduced': regression,
                     'status': 'PASS' if all(same.values()) and regression else 'FAIL'}
        (out/'hardened_branch_comparison.json').write_text(json.dumps(postcheck, indent=2)+'\n')
        report['hardened_branch_postcheck'] = postcheck['status']
    report['source_unchanged'] = manifest(source) == before
    report['elapsed_seconds'] = time.monotonic()-start
    report['status'] = 'PASS' if report['source_unchanged'] and all(
        row['status'] == 'PASS' for row in report['jobs']) and report.get(
            'hardened_branch_postcheck') == 'PASS' else 'FAIL'
    (out/'summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print('LEGACY_RANK9_COMPLETE_REPLAY', report['status'], flush=True)
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
