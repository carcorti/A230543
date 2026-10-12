# OEIS A230543

Carlo Corti — local publication draft, October 2026.

**Local pre-upload candidate.** The package excludes internal review metadata
and validates the exact file and directory inventory. Repository and DOI
locators remain prospective; no upload, release or remote reproduction is
claimed.

A230543 lists increasing integers `n >= 2` with positive arithmetic derivatives
`D(n)` and `D(D(n))` such that `n^2 + D(n)^2 + D(D(n))^2` is a square.
Here `D(0) = D(1) = 0`, `D(p) = 1` for primes, and
`D(ab) = a D(b) + b D(a)`.
The 40-row prefix ends at `a(40) = 129667967451`. Eighteen terms extend the
accepted 22-row baseline; the recorded C scan covers
`408918817 <= n <= 130000000000`. Full negative coverage is conditional on that
implementation, and negative completeness of the inherited baseline was not
locally repeated. The next index is unresolved:
`130000000000 < a(41) <= 244140625000`; the upper witness is unindexed.

The C implementation uses segmented factorization for the first derivative,
deterministic 64-bit primality and bounded Pollard rho with exact trial-division
fallback for the second derivative, and GMP for the square test. Completed
blocks advance durable state; eight threads and input cap `10^16` are supported.
The cap describes numerical capacity, not completed coverage.

## Contents

| Path | Purpose |
|---|---|
| `src/a230543.c`, `src/Makefile` | Byte-identical reviewed production source and build recipe |
| `data/b230543.txt` | Sole canonical 40-term indexed b-file |
| `data/witnesses.tsv` | `i, n, D(n), D(D(n)), root`, exact positive witnesses |
| `data/quadruples.txt` | Same witnesses in the original commented documentary format |
| `data/forms.tsv` | Primitive coordinates, gcd, rational rate, scale core, degree and prime parameters |
| `data/history/prefix22.txt` | Explicitly historical accepted baseline, not a competing current b-file |
| `paper/A230543_v2.tex` | Unmodified current English monolithic manuscript, inline bibliography |
| `validation/run.py` | Reconstructed fail-closed public validation command |
| `validation/check.py`, `validation/reference.tsv` | Unchanged independent trial-division oracle and 30 fixtures |
| `validation/backend_probe.c` | Unchanged C white-box wrapper, shared production backend |
| `validation/notes.md`, `validation/summary.md` | Methods, scopes, dependencies and local results |
| `evidence/*.tar.gz` | Separate compact build, campaign, scientific and development evidence |
| `docs/origins.tsv`, `docs/archives.tsv` | Source-to-package aliases, original member hashes and sizes |
| `docs/sources.md`, `docs/cli.md` | Source acquisition/build requirements and exact CLI |
| `CITATION.cff`, `LICENSE`, `SHA256SUMS`, `.gitignore` | Draft citation, existing MIT license, inventory and generated-file exclusions |

## Build and verify

Tested on x86_64 Linux, Python 3.12.3, GCC 13.3.0, GMP 6.3.0,
OpenSSL 3.0.13, GNU OpenMP and SymPy 1.12. The original executable also needs
its Linux/glibc ABI. Install GCC/make, GMP and OpenSSL development packages,
`pkg-config`, and Python with `sympy==1.12`; see `docs/sources.md`.

```sh
make -C src
make -C src clean
python3 -B validation/run.py
```

The public command uses only this package, checks the exact file/directory inventory and all
archive members, extracts and builds in temporary directories, and exits
nonzero at a mismatch. It runs bounded arithmetic, native witness replay and
backend tests. It executes no `init`/`next`, full negative campaign or PDF
creation. Expect stage PASS lines and a final JSON `status: PASS`.
The complete suite can take several minutes. It also works under a renamed
clone/extraction root and ignores only root `.git/` provider metadata.
Use `python3 -B -O validation/run.py` for the same shared implementation under
optimized Python. Generated files inside the package intentionally fail the
inventory check; run `make -C src clean` after a manual build.

To regenerate the three derived public tables without overwriting inputs:

```sh
python3 -B validation/run.py --export /tmp/a230543-data
```

The destination must not exist. This writes `b230543.txt`, `witnesses.tsv` and
`forms.tsv`; their bytes must match `data/`. Both witness text tables and the
b-file preserve the author's required final empty record (`LF LF`).

## Manuscript and evidence

`paper/A230543_v2.tex` needs no external bibliography or images. Its build
requirements and a PDF-suppressed syntax check are in `docs/sources.md`.
No PDF is included. The filename retains `v2`, and the intentional DOI sentinel
is `10.5281/zenodo.xxxxxxxx`. `CITATION.cff` reserves first-release version
`v1.0`; it has no release date because no release has occurred.

The archives retain original bytes under short aliases. Inspect or unpack:

```sh
tar -tzf evidence/studies.tar.gz
mkdir /tmp/a230543-evidence
tar -xzf evidence/runs.tar.gz -C /tmp/a230543-evidence
tar -xzf evidence/build.tar.gz -C /tmp/a230543-evidence
```

The runner checks extraction/member hashes before using any input. The original
run binary is retained solely for identity-bound historical replay; a rebuild
is never substituted into historical run metadata. The compact run archive
contains all 22 seals, configurations, aggregates and original timing rows.
Development transcripts and original diagnostic drivers in `tests.tar.gz` are
historical evidence, not freshly repeated sanitizer/concurrency certification.

Private manuscript/code review conversations and process records, obsolete
drafts, caches, redundant compiled test variants and third-party full-text
papers are excluded, including from the archives. One historical regression
driver has a reviewer-attribution comment replaced by a technical description;
its executable statements are unchanged. Member hashes identify the actual
curated bytes; the original driver remains in the private workspace.
Bibliographic locators and reading limitations are in the manuscript and
`docs/sources.md`. The complete current proofs do not depend on distributing
the separately cited local A249106 manuscript. No sparse indexed term beyond
index 40 is claimed. The documentary OEIS attachment remains an editorial
candidate in the workspace; its byte-identical public counterpart has the
clear repository name `data/quadruples.txt`.
