#!/usr/bin/env python3
"""Reconstructed public checks of frozen A230543 evidence; no init/next.

The independent oracle check.py is unchanged. This runner reconstructs the
packaging checks from the original reports identified in docs/origins.tsv.
Archive consistency, shared-backend replay and independent arithmetic retain
their distinct meanings. All build/extraction output goes to temporary roots.
"""
import argparse
import csv
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode = True
import check as o

ROOT = Path(__file__).resolve().parents[1]
require = o.require
o.derivative = lru_cache(maxsize=250000)(o.derivative)
D = o.derivative


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(args, **kwargs):
    p = subprocess.run(list(map(str, args)), capture_output=True, text=True,
                       timeout=120, **kwargs)
    require(p.returncode == 0, f'command failed: {args}: {p.stderr[-2000:]}')
    return p.stdout


def integrity():
    manifest = ROOT/'SHA256SUMS'
    expected = {}
    for line in manifest.read_text().splitlines():
        digest, name = line.split('  ', 1)
        o.digest(digest)
        require(name not in expected and not Path(name).is_absolute() and
                '..' not in Path(name).parts, 'checksum path grammar')
        expected[name] = digest
    expected_dirs = {str(parent) for name in expected
                     for parent in Path(name).parents if parent != Path('.')}
    actual = set()
    actual_dirs = set()
    metadata = ROOT/'.git'
    if metadata.exists() or metadata.is_symlink():
        require(metadata.is_dir() and not metadata.is_symlink(),
                'root .git metadata must be a real directory')
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if rel.parts[0] == '.git':
            continue  # provider metadata only at root; never arbitrary payload
        require(not path.is_symlink(), 'package symlink')
        if path.is_dir():
            actual_dirs.add(str(rel))
        else:
            require(path.is_file(), 'nonregular package entry')
            if str(rel) != 'SHA256SUMS':
                actual.add(str(rel))
    require(actual == set(expected), 'missing or unexpected package files')
    require(actual_dirs == expected_dirs, 'missing or unexpected package directories')
    for name, digest in expected.items():
        require(sha(ROOT/name) == digest, 'changed package file: '+name)
    return len(expected)+1


def unpack(name, destination):
    origins = list(csv.DictReader((ROOT/'docs/origins.tsv').open(), delimiter='\t'))
    wanted = {r['public_artifact'].split('::', 1)[1]: r for r in origins
              if r['public_artifact'].startswith(name+'::')}
    seen = set()
    with tarfile.open(ROOT/name, 'r:gz') as archive:
        for member in archive.getmembers():
            rel = Path(member.name)
            require(member.isfile() and not rel.is_absolute() and
                    '..' not in rel.parts and member.name not in seen and
                    member.name in wanted, 'unsafe or unexpected archive member')
            row = wanted[member.name]
            require(member.size == int(row['bytes']) and member.size <= 2000000,
                    'archive member size')
            data = archive.extractfile(member).read()
            require(hashlib.sha256(data).hexdigest() == row['sha256'], 'member digest')
            path = destination/rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(member.mode & 0o755)
            seen.add(member.name)
    require(seen == set(wanted) and seen, 'missing archive member')


def factor(n):
    result = {}
    p = 2
    while p <= n//p:
        while n % p == 0:
            result[p] = result.get(p, 0)+1
            n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        result[n] = result.get(n, 0)+1
    return result


