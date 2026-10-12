/* Disposable white-box checks; not an independent mathematical oracle. */
#define main production_entry
#include "../src/a230543.c"
#undef main
int main(int argc, char **argv) {
    if(gcd64(6,4)!=2 || rho_step(2,1,7)!=5) return 14;
    if (argc == 2 && !strcmp(argv[1], "bounds")) {
        uint64_t xs[] = {0,1,2,3,4,CAP-1,CAP,UINT64_MAX-1,UINT64_MAX};
        for (size_t i=0;i<sizeof xs/sizeof xs[0];++i) {
            uint64_t r=isqrt64(xs[i]);
            if ((u128)r*r>xs[i] || (u128)(r+1)*(r+1)<=xs[i]) return 1;
        }
        uint64_t x=0;
        if (!dec64("18446744073709551615",&x)||x!=UINT64_MAX ||
            dec64("18446744073709551616",&x)||dec64("-1",&x)||dec64("",&x)) return 2;
        Config c={.start=2,.end=CAP,.block=MIN_BLOCK,.group=UINT64_MAX,.threads=8};
        if(num_segments(&c)!=1) return 3;
        uint64_t lo,hi;seg_bounds(&c,0,&lo,&hi);
        if(lo!=2||hi!=CAP) return 4;
        c.group=1;
        uint64_t count=num_segments(&c);
        if(count!=((CAP-2)/MIN_BLOCK+1)||count>=(UINT64_C(1)<<40)) return 5;
        seg_bounds(&c,count-1,&lo,&hi);
        if(hi!=CAP || (u128)(lo-1)+MIN_BLOCK<CAP) return 6;
        char name[32];state_name(name,(UINT64_C(1)<<40)-1,true);
        if(strcmp(name,"sffffffffff.sha256")) return 7;
        char formatted[40];fmt128((u128)-1,formatted);
        if(strcmp(formatted,"340282366920938463463374607431768211455")) return 8;
        if(sizeof(Hit)!=32) return 9;
        atomic_store(&stopped,1);
        bool fallback=false;u128 d;
        if(derivative64(10403,&d,&fallback)) return 10;
        puts("bounds/absence/stop PASS");return 0;
    }
    char line[128];
    while(fgets(line,sizeof line,stdin)) {
        line[strcspn(line,"\n")]=0;uint64_t n;
        if(!dec64(line,&n)||n<1) return 11;
        bool fallback=false;u128 d;
        if(!derivative64(n,&d,&fallback)) return 12;
        char value[40];fmt128(d,value);
        printf("%" PRIu64 "\t%d\t%s\t%d\n",n,prime64(n)?1:0,value,fallback?1:0);
    }
    return ferror(stdin)?13:0;
}
