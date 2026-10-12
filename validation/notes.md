# Validation methods and scope

`run.py` is a new, explicitly **reconstructed** public runner. It reconstructs
the retained audits using the original byte-preserved reports in
`evidence/studies.tar.gz`; it is not represented as the old workspace auditor.
`check.py`, `reference.tsv` and `backend_probe.c` are unchanged originals.
`docs/origins.tsv` identifies every copied source and archived member, including
original SHA-256. Source-column paths are historical workspace provenance,
not missing public runtime dependencies. `archive::member` names refer to
members within a supplied archive. All required live inputs are package-relative.

| Check | Type | Exact input and checked domain |
|---|---|---|
| Forty witnesses and thirty fixtures | Independent arithmetic | Trial division and `math.isqrt`; no C helpers |
| Primitive forms/rational rates | Independent arithmetic | All 40 rows, gcd normalization and reduced-residue scale decomposition |
| Finite seed rectangle | Independent arithmetic, independent CAS on positives | 160000 pairs, rate 1..8 and m 1..20000; 15 positives, SymPy 1.12 factorization of positives; negatives have one independent implementation |
| Prime pattern | Independent arithmetic | All 168 primes <=1000, including shared-prime cases; only p=71 positive |
| Campaign windows | Independent arithmetic | Fresh replay of original record domains: union 10763, 11 positives and 10752 negatives |
| Code-diagnostic union | Independent arithmetic | [2,32769], two post-prefix windows, 30 fixtures and CAP neighbors; union 33827, 30 positives and 33797 negatives |
| Seals and joins | Archive/state consistency | Six runs, 22 complete segments and 18 sorted appended positives; exact hash/config/frontier/aggregate alignment |
| Original native replay | Production shared backend | Exact original binary plus its original adjacent source/Makefile; six `verify` calls, positive recomputation only |
| C backend corpus and bounds | Independent CAS versus production backend | Seeded original finite corpus, SymPy primality/factorization and white-box checks |
| Vanishing-base operands | Independent trial arithmetic versus production backend | All 55 divisors >=2 of the seven bases, nine primes; no uint64-wide enumeration |
| Forced trial fallback | Production white-box plus independent arithmetic | 10403, 10201, 1000036000099; exact derivatives and fallback flags |
| Python normal / -O | Cross-mode shared implementation | Same public runner; optimization does not remove checks |
| Historical sanitizer, TSan, parallel and recovery tests | Report-only in this preparation | Original diagnostic sources, transcript records and retained states in `tests.tar.gz`; not newly rerun |

The runner regenerates the public b-file, witness table and primitive-form table
and compares **bytes**, including LF LF framing for the first two. The renamed
documentary table `quadruples.txt` is an unmodified copy of the workspace OEIS
witness attachment, not a sparse indexed-term file. Its index convention agrees
with the 40-row b-file and manuscript; table/header conversions are checked.
The unindexed upper witness 244140625000 is tested through the same F4 relation
that first reproduces the known n=512 case; it does not become a(41).

`studies.tar.gz` holds original reports under aliases r1/r2/r11a/r11b/r11c/r13,
intake, pattern, classes30, environment and diagnostics. Window duplicates are
reconciled by n and full record equality before counting their union. The source
reports remain historical; a fresh public replay does not rewrite their dates
or imply an independent full negative enumeration. Native completeness assumes
the reviewed C implementation, and baseline completeness is inherited.

`runs.tar.gz` contains the exact run configurations, segment states, seals,
aggregates and original time TSVs. Their columns are call label, elapsed seconds,
user seconds, system seconds, peak RSS KiB, and exit status. The manifest rows
supply segment ID, inclusive endpoints, state SHA-256, elapsed nanoseconds and
hit count. Segment/call order is checked across each phase; decimal precision
is preserved. Total continuation wall time is about 62022 s; the final phase is
about 15946 s with maximum recorded peak RSS 23536 KiB. Exact decimal timings
remain in the machine-readable archival records. Raw shell terminal streams
are not complete campaign telemetry; structured records provide the stated data.

`build.tar.gz` includes the exact historical source, Makefile and executable.
Public source/build copies are byte-identical; there is no normalization diff
or alternative production implementation. Format magic numbers such as SEG-2
are serialization schema identifiers, not lifecycle suffixes. The newly built
public executable is tested as a build result and is never attributed to the
historical campaign. Decompression and all build outputs are disposable.

`tests.tar.gz` preserves original intake/family/campaign-auditor sources, the
recorded development environment, finite developer-test sources and selected logs/states,
without artificial long-path stress trees, instrumented binaries or duplicate
code copies. Its driver/member names are archival aliases: use `origins.tsv`
to recover original paths when studying the historical harness. These records
are for evidence inspection, not an additional public execution interface.
Original transcripts can mention paths/tools from the development host;
they are historical provenance, not dependencies of `run.py`.

The manuscript's v1 reviews do not certify the exact revised v2. Reviewer
conversations and internal manuscript QA reports are private and not copied.
Internal code-review process records are excluded from the curated archive.
A reviewer-attribution comment in one historical regression driver was replaced
with a technical description; executable statements remain identical. Its
source-map row points to the curated workspace copy, and its digest binds the
actual public member. All other retained archived members preserve their bytes.
The inventory validator rejects unexpected files, empty directories, symlinks
and nonregular entries. Directory names are derived from checksummed file
parents; only a real root `.git/` directory is exempt as provider metadata.
No full-cap performance, global primitive-form classification, bibliographic
novelty, public upload or independently repeated full scan is inferred.
