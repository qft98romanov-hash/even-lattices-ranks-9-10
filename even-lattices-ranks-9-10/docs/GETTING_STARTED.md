# Prepare a GitHub repository

This package is ready to be unpacked as a repository working tree. Preparation
has not created a remote repository or uploaded any source material.

1. Unpack `even-lattices-ranks-9-10` and read `README.md`.
2. Open `manuscript/paper.pdf`. Edit `manuscript/paper.tex` when ready.
3. Run `python scripts/verify.py --hashes-only` to check the preserved evidence.
4. Run `python scripts/verify.py` for the routine exact mathematical checks.
5. Create an empty **private** GitHub repository while the collaboration and
   manuscript are under review. Suggested name: `even-lattices-ranks-9-10`.
6. In Git Bash, macOS Terminal, or a Linux shell, open the unpacked directory
   and run the commands below, replacing the quoted URL placeholder with the
   repository URL copied from GitHub.

```sh
git init
git add .
git commit -m "Prepare English research draft and exact certificates"
git branch -M main
git remote add origin "PASTE_YOUR_REPOSITORY_URL_HERE"
git push -u origin main
```

Git uses your configured author identity and authentication. The package does
not include account credentials. It contains thousands of certificate files;
Git is the practical upload route for retaining the complete directory tree.

The `.gitattributes` file preserves file bytes, including on Windows. Keep it:
automatic line-ending conversion would otherwise invalidate certificate hashes.

## GitHub description

Suggested short description:

> Minimum determinants of even integral lattices in ranks 9 and 10, with exact certificates and applications to cross-section sphere packings. Working draft under review.

## Build or edit the paper

Local build:

```sh
python scripts/build_paper.py
```

This requires XeLaTeX. For Overleaf, upload the separate Overleaf ZIP, select
XeLaTeX as the compiler, and compile `main.tex`. The reference list is embedded;
no bibliography service or downloaded data is needed to build the paper.

## Continuous integration

The included workflow is manual: after uploading, open **Actions**, choose
**Verify exact certificates**, and select **Run workflow**. It executes the
routine suite with Python 3.12 on Ubuntu and does not publish anything. This
workflow has been prepared but has not been executed on GitHub by this task.

The repository package is a review draft. The final publication author list,
license, public repository URL, and any DOI are not invented in the metadata.
See [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) for the remaining
editorial decisions.
