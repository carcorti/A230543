# Frozen production CLI

Build with `make -C src`; the public source and Makefile are unchanged from
the executed campaign. The program binds an executable to adjacent
`a230543.c` and `Makefile` bytes, and checks those hashes against `run.cfg`.
A different compiler/runtime can change the binary hash even with identical
source. It must not be substituted into a recorded campaign configuration.

The supported commands are exactly:

```text
a230543 init DIR START END BLOCK GROUP THREADS
a230543 next DIR
a230543 status DIR
a230543 verify DIR
```

`init` creates a fresh immutable configuration; `next` performs at most one
operational segment and supports repetition of an interrupted internal block.
The input cap is 10^16, block is a power of two in [16384,1048576], group is a
positive uint64, and threads are in [1,8]. Capacity is not completed coverage.
Only sealed completed segments support aggregate coverage; a partial frontier
is not a completed segment. Do not alter configurations or identity metadata.

For historical replay, unpack `build.tar.gz` and `runs.tar.gz` into the same
fresh root and use its original `src/a230543 verify runs/13`, replacing 13 by
any of first, 1E10, 11a, 11b or 11c. The public runner already performs all six
checks safely in a temporary directory. The example assumes execution from
that unpacked root. `verify` recomputes positives and reads native state; it
never re-enumerates all recorded negatives.

The recorded initial campaign invocation was
`src/a230543 init runs/first 408918817 711541152 1048576 289 8`, followed by
`src/a230543 next runs/first`. The last configuration was
`src/a230543 init runs/13 100000000001 130000000000 1048576 5723 8`, with five
`next` calls. These are historical descriptions, not preparation commands.
All six exact configurations and continuation telemetry are in `runs.tar.gz`.
No production campaign should be launched as part of package inspection.
