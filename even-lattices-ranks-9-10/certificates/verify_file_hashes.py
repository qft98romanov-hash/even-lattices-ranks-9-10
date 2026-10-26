#!/usr/bin/env python3
"""Verify package file identity on a fresh extraction, not mathematical truth."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import sys


def main():
    root = Path(__file__).resolve().parent
    manifest = root / 'SHA256SUMS'
    if not manifest.is_file():
        raise SystemExit('Missing SHA256SUMS; use the complete extracted package.')
    failures = []
    seen = set()
    for line_no, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
        try:
            expected, name = line.split('  ', 1)
            rel = PurePosixPath(name)
            if (len(expected) != 64 or any(c not in '0123456789abcdef' for c in expected)
                    or not name or rel.is_absolute() or '..' in rel.parts
                    or name in seen):
                raise ValueError('Invalid or duplicate manifest entry')
            seen.add(name)
            path = root.joinpath(*rel.parts)
            with path.open('rb') as stream:
                digest = sha256()
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(block)
            if digest.hexdigest() != expected:
                failures.append(f'MODIFIED {name}')
        except (ValueError, OSError) as exc:
            failures.append(f'LINE {line_no}: {exc}')
    if failures:
        print('\n'.join(failures))
        print('Some verifiers rewrite status files and logs; check a fresh extraction.')
        return 1
    print(f'PACKAGE_FILE_HASHES_PASS: {len(seen)} files')
    print('Hashes establish file identity, not exhaustive coverage or mathematical correctness.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