def classes(studies):
    rows = studies['r13']['all_classes']
    require([r['i'] for r in rows] == list(range(1, 41)), 'class index domain')
    for row in rows:
        w = tuple(row['witness']); g = math.gcd(*w)
        require(o.witness(w[0]) == w and g == row['gcd'], 'positive arithmetic')
        m,u,v,r = (x//g for x in w)
        require([m,u,v,r] == row['normalized'], 'normalized form')
        rate = Fraction(u-D(m), m)
        require(rate == Fraction(row['lambda']) == Fraction(D(g), g) and
                D(u)+rate*u == v and m*m+u*u+v*v == r*r, 'shape rate/chain')
        f = factor(rate.denominator)
        require(all(e == 1 for e in f.values()), 'squarefree rate denominator')
        residues = {p: rate.numerator*pow(rate.denominator//p, -1, p) % p for p in f}
        alpha = sum((Fraction(e,p) for p,e in residues.items()), Fraction(0))
        core = math.prod(p**e for p,e in residues.items()); k = rate-alpha
        require(k.denominator == 1 and k >= 0 and core == row['core'] and
                int(k) == row['free_prime_count'], 'modular scale decomposition')
        params = row['prime_parameters']
        require(len(params) == k and all(factor(p) == {p:1} for p in params) and
                core*math.prod(p**p for p in params) == g, 'scale reconstruction')
    require(len({tuple(r['normalized']) for r in rows}) == 10 and
            [r['i'] for r in rows if r['free_prime_count']==0] == [2,8,11,28,36,37],
            'shape inventory')
    require([sum(r['free_prime_count']==k for r in rows) for k in (4,3,2,1)] ==
            [17,12,3,2], 'infinite form counts')
    return rows


def data_bytes(rows):
    b = (''.join(f"{r['i']} {r['witness'][0]}\n" for r in rows)+'\n').encode()
    w = ('i\tn\tD\tD2\troot\n'+''.join('\t'.join(map(str,[r['i'],*r['witness']]))+
         '\n' for r in rows)+'\n').encode()
    f = 'i\tm\tu\tv\tr\tgcd\tlambda\tcore\tk\tparameters\n'
    f += ''.join('\t'.join(map(str,[r['i'],*r['normalized'],r['gcd'],r['lambda'],
              r['core'],r['free_prime_count'],','.join(map(str,r['prime_parameters'])) or '-']))+
              '\n' for r in rows)
    return {'b230543.txt':b, 'witnesses.tsv':w, 'forms.tsv':f.encode()}


def manuscript(rows):
    tex = (ROOT/'paper/A230543.tex').read_text()
    tables = re.findall(r'\\begin\{longtable\}.*?\\end\{longtable\}', tex, re.S)
    require(len(tables)==2, 'two full manuscript tables')
    wr = re.findall(r'^(\d+) & (\d+) & (\d+) & (\d+) & (\d+)\\\\',tables[1], re.M)
    require([tuple(map(int,r)) for r in wr] == [(r['i'],*r['witness']) for r in rows],
            'manuscript witness alignment')
    pr = re.findall(r'^(\d+) & (\d+) & \$(.*?)\$ & (\d+) & \$(.*?)\$\\\\',tables[0],re.M)
    expected=[]
    for r in rows:
        k=r['free_prime_count']; label='S_{'+str(r['i'])+'}' if k==0 else 'H' if k==1 else 'F_'+str(k)
        params=r'\varnothing' if not r['prime_parameters'] else '('+','.join(map(str,r['prime_parameters']))+')'
        expected.append((str(r['i']),str(r['witness'][0]),label,str(r['gcd']),params))
    require(pr == expected, 'manuscript class alignment')
    require(not re.search(r'\\(?:input|include|bibliography)\{', tex) and
            'https://doi.org/10.5281/zenodo.23311392' in tex,
            'monolithic manuscript with designated concept DOI')
    pdf = ROOT/'paper/A230543.pdf'
    raw = pdf.read_bytes()
    require(raw.startswith(b'%PDF-') and b'%%EOF' in raw[-1024:], 'PDF framing')
    info = command(['pdfinfo', pdf])
    title = re.search(r'\\title\{([^{}]+)\}', tex).group(1)
    require(re.search(r'^Author:\s+Carlo Corti\s*$', info, re.M) is not None and
            re.search(r'^Title:\s+'+re.escape(title)+r'\s*$', info, re.M) is not None,
            'PDF author/title metadata')
    text = command(['pdftotext', '-layout', pdf, '-'])
    numbers = set(re.findall(r'\b\d+\b', text))
    require(all(str(value) in numbers for row in rows for value in row['witness']) and
            '10.5281/zenodo.23311392' in text and 'Carlo Corti' in text,
            'PDF scientific witnesses and concept DOI')
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',tex)
    bib=re.findall(r'\\bibitem\{([^}]+)\}',tex)
    cites=[c.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',tex) for c in group.split(',')]
    require(len(labels)==len(set(labels)) and set(refs)<=set(labels) and
            len(bib)==len(set(bib)) and set(cites)==set(bib), 'TeX reference closure')


def finite(studies):
    import sympy
    require(sympy.__version__ == '1.12', 'SymPy 1.12 required for checked CAS backend')
    def cas(n):
        return sum(int(e)*(n//int(p)) for p,e in sympy.factorint(n).items()) if n>1 else 0
    hits=[]
    for rate in range(1,9):
        for m in range(1,20001):
            u=D(m)+rate*m; v=D(u)+rate*u; r=math.isqrt(m*m+u*u+v*v)
            if u>0 and v>0 and r*r==m*m+u*u+v*v:
                require(u==cas(m)+rate*m and v==cas(u)+rate*u, 'CAS positive rectangle')
                hits.append((rate,m,u,v,r))
    retained=[(x['lambda'],*x['chain'],x['root']) for x in studies['intake']['rectangle']['hits']]
    require(hits==retained and len(hits)==15, '160000-pair rectangle')
    primes=[p for p in range(2,1001) if factor(p)=={p:1}]
    records=studies['pattern']['records']
    require([r['p'] for r in records]==primes and len(primes)==168,'finite prime domain')
    positives=[]
    for row in records:
        p=row['p']; n=187*p**4; u=D(n);v=D(u);q=n*n+u*u+v*v;r=math.isqrt(q)
        require([n,u,v,r]==[row['n'],row['D'],row['D2'],row['root_floor']] and
                bool(row['accept'])==(r*r==q),'prime pattern record')
        cp=28*p+748
        require(u==p**3*cp and v==p**2*(p*D(cp)+3*cp),'shared-prime pattern identity')
        if row['accept']:positives.append(p)
    require(positives==[71],'finite prime positives')
    print('PASS rectangle: 160000 pairs, 15 positives; CAS positives; prime screen: 168/1',flush=True)


def coverage(runs, build, rows):
    tags=('first','1E10','11a','11b','11c','13'); next_low=408918817
    collected=[];segments=0; timings=[]
    for name in ('time.tsv','t11.tsv','t13.tsv'):
        timings += [r.split() for r in (runs/name).read_text().splitlines()]
    index=0
    for tag in tags:
        run=runs/tag;identity=sha(run/'run.cfg');cfg=o.config((run/'run.cfg').read_bytes())
        require(cfg['start']==next_low and cfg['threads']==8,'campaign join/threads')
        for key,path in [('source_sha','a230543.c'),('makefile_sha','Makefile'),('binary_sha','a230543')]:
            require(cfg[key]==sha(build/path),'historical run identity')
        found=o.rows(run/'hits.tsv',True,identity);o.sealed_coverage(run,cfg,identity,found)
        for state in o.lines((run/'manifest.tsv').read_bytes())[2:]:
            s=state.split('\t');t=timings[index];index+=1;segments+=1
            require(len(t)==6 and t[-1]=='0' and
                    abs(Decimal(t[1])-Decimal(s[4])/10**9)<Decimal('0.1'),'seal timing alignment')
        # Original executable plus original adjacent C/Makefile, never a rebuilt
        # executable substituted into historical identities. No next/init.
        output=command([build/'a230543','verify',run])
        require('COMPLETE' in output and 'INCOMPLETE' not in output,'original native replay')
        collected+=found;next_low=cfg['end']+1
    require(next_low==130000000001 and segments==index==len(timings)==22 and
            collected==[tuple(r['witness']) for r in rows[22:]],'full campaign aggregate')
    total=sum((Decimal(t[1]) for t in timings),Decimal(0))
    require(total==Decimal('62021.68'),'raw wall sum')
    print('PASS coverage: 6 runs, 22 seals, 129591081184 inputs, 18 positives; native replay',flush=True)


def windows(studies):
    union={}
    for tag in ('r1','r2','r11a','r11b','r11c','r13'):
        d=studies[tag];ws=[d['neighborhood']] if tag=='r1' else d['windows']
        for w in ws:
            low,high=w['actual_bounds'];records=w['records']
            require([r[0] for r in records]==list(range(low,high+1)) and
                    len(records)==w['actual_count'],'window identity')
            for row in records:
                n,a,b,q,r,accept=row;da=D(n);db=D(da);square=n*n+da*da+db*db
                require([a,b,q,r,bool(accept)]==[da,db,square,math.isqrt(square),
                        da>0 and db>0 and math.isqrt(square)**2==square],'window arithmetic')
                require(n not in union or union[n]==row,'window overlap')
                union[n]=row
    require(len(union)==10763 and sum(bool(r[-1]) for r in union.values())==11,'window union')
    print('PASS campaign windows: 10763 distinct inputs, 11 positives',flush=True)
    # Original diagnostic union: small interval, two post-prefix windows,
    # 30 fixtures (including a wide unindexed witness) and CAP neighbors.
    inputs=set(range(2,32770))
    for rec in studies['diagnostics']['checks']:
        lo,hi=rec['domain'];inputs.update(range(lo,hi+1))
    fixtures=o.rows(ROOT/'validation/reference.tsv')
    inputs.update(r[0] for r in fixtures);inputs.update((10**16-1,10**16))
    found=[w for n in sorted(inputs) if (w:=o.witness(n))]
    require(len(inputs)==33827 and len(found)==30 and set(found)==set(fixtures),'diagnostic union')
    print('PASS separate diagnostic union: 33827 distinct inputs, 30 positives',flush=True)


def backend(temp):
    import sympy
    versions={'python':sys.version.split()[0], 'sympy':sympy.__version__,
              'gcc':command(['gcc','-dumpfullversion']).strip(),
              'gmp':command(['pkg-config','--modversion','gmp']).strip(),
              'openssl':command(['pkg-config','--modversion','openssl']).strip()}
    require(versions['gmp']=='6.3.0' and versions['openssl']=='3.0.13',
            'native replay requires tested GMP 6.3.0/OpenSSL 3.0.13 environment')
    flags=['-O2','-std=c17','-Wall','-Wextra','-Werror','-fopenmp']
    for name,extra in [('probe',[]),('fallback',['-DA230543_FORCE_FALLBACK'])]:
        command(['gcc',*flags,*extra,ROOT/'validation/backend_probe.c','-o',temp/name,'-lgmp','-lcrypto'])
    command([temp/'probe','bounds'])
    bases=(2,325,9375,28178,450775,9780504,1795265022);divisors=set()
    for b in bases:
        ds=[1]
        for p,e in factor(b).items():ds=[d*p**j for d in ds for j in range(e+1)]
        divisors.update(d for d in ds if d>=2)
    rng=random.Random(230543)
    corpus={1,2,3,4,97,101,10403,3215031751,341550071728321,3825123056546413051,
            2**64-1,2**64-59,265000000000000000}
    corpus.update(rng.randrange(2,10**12) for _ in range(128))
    corpus.update(x for n in (2,101,1009,10007) for x in (n*n,n**3) if x<2**64)
    inputs=sorted(divisors|corpus)
    output=command([temp/'probe'],input=''.join(str(n)+'\n' for n in inputs))
    parsed=[tuple(map(int,r.split())) for r in output.splitlines()]
    require([r[0] for r in parsed]==inputs,'native corpus complete')
    for n,prime,d,fb in parsed:
        fs=sympy.factorint(n);expected=sum(int(e)*(n//int(p)) for p,e in fs.items())
        require(prime==int(sympy.isprime(n)) and d==expected,'independent CAS backend check')
        if n in divisors:
            require(prime==int(factor(n)=={n:1}) and d==D(n),'trial-division base divisor')
    require(len(divisors)==55 and sum(factor(n)=={n:1} for n in divisors)==9,'55 exceptional operands')
    forced=command([temp/'fallback'],input='10403\n10201\n1000036000099\n')
    rows=[tuple(map(int,r.split())) for r in forced.splitlines()]
    require([r[0] for r in rows]==[10403,10201,1000036000099],'forced corpus complete')
    for n,prime,d,fb in rows:
        require(d==D(n) and fb==1 and prime==0,'forced fallback exactness')
    public=temp/'public';public.mkdir()
    for name in ('a230543.c','Makefile'):shutil.copyfile(ROOT/'src'/name,public/name)
    command(['make','-C',public])  # bounded build only; output never enters package
    print('PASS native bounds/CAS corpus/55 base divisors/forced fallback/public build',flush=True)
    return versions


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export',type=Path,help='write regenerated b-file, witnesses and forms to a NEW directory')
    args=parser.parse_args()
    if args.export:
        require(not args.export.exists(),'export destination must not exist')
    count=integrity();print('PASS package inventory/checksums:',count,'files',flush=True)
    with tempfile.TemporaryDirectory(prefix='a230543-') as td:
        temp=Path(td)
        for name in ('build','runs','studies','tests'):
            unpack('evidence/'+name+'.tar.gz',temp/name)
        studies={p.stem:json.loads(p.read_text()) for p in (temp/'studies').glob('*.json')}
        rows=classes(studies);generated=data_bytes(rows)
        for name,data in generated.items():require((ROOT/'data'/name).read_bytes()==data,'generated data: '+name)
        command([sys.executable,ROOT/'validation/check.py'])
        raw=(ROOT/'data/quadruples.txt').read_bytes()
        require(raw.endswith(b'\n\n') and not raw.endswith(b'\n\n\n'),'documentary framing')
        q=[tuple(map(int,r.split())) for r in raw.decode().splitlines() if r and not r.startswith('#')]
        require(q==[(r['i'],*r['witness']) for r in rows],'documentary witnesses')
        manuscript(rows)
        require(o.witness(512)==(512,2304,10752,11008),'known-family mapping replay')
        upper=(244140625000,1098632812500,5126953125000,5249023437500)
        require(o.witness(upper[0])==upper and upper[0]==2*math.prod(p**p for p in (2,5,5,5))
                and upper[0] not in [r['witness'][0] for r in rows],'unindexed exact upper bound')
        cap=10**16;u1=cap*(cap.bit_length()-1)//2;u2=u1*(u1.bit_length()-1)//2
        require((u1,u2)==(265000000000000000,7552500000000000000) and
                (cap*cap+u1*u1+u2*u2).bit_length()==126,'numeric envelope')
        print('PASS 40 witnesses, 10 forms, TeX tables, inherited prefix, endpoint and capacity',flush=True)
        versions=backend(temp)
        coverage(temp/'runs/runs',temp/'build/src',rows)
        finite(studies)
        windows(studies)
        if args.export:
            args.export.mkdir(parents=True)
            for name,data in generated.items():(args.export/name).write_bytes(data)
        print(json.dumps({'status':'PASS','dependencies':versions,'package_files':count,
              'terms':40,'first_unresolved_index':41,'lower_bound':130000000000,
              'upper_bound':upper[0],'full_negative_independence':False,
              'limitations':'Accepted 22-row baseline inherited; full native negative coverage conditional; archival development tests not rerun; no official init/next or PDF generation.'},sort_keys=True),flush=True)


if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError,subprocess.SubprocessError,tarfile.TarError) as e:
        print('FAIL:',e,file=sys.stderr);raise SystemExit(1)
