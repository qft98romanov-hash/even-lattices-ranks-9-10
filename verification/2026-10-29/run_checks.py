#!/usr/bin/env python3
"""Run supplementary checks in a disposable copy and retain only fresh results.

Examples:
  python run_checks.py
  python run_checks.py --packages exact windows pari gap magma sage oscar
  python run_checks.py --packages exact pari --gp /path/to/gp --require-all

The original certificates and the retained results/ snapshot are never modified.
Missing executables are NOT_RUN, not PASS. A zero exit code is insufficient:
each checker must print its exact completion marker and, when applicable, write
a fresh JSON report with an accepted status. Numerical cross-checks do not gain
stronger mathematical guarantees merely by being invoked by this runner.
"""
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

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]

CHECKS = {
    'exact': {'script': 'check_exact.py', 'binary': 'python', 'arguments': [],
              'marker': 'INDEPENDENT_SYMPY_FRACTION_CHECKS_PASS',
              'report': 'exact.json', 'statuses': ['PASS']},
    'windows': {'script': 'check_windows.py', 'binary': 'python', 'arguments': [],
                'marker': 'INDEPENDENT_WINDOWS_HNF_AND_CLUSTER_CHECK_PASS',
                'report': 'windows.json', 'statuses': ['PASS']},
    'pari': {'script': 'check_pari.gp', 'binary': 'gp', 'arguments': ['-q', '-f'],
             'marker': 'PASS_PARI_CROSSCHECK'},
    'gap': {'script': 'check_orbits.g', 'binary': 'gap', 'arguments': ['-q', '-T'],
            'marker': 'GAP_ORBIT_CHECK_PASS', 'report': 'gap_orbits.json', 'statuses': ['PASS']},
    'magma': {'script': 'check_magma.m', 'binary': 'magma', 'arguments': [],
              'marker': 'ALL_MAGMA_EXPLICIT_CHECKS_PASS'},
    'sage': {'script': 'check_sage.py', 'binary': 'sage', 'arguments': ['-python'],
             'marker': 'ALL_SAGE_EXPLICIT_CROSS_CHECKS_PASS',
             'report': 'sage_run.json', 'statuses': ['PASS_CROSS_CHECK']},
    'oscar': {'script': 'check_oscar.jl', 'binary': 'julia', 'arguments': [],
              'marker': 'ALL_OSCAR_EXPLICIT_CHECKS_PASS'},
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_binary(name: str, override: str | None) -> str | None:
    if name == 'python':
        return sys.executable
    candidate = override or name
    # Explicit paths are made absolute before changing the subprocess cwd.
    path = Path(candidate).expanduser()
    if path.is_file():
        return str(path.resolve())
    return shutil.which(candidate)


def execute(command: list[str], cwd: Path, log_path: Path,
            environment: dict, timeout: float | None) -> dict:
    started = time.perf_counter()
    try:
        with log_path.open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=cwd, env=environment,
                                    stdout=log, stderr=subprocess.STDOUT,
                                    text=True, timeout=timeout, check=False)
        return {'returncode': result.returncode,
                'elapsed_seconds': round(time.perf_counter() - started, 6)}
    except subprocess.TimeoutExpired:
        return {'returncode': None, 'error_type': 'timeout',
                'error': f'Execution exceeded {timeout} seconds',
                'elapsed_seconds': round(time.perf_counter() - started, 6)}
    except OSError as error:
        return {'returncode': None, 'error_type': 'invocation_error',
                'error': f'{type(error).__name__}: {error}',
                'elapsed_seconds': round(time.perf_counter() - started, 6)}


