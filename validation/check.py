#!/usr/bin/env python3
"""Independent integer oracle. Membership checks do not prove range coverage.

Trial division is deliberately independent of the C sieve, MR/rho and GMP.
For completeness checks, --low/--high require a sealed run to END, then
explicitly enumerate a bounded interval. Read a static local run directory;
hashes detect accidental drift, not an adversarial rewrite of all artifacts.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAP = 10**16
PREFIX_SHA = '03efb10156a20d0f04fc7b1ff6f2f6de49b491ae8f7c88482475d61a964e5353'
CANONICAL_SHA = 'c5faac2e7453b1295c07129005a3b57880ab2a59066c557a98c02da92d6b95b7'
WITNESSES_SHA = '4803ca454d7e863ac104d66b75b0c23c8306eb125939c359f5ec16079456c16e'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def derivative(n):
    if n < 2:
        return 0
    remaining, answer, p = n, 0, 2
    while p <= remaining // p:
        exponent = 0
        while remaining % p == 0:
            remaining //= p
            exponent += 1
        answer += exponent * (n // p)
        p = 3 if p == 2 else p + 2
    if remaining > 1:
        answer += n // remaining
    return answer

def witness(n):
    a = derivative(n)
    b = derivative(a)
    square = n*n + a*a + b*b
    r = math.isqrt(square)
    return (n, a, b, r) if a > 0 and b > 0 and r*r == square else None

def lines(raw):
    require(raw.endswith(b'\n') and b'\r' not in raw and b'\0' not in raw, 'TSV framing')
    return raw.decode('ascii').split('\n')[:-1]

def number(text):
    require(text.isascii() and text.isdecimal(), 'integer grammar')
    value = int(text)
    require(value < 2**64, 'integer range')
    return value

def digest(text):
    require(len(text) == 64 and all(c in '0123456789abcdef' for c in text), 'digest grammar')
    return text

def parse_rows(records):
    result = []
    for line in records:
        fields = line.split('\t')
        require(len(fields) == 4, 'row grammar')
        row = tuple(map(number, fields))
        require(2 <= row[0] <= CAP and all(x > 0 for x in row), 'row domain')
        require(not result or result[-1][0] < row[0], 'row order')
        result.append(row)
    return result

def rows(path, header=False, identity=None):
    records = lines(path.read_bytes())
    if header:
        if identity is None:
            require(len(records) >= 2 and records[0].startswith('A230543-HITS-1\tcfg_sha='), 'hits identity')
            identity = digest(records[0].removeprefix('A230543-HITS-1\tcfg_sha='))
        require(len(records) >= 2 and records[0] == 'A230543-HITS-1\tcfg_sha='+identity, 'hits identity')
        require(records[1] == 'n\tx1\tx2\troot', 'hits columns')
        records = records[2:]
    return parse_rows(records)

def config(raw):
    records = lines(raw)
    keys = ('start', 'end', 'block', 'group', 'threads', 'source_sha', 'makefile_sha', 'binary_sha')
    require(len(records) == 9 and records[0] == 'A230543-CFG-1', 'config schema')
    fields = {}
    for key, record in zip(keys, records[1:]):
        parts = record.split('\t')
        require(len(parts) == 2 and parts[0] == key, 'config field')
        fields[key] = number(parts[1]) if key in keys[:5] else digest(parts[1])
    require(2 <= fields['start'] <= fields['end'] <= CAP and
            16384 <= fields['block'] <= 1048576 and
            fields['block'] & (fields['block']-1) == 0 and
            fields['group'] > 0 and 1 <= fields['threads'] <= 8, 'config domain')
    return fields

def sealed_coverage(run, fields, identity, found):
    records = lines((run/'manifest.tsv').read_bytes())
    require(len(records) >= 2 and records[0] == 'A230543-MANIFEST-1\tcfg_sha='+identity,
            'manifest identity')
    require(records[1] == 'id\tlow\thigh\tstate_sha\telapsed_ns\thits', 'manifest columns')
    width = fields['block'] * fields['group']
    count = (fields['end']-fields['start']+width)//width
    require(len(records)-2 == count, 'native run not sealed to END')
    collected = []
    for k, record in enumerate(records[2:]):
        parts = record.split('\t')
        require(len(parts) == 6 and parts[0] == format(k, '010x'), 'manifest segment ID')
        low = fields['start'] + k*width
        high = min(low+width-1, fields['end'])
        require(number(parts[1]) == low and number(parts[2]) == high, 'manifest bounds')
        sha, elapsed, hits = digest(parts[3]), number(parts[4]), number(parts[5])
        name = 's'+parts[0]
        raw = (run/(name+'.tsv')).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == sha, 'segment hash')
        require((run/(name+'.sha256')).read_bytes() == (sha+'\n').encode('ascii'), 'segment seal')
        segment = lines(raw)
        require(len(segment) >= 9 and segment[0] == 'A230543-SEG-2', 'segment schema')
        keys = ('cfg_sha', 'id', 'low', 'high', 'frontier', 'elapsed_ns', 'hits')
        values = {}
        for key, line in zip(keys, segment[1:8]):
            pair = line.split('\t')
            require(len(pair) == 2 and pair[0] == key, 'segment field')
            values[key] = pair[1]
        require(values['cfg_sha'] == identity and values['id'] == parts[0], 'segment identity')
        require(number(values['low']) == low and number(values['high']) == high and
                number(values['frontier']) == high, 'segment not complete')
        require(number(values['elapsed_ns']) == elapsed and number(values['hits']) == hits,
                'segment/manifest metadata')
        footer = segment[-1].split('\t')
        require(len(footer) == 2 and footer[0] == 'state_sha', 'segment footer')
        prefix = raw[:raw.rfind(b'\n', 0, len(raw)-1)+1]
        require(hashlib.sha256(prefix).hexdigest() == digest(footer[1]), 'segment state digest')
        witnesses = parse_rows(segment[8:-1])
        require(len(witnesses) == hits and all(low <= row[0] <= high for row in witnesses),
                'segment witnesses')
        collected.extend(witnesses)
    require(collected == found, 'sealed/aggregate witnesses disagree')

def indexed_prefix(raw):
    """Strict canonical b-file grammar, contiguous indices and increasing n."""
    require(raw.endswith(b'\n\n') and not raw.endswith(b'\n\n\n') and
            b'\r' not in raw and b'\0' not in raw, 'b-file framing')
    result = []
    for record in raw[:-2].decode('ascii').split('\n'):
        parts = record.split(' ')
        require(len(parts) == 2, 'b-file row grammar')
        i,n = map(number, parts)
        require(i == len(result)+1 and 2 <= n <= CAP and
                (not result or n > result[-1][1]), 'b-file index/value order')
        result.append((i,n))
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path)
    parser.add_argument('--low', type=int)
    parser.add_argument('--high', type=int)
    args = parser.parse_args()
    raw = (ROOT/'data/history/prefix22.txt').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PREFIX_SHA, 'accepted prefix changed')
    known = indexed_prefix(raw)
    require(len(known) == 22 and [i for i, _ in known] == list(range(1, 23)), 'prefix indexing')
    canonical_raw = (ROOT/'data/b230543.txt').read_bytes()
    canonical = indexed_prefix(canonical_raw)
    require(hashlib.sha256(canonical_raw).hexdigest() == CANONICAL_SHA and
            len(canonical) == 40 and canonical[:22] == known, 'validated canonical prefix changed')
    witness_raw = (ROOT/'data/witnesses.tsv').read_bytes()
    require(hashlib.sha256(witness_raw).hexdigest() == WITNESSES_SHA and
            witness_raw.endswith(b'\n\n') and not witness_raw.endswith(b'\n\n\n'),
            'canonical witnesses identity/framing')
    witness_records = lines(witness_raw)
    require(witness_records[0] == 'i\tn\tD\tD2\troot' and witness_records[-1] == '',
            'canonical witness header')
    indexed_witnesses = []
    for record in witness_records[1:-1]:
        fields = record.split('\t')
        require(len(fields) == 5, 'indexed witness grammar')
        indexed_witnesses.append(tuple(map(number, fields)))
    require([(r[0],r[1]) for r in indexed_witnesses] == canonical, 'canonical witness indexing')
    for row in indexed_witnesses:
        require(witness(row[1]) == row[1:], 'independent canonical witness mismatch')
    fixtures = rows(ROOT/'validation/reference.tsv')
    require({n for _, n in known}.issubset({x[0] for x in fixtures}), 'prefix fixtures missing')
    for row in fixtures:
        require(witness(row[0]) == row, 'independent fixture mismatch: '+str(row[0]))
    result = {'status':'PASS', 'fixtures':len(fixtures), 'prefix_terms':len(known),
              'canonical_terms':len(canonical), 'canonical_sha256':CANONICAL_SHA,
              'method':'Python integer trial division and math.isqrt; no C backend',
              'coverage':'canonical/fixture membership only; contiguous ordering provenance is final campaign audit'}
    if args.run:
        cfg = (args.run/'run.cfg').read_bytes()
        fields = config(cfg)
        identity = hashlib.sha256(cfg).hexdigest()
        found = rows(args.run/'hits.tsv', True, identity)
        require(all(fields['start'] <= row[0] <= fields['end'] for row in found), 'hit outside run')
        for row in found:
            require(witness(row[0]) == row, 'independent hit mismatch')
        result['run_hits'] = len(found)
        result['coverage'] = 'run membership only; no completion claim'
        require((args.low is None) == (args.high is None), 'both interval bounds required')
        if args.low is not None:
            require(2 <= args.low <= args.high <= 10**10 and args.high-args.low < 40000, 'oracle interval budget')
            require(fields['start'] == args.low and fields['end'] == args.high, 'interval identity')
            sealed_coverage(args.run, fields, identity, found)
            expected = [r for n in range(args.low, args.high+1) if (r := witness(n))]
            require(found == expected, 'complete interval disagreement')
            result['coverage'] = [args.low, args.high]
            result['tested_inputs'] = args.high-args.low+1
            result['sealed_to_end'] = True
    else:
        require(args.low is None and args.high is None, 'interval needs --run')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
