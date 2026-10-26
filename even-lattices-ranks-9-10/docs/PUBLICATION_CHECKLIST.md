# Repository preparation

This package is ready to inspect locally and use as the starting tree of a GitHub repository. Creating or publishing that repository is a separate action by its owner.

## Items to settle before making the repository public

- Choose the final repository name and author attribution for the standalone draft.
- Agree with the coauthors on public redistribution of the original unpublished manuscript included in `certificates/source_main4.pdf` and the historical reports. The complete certificate bundle currently preserves those materials.
- Choose appropriate reuse terms for the manuscript and code. No MIT, CC, or other license has been selected by this package.
- Keep the working-draft status, AI-assistance disclosure, external inputs, and outstanding review/novelty tasks visible.
- Perform the hash check on a fresh copy, and review the actual verification record shipped with this release.

Suggested repository name: `even-lattices-ranks-9-10`.

Suggested short description:

> Working draft and exact certificates for minimum Gram determinants and equality cases of even integral lattices of ranks 9 and 10, with applications to cross-section sphere packings.

## Initialize locally

Unpack the repository ZIP and open a terminal in the directory containing `README.md`, `manuscript/`, and `certificates/`. If it is not already a Git checkout, initialize it and review what will be added:

```bash
git init
git branch -M main
git status
git add .
git status --short
git diff --cached --stat
git commit -m "Add English working draft and exact lattice certificates"
```

Review the staged list before committing. The supplied `.gitignore` excludes routine verification outputs and transient manuscript build files; do not add unrelated scratch copies. The complete evidence bundle contains thousands of small files, so Git is more practical than manually uploading every file through the browser.

## Connect to GitHub when ready

Create an empty repository in your GitHub account. A private repository can be used while the draft and author list are being agreed. Avoid creating a second README through GitHub when importing this prepared tree.

GitHub will display the remote URL and the commands for pushing an existing repository. Use the URL of the repository you actually created; this package does not invent an account or remote address. After pushing, check that the README links to the PDF and reproduction instructions work.

## Optional release

When a reviewed snapshot is ready to share, create a versioned release that identifies it as a working draft. Attach the English PDF and the complete source/certificate archive. Do not describe internal computational checks as external peer review or formal verification.

