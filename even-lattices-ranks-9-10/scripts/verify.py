#!/usr/bin/env python3
"""Check the archived evidence in a temporary copy, preserving certified bytes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hashes-only', action='store_true',
                        help='Check archived file identity without running mathematical verifiers.')
    parser.add_argument('--full-global', action='store_true')
    parser.add_argument('--replay-rank10-equality', action='store_true')
    parser.add_argument('--full-local-extensions', action='store_true')
    parser.add_argument('--full-equality', action='store_true',
                        help='Historical flag: regenerate the older RANK-NINE equality certificate.')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    if not __debug__:
        parser.error('Assertions must be enabled: do not use -O, -OO, or PYTHONOPTIMIZE.')
    if args.workers < 1:
        parser.error('--workers must be positive')
    flags = [flag for flag in ('--full-global', '--replay-rank10-equality',
                              '--full-local-extensions', '--full-equality')
             if getattr(args, flag[2:].replace('-', '_'))]
    if args.hashes_only and flags:
        parser.error('--hashes-only cannot be combined with regeneration flags')
    if flags and os.name == 'nt':
        parser.error('Run full regeneration on Linux, macOS, or Linux under WSL.')
    root = Path(__file__).resolve().parents[1]
    evidence = root / 'certificates'
    if not (evidence / 'verify_new_results.py').is_file():
        parser.error('The complete certificates directory is required.')
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable, str(evidence / 'verify_file_hashes.py')],
                            cwd=evidence, env=env)
    if result.returncode or args.hashes_only:
        return result.returncode
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    run_dir = root / 'verification_runs' / stamp
    run_dir.mkdir(parents=True)
    start = time.perf_counter()
    invoked_logs = []
    with tempfile.TemporaryDirectory(prefix='lattice-certificates-') as temp:
        work = Path(temp) / 'certificates'
        shutil.copytree(evidence, work)
        command = [sys.executable, str(work / 'verify_new_results.py'),
                   '--workers', str(args.workers), *flags]
        with (run_dir / 'console.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen(command, cwd=work, env=env,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, encoding='utf-8', errors='replace')
            assert process.stdout is not None
            for line in process.stdout:
                print(line, end='', flush=True)
                log.write(line)
                log.flush()
                if line.startswith('RUN '):
                    fields = line.split()
                    suffix = ('_control' if '--control' in fields else
                              '_replay' if '--replay' in fields else '')
                    invoked_logs.append(
                        f'{len(invoked_logs) + 1:02d}_{Path(fields[1]).stem}{suffix}.log')
            returncode = process.wait()
        (run_dir / 'logs').mkdir()
        for name in invoked_logs:
            source = work / 'local_replay_logs' / name
            if source.is_file():
                shutil.copyfile(source, run_dir / 'logs' / name)
    record = {
        'timestamp_utc': stamp,
        'python': platform.python_version(),
        'platform': platform.platform(),
        'mode': 'routine' if not flags else 'routine plus requested regenerations',
        'flags': flags,
        'workers': args.workers,
        'certificate_manifest_sha256': hashlib.sha256(
            (evidence / 'SHA256SUMS').read_bytes()).hexdigest(),
        'elapsed_seconds': round(time.perf_counter() - start, 3),
        'exit_code': returncode,
        'invoked_check_count': len(invoked_logs),
        'status': 'PASS' if returncode == 0 else 'FAIL',
        'scope': 'Executed checks only; not external peer review or formal verification.'
    }
    (run_dir / 'run.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('Run record:', run_dir.relative_to(root))
    return returncode


if __name__ == '__main__':
    raise SystemExit(main())
