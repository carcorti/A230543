# Dependencies and consulted sources

The TeX source is self-contained. Use pdfTeX (tested version 3.141592653-2.6-1.40.25)
with LaTeX packages `fontenc`, `inputenc`, `lmodern`, `geometry`, `amsmath`,
`amssymb`, `amsthm`, `booktabs`, `longtable`, `array`, `xcolor`, `xurl`, and
`hyperref`. A Debian/Ubuntu TeX Live installation with `texlive-latex-base`,
`texlive-latex-recommended`, `texlive-latex-extra`, and `lmodern` supplies them.
To check syntax without producing a PDF, from the package root:

```sh
mkdir -p /tmp/a230543-tex
pdflatex -draftmode -interaction=nonstopmode -halt-on-error -output-directory=/tmp/a230543-tex paper/A230543_v2.tex
```

Repeat that exact command three times to settle cross-references. Auxiliary
outputs go outside the package. This is syntax/reference QA; visual page QA
requires separate authorization to generate a PDF.

The production build uses the unchanged strict Makefile, GCC with GNU unsigned
128-bit integers, POSIX files/locks/signals, OpenMP, GMP and OpenSSL EVP hashes.
The tested native environment is x86_64 Linux/glibc 2.39, GCC 13.3.0,
GMP 6.3.0, OpenSSL 3.0.13 and GNU libgomp. The public runner checks native library
versions and reports compiler/Python versions. It requires Python >= 3.10 and
SymPy 1.12 (checked exactly). Install `build-essential`, `libgmp-dev`,
`libssl-dev`, `pkg-config`, and SymPy in your chosen Python environment.
Historical LLVM 18/libomp/Archer, ASan/UBSan, cppcheck and clang-tidy tests are
preserved as records; these tools are not dependencies of the public runner.
No new sanitizer result is inferred from archived PASS transcripts.

Consulted third-party full texts are not bundled, because redistribution
permission has not been established. Obtain them through these primary locators:

| Source | Role and access boundary |
|---|---|
| [Ufnarovski–Åhlander (2003)](https://cs.uwaterloo.ca/journals/JIS/VOL6/Ufnarovski/ufnarovski.html) | Product rule, derivative bound, integer/rational rate theory; full publisher text consulted |
| [Kovič (2012)](https://cs.uwaterloo.ca/journals/JIS/VOL15/Kovic/kovic4.pdf) | Integer-rate prime-power factorization; full publisher text consulted |
| [Forišek–Jančina (2015)](https://ceur-ws.org/Vol-1326/020-Forisek.pdf) | Deterministic seven-base test below 2^64, Section 1.4/Theorem 3 |
| [Pollard (1975)](https://pages.cs.wisc.edu/~cs812-1/pollardrho.pdf) | Factor finding; heuristic speed separated from deterministic fallback |
| [GNU MP integer roots](https://gmplib.org/manual/Integer-Roots) | Exact square predicate and roots, manual version 6.3.0 |
| [Tossavainen et al. (2024)](https://doi.org/10.1080/07468342.2023.2268494) | Historical/expository context; author-uploaded full text consulted during v2 revision |
| [Hoepli book](https://www.hoepli.it/libro/la-derivata-aritmetica-/9788820358648.html) | Publisher metadata only; full book not consulted |

The other Balzarotti–Lava volume, Sandit ISBN 9788869287480, was consulted
through metadata only; year and full text remain unverified. The related OEIS
entries and their exact mathematical roles are cited inline in the manuscript.
The accepted 22-row A230543 baseline is a dated inherited snapshot, not a
claim that the current online endpoint was reverified. The cited Carlo Corti
A249106 manuscript v4 remains separately local, with public availability
unverified; A230543 proves its needed forms in its own current manuscript.