def version_evidence(log: str, report: dict | None) -> dict:
    evidence = {}
    if report:
        for key in ('python', 'sympy', 'gap_version', 'sage_version'):
            if key in report:
                evidence[key] = report[key]
    prefixes = ('PARI_VERSION ', 'JULIA_VERSION ', 'OSCAR_VERSION ', 'MAGMA_VERSION ',
                'Magma V', 'GAP_VERSION ')
    evidence['version_lines'] = [line for line in log.splitlines()
                                 if line.startswith(prefixes)]
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packages', nargs='+', choices=list(CHECKS),
                        default=['exact', 'windows', 'pari', 'gap'])
    for name in ('gp', 'gap', 'magma', 'sage', 'julia'):
        parser.add_argument('--' + name, help=f'Executable path/name for {name}')
    parser.add_argument('--require-all', action='store_true',
                        help='Return nonzero when any requested executable is unavailable')
    parser.add_argument('--timeout', type=float, default=None,
                        help='Optional per-command timeout in seconds (default: no limit)')
    args = parser.parse_args()
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
        parser.error('Run without -O, -OO or a nonzero PYTHONOPTIMIZE setting')
    if args.timeout is not None and args.timeout <= 0:
        parser.error('--timeout must be positive')
    packages = list(dict.fromkeys(args.packages))
    certificate_source = REPOSITORY / 'even-lattices-ranks-9-10' / 'certificates'
    if not (certificate_source / 'verify_new_results.py').is_file():
        parser.error('The original nested certificates/ directory is required')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    run_directory = HERE / 'runs' / stamp
    run_directory.mkdir(parents=True)
    (run_directory / 'logs').mkdir()
    started = time.perf_counter()
    manifest = {
        'schema': 1, 'timestamp_utc': stamp, 'status': 'RUNNING',
        'python': platform.python_version(), 'platform': platform.platform(),
        'packages_requested': packages, 'require_all': args.require_all,
        'runner_sha256': digest(Path(__file__).resolve()),
        'archive_manifest_sha256': digest(certificate_source / 'SHA256SUMS'),
        'checks': {name: {'status': 'NOT_RUN', 'reason': 'preparation_not_completed'}
                   for name in packages}, 'exporters': [],
        'scope': 'Fresh runs of selected supplementary checks only. '
                 'No external review, formal verification or new theorem is implied.',
    }
    environment = os.environ.copy()
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    manifest_path = run_directory / 'run.json'

    def save_manifest() -> None:
        manifest['elapsed_seconds'] = round(time.perf_counter() - started, 6)
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

    save_manifest()
    try:
        with tempfile.TemporaryDirectory(prefix='lattice-independent-checks-') as temporary:
            mirror = Path(temporary) / 'repository'
            work = mirror / 'verification' / HERE.name
            shutil.copytree(HERE, work, ignore=shutil.ignore_patterns(
                'results', 'runs', '__pycache__', '*.pyc'))
            shutil.copytree(certificate_source,
                            mirror / 'even-lattices-ranks-9-10' / 'certificates')
            (work / 'results').mkdir()

            # All exported literals are rebuilt from the archived source in the
            # disposable mirror. No retained result can satisfy a report check.
            for exporter in ('export_inputs.py', 'export_pari.py',
                             'export_gap.py', 'export_adapters.py'):
                command = [sys.executable, exporter]
                log_path = run_directory / 'logs' / (Path(exporter).stem + '.log')
                result = execute(command, work, log_path, environment, args.timeout)
                result.update(script=exporter, command=command,
                              log=log_path.relative_to(run_directory).as_posix())
                manifest['exporters'].append(result)
                if result['returncode'] != 0:
                    raise RuntimeError(f'Input exporter failed: {exporter}; see {log_path}')
            manifest['input_sha256'] = digest(work / 'data/lattices.json')
            manifest['input_source_provenance'] = json.loads(
                (work / 'data/lattices.json').read_text(encoding='utf-8'))['provenance']

            for package in packages:
                spec = CHECKS[package]
                executable = resolve_binary(spec['binary'], getattr(args, spec['binary'], None))
                entry = {'status': 'NOT_RUN', 'script': spec['script'],
                         'script_sha256': digest(work / spec['script']),
                         'required_completion_marker': spec['marker']}
                manifest['checks'][package] = entry
                if executable is None:
                    entry.update(reason='executable_not_found',
                                 requested_executable=getattr(args, spec['binary'], None) or spec['binary'])
                    print(package, 'NOT_RUN: executable not found', flush=True)
                    save_manifest()
                    continue
                command = [executable, *spec['arguments'], spec['script']]
                entry['command'] = command
                log_path = run_directory / 'logs' / (package + '.log')
                entry['log'] = log_path.relative_to(run_directory).as_posix()
                print(package, 'RUN', flush=True)
                entry.update(execute(command, work, log_path, environment, args.timeout))
                text = log_path.read_text(encoding='utf-8', errors='replace')
                if package == 'pari':
                    # The independent set-comparison checker consumes this
                    # freshly captured transcript, never the retained snapshot.
                    shutil.copyfile(log_path, work / 'results/pari.log')
                marker_ok = spec['marker'] in {line.strip() for line in text.splitlines()}
                entry['completion_marker_found'] = marker_ok
                fresh_report = None
                report_ok = True
                if 'report' in spec:
                    target = work / 'results' / spec['report']
                    entry['report'] = 'results/' + spec['report']
                    try:
                        fresh_report = json.loads(target.read_text(encoding='utf-8'))
                        report_ok = fresh_report.get('status') in spec['statuses']
                        entry['report_status'] = fresh_report.get('status')
                        if 'input_sha256' in fresh_report:
                            report_ok = report_ok and fresh_report['input_sha256'] == manifest['input_sha256']
                    except (OSError, ValueError) as error:
                        report_ok = False
                        entry['report_error'] = f'{type(error).__name__}: {error}'
                entry['version_evidence'] = version_evidence(text, fresh_report)
                entry['status'] = ('PASS' if entry['returncode'] == 0 and marker_ok and report_ok else 'FAIL')
                print(package, entry['status'], flush=True)
                save_manifest()
            if all(manifest['checks'].get(name, {}).get('status') == 'PASS'
                   for name in ('exact', 'pari')):
                print('pari_exact_comparison RUN', flush=True)
                command = [sys.executable, 'compare_pari_vectors.py']
                log_path = run_directory / 'logs/pari_exact_comparison.log'
                entry = execute(command, work, log_path, environment, args.timeout)
                text = log_path.read_text(encoding='utf-8', errors='replace')
                marker = 'PARI_EXACT_VECTOR_COMPARISON_PASS'
                marker_ok = marker in {line.strip() for line in text.splitlines()}
                target = work / 'results/pari_vector_comparison.json'
                report_ok = False
                try:
                    report_ok = json.loads(target.read_text(encoding='utf-8')).get('status') == 'PASS'
                except (OSError, ValueError):
                    pass
                entry.update(command=command, script='compare_pari_vectors.py',
                             script_sha256=digest(work / 'compare_pari_vectors.py'),
                             log='logs/pari_exact_comparison.log',
                             required_completion_marker=marker, completion_marker_found=marker_ok,
                             report='results/pari_vector_comparison.json',
                             status='PASS' if entry['returncode'] == 0 and marker_ok and report_ok else 'FAIL')
                manifest['checks']['pari_exact_comparison'] = entry
                print('pari_exact_comparison', entry['status'], flush=True)
                save_manifest()
            shutil.copytree(work / 'results', run_directory / 'results')
            shutil.copytree(work / 'data', run_directory / 'inputs')
            manifest['fresh_result_sha256'] = {
                path.relative_to(run_directory).as_posix(): digest(path)
                for path in sorted((run_directory / 'results').rglob('*')) if path.is_file()}
            statuses = [entry['status'] for entry in manifest['checks'].values()]
            if 'FAIL' in statuses:
                manifest['status'] = 'FAIL'
            elif all(status == 'NOT_RUN' for status in statuses):
                manifest['status'] = 'NOT_RUN'
            elif 'NOT_RUN' in statuses:
                manifest['status'] = 'PASS_WITH_NOT_RUN'
            else:
                manifest['status'] = 'PASS'
    except Exception as error:
        manifest['status'] = 'FAIL'
        manifest['error'] = f'{type(error).__name__}: {error}'
        print(manifest['error'], file=sys.stderr, flush=True)
    finally:
        save_manifest()
    print('RUN_STATUS', manifest['status'])
    print('RUN_RECORD', manifest_path)
    if manifest['status'] == 'FAIL':
        return 1
    if args.require_all and any(entry['status'] == 'NOT_RUN' for entry in manifest['checks'].values()):
        return 2
    if manifest['status'] == 'NOT_RUN':
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
