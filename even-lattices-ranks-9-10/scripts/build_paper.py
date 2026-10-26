#!/usr/bin/env python3
"""Build the English standalone manuscript with three XeLaTeX passes."""
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    source = root / 'manuscript' / 'paper.tex'
    engine = shutil.which('xelatex')
    if engine is None:
        raise SystemExit('XeLaTeX is required. Alternatively upload paper.tex to Overleaf and select XeLaTeX.')
    build = root / 'build' / 'paper'
    build.mkdir(parents=True, exist_ok=True)
    for index in range(1, 4):
        print(f'XeLaTeX pass {index}/3', flush=True)
        with (build / f'pass-{index}.log').open('w', encoding='utf-8') as log:
            result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error',
                                     '-file-line-error', '-output-directory', str(build),
                                     str(source)], cwd=source.parent,
                                    stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit(f'Compilation failed; see {build / f"pass-{index}.log"}')
    shutil.copyfile(build / 'paper.pdf', root / 'manuscript' / 'paper.pdf')
    shutil.copyfile(source, root / 'manuscript' / 'paper.txt')
    print('Built manuscript/paper.pdf; paper.txt is identical to paper.tex.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
