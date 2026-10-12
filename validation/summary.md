# Local preparation validation

Date: 2026-10-09. Local pre-upload validation; no remote release.

The earlier preflight identified internal process metadata in the test archive
and an inventory check accepting unexpected empty directories. Both corrections
were separately authorized and applied: five internal process records were
excluded, one archival driver comment was normalized, and `run.py` now checks
the exact directory set as well as files, retaining only root `.git/` metadata.
The original scientific data, C source, Makefile and manuscript remain unchanged.

The reconstructed public suite passes against frozen canonical scientific
inputs using `python3 -B validation/run.py`, including under optimized Python
(`-O`), renamed clone-like roots with root `.git/` metadata, and extracted
provider-style source archives. Missing files, changed checksummed files,
unexpected files and unexpected empty directories must fail with the intended
reason in both Python modes. Archive member identities and source mappings
refer to the curated payload. These checks simulate distribution locally;
they do not certify any actually published artifact. No new production
campaign was executed. Detailed preflight logs remain outside this payload.

Checked versions: Python 3.12.3, GCC 13.3.0, GMP 6.3.0, OpenSSL 3.0.13,
SymPy 1.12. Strict public build and native probe builds passed. The original
identity-bound binary passed `verify` for each of the six recorded runs.
The original Makefile has only build and clean targets; unsupported generic
`test`/`sanitize` targets were not invented. Historical sanitizer and qualified
TSan/concurrency/recovery evidence is archived, not freshly certified here.

Numerical PASS: 40 indexed witnesses, 30 diagnostic fixtures, 10 primitive
forms, six singleton indices, family counts 17/12/3/2; six gapless intervals
and 22 completed seals; 129591081184 native inputs and 18 appended positives;
10763 campaign-window inputs (11 positive); 33827 separate diagnostic inputs
(30 positive); 160000 rectangle pairs (15 positive, CAS-rechecked);
168 prime-screen inputs (only p=71 positive); 55 vanishing-base operands
(nine primes), forced exact fallback, numeric bounds and unindexed endpoint.
Last witness: (129667967451, 141652330200, 513638672580, 548364705651).
First unresolved index 41: 130000000000 < a(41) <= 244140625000.
The upper witness is not appended to the b-file.

Public data regenerate byte-identically using `--export` to a new directory.
Canonical b-file, witnesses and documentary table have exactly LF LF terminal
framing. The sole public b-file has indices 1..40 and its first 22 terms agree
with the explicitly historical accepted prefix. Full negative coverage
remains conditional on the C implementation and inherited baseline.

The unchanged TeX v2 passed three pdfTeX draftmode passes, with zero errors,
undefined references, overfull/underfull boxes or warnings and no PDF generated.
Its two complete scientific tables agree with the public data. Visual page QA
was not performed. Manuscript policy audit passed all 14 gates.
CITATION.cff passed CFF 1.2.0 schema validation. PERSONAL IDENTITY PASS was
established from the mutually consistent current manuscript author, source
copyright and existing author-supplied MIT LICENSE: Carlo Corti. The license
was preserved, not recreated. Third-party bibliographic authors are separate.

Public source and Makefile retain stable unversioned names and are
byte-identical to the executed source/build, so their documentary/path diff
is empty. Serialization magic-number suffixes denote formats, not lifecycle
versions. No frozen production source, working data or manuscript was altered.
Archive curation changed only the publication subset and the comment described
above; private originals and their historical evidence remain unchanged. Original member identities and renamed archive mappings are in
`docs/origins.tsv`; complete public inventory hashes are in `SHA256SUMS`.

Auxiliary attachment decision: YES for a documentary witness table; NO for
a sparse indexed-term file, because no exact later index is established.
The workspace editorial candidate is `data/a230543.txt`; its public
byte-identical reproducibility copy is `data/quadruples.txt`. A proposed later
OEIS description is "Carlo Corti, Table of n, D(n), D^2(n) and the diagonal
for indices 1 through 40". No editorial upload or entry change occurred.

CITATION.cff reserves v1.0, repository https://github.com/carcorti/A230543,
and intentional DOI placeholder 10.5281/zenodo.xxxxxxxx, consistently with
the manuscript. Release date is omitted because no release exists yet.
Private reviews, obsolete drafts, caches, redundant binary variants and
third-party full texts are excluded; acquisitions/limitations are documented.

The local preparation record and exact command logs remain outside the public
payload. Publication, DOI assignment and distributed-release verification
remain pending. Local pre-upload readiness grants no publication authority.
