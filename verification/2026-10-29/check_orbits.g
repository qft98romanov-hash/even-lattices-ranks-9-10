# Independent exact GAP verification of the E8/3E8 glue-orbit calculation.
# Run from this directory after: python3 export_gap.py
# Command: gap -q -b -T check_orbits.g
#
# No original Python verifier is imported, and no stored vector/orbit lists
# are used. The only numerical input is the integer E8 Gram matrix.
# Norms always mean squared lengths. All enumeration bounds are rational.
# Matrices act on ROW vectors from the right; their permutations act on
# class indices 1 + Sum(x_i * 3^(i-1)).

Read("data/gap_inputs.g");

AuditCheck := function(test, message)
    if not test then
        Print("GAP_ORBIT_CHECK_FAIL: ", message, "\n");
        QUIT_GAP(1);
    fi;
end;

AuditClassId := function(v)
    return 1 + Sum([1..Length(v)], i -> (v[i] mod 3) * 3^(i-1));
end;

AuditCoordinates := function(id)
    local x, v, i;
    x := id-1; v := [];
    for i in [1..8] do
        Add(v, x mod 3);
        x := QuoInt(x, 3);
    od;
    return v;
end;

# LDL^T decomposition G = lower * diag(d) * lower^T over the rationals.
# For a row x, the norm is Sum_i d_i (x_i + Sum_{j>i} lower[j][i] x_j)^2.
AuditLDL := function(g)
    local n, lower, d, i, j, k, t;
    n := Length(g); lower := IdentityMat(n); d := [];
    for i in [1..n] do
        t := g[i][i];
        for k in [1..i-1] do t := t - lower[i][k]^2 * d[k]; od;
        AuditCheck(t > 0, "positive definiteness");
        d[i] := t;
        for j in [i+1..n] do
            t := g[j][i];
            for k in [1..i-1] do
                t := t - lower[j][k]*d[k]*lower[i][k];
            od;
            lower[j][i] := t/d[i];
        od;
    od;
    AuditCheck(lower*DiagonalMat(d)*TransposedMat(lower)=g,"LDL identity");
    return [lower,d];
end;

# Enumerate the entire ellipsoid x*G*x^T <= bound by reverse recursion.
# The integer interval is intentionally wider than needed; exact rational
# comparisons remove all excess candidates. No square-root rounding is used.
AuditEnumerate := function(g, bound)
    local n, ld, lower, d, x, minima, counts, roots, nodes, visit;
    n := Length(g); ld := AuditLDL(g); lower := ld[1]; d := ld[2];
    x := List([1..n], i->0);
    minima := List([1..3^n], i->fail);
    counts := List([0..bound], i->0); roots := []; nodes := 0;
    visit := function(i, partial)
        local s, j, radius, lo, hi, z, next, id, actual;
        nodes := nodes+1;
        if i=0 then
            actual := x*g*x;
            AuditCheck(actual=partial and IsInt(actual),"enumerated norm identity");
            id := AuditClassId(x);
            if minima[id]=fail or actual < minima[id] then minima[id]:=actual; fi;
            counts[actual+1] := counts[actual+1]+1;
            if actual=2 then Add(roots,ShallowCopy(x)); fi;
            return;
        fi;
        s := 0;
        for j in [i+1..n] do s := s+lower[j][i]*x[j]; od;
        radius := RootInt(Int((bound-partial)/d[i]))+1;
        lo := Int(-s)-radius-1;
        hi := Int(-s)+radius+1;
        for z in [lo..hi] do
            next := partial+d[i]*(z+s)^2;
            if next <= bound then
                x[i]:=z; visit(i-1,next);
            fi;
        od;
    end;
    visit(n,0);
    return rec(minima:=minima,counts:=counts,roots:=roots,nodes:=nodes);
end;

# For a root r of norm 2, x maps to x-(x*G*r^T)*r.
AuditReflection := function(g,r)
    local u, t, i, j, n;
    n:=Length(g); u:=g*r; t:=IdentityMat(n);
    AuditCheck(r*g*r=2,"root norm");
    for i in [1..n] do
        for j in [1..n] do t[i][j]:=t[i][j]-u[i]*r[j]; od;
    od;
    AuditCheck(t*g*TransposedMat(t)=g,"reflection isometry");
    AuditCheck(t*t=IdentityMat(n),"reflection involution");
    return t;
end;

start := Runtime();
AuditCheck(E8Gram=TransposedMat(E8Gram),"symmetric Gram");
AuditCheck(DeterminantMat(E8Gram)=1,"unimodular E8 Gram");
Print("GAP version: ",GAPInfo.Version,"\n");
Print("Input SHA256: ",E8InputSHA256,"\n");
Print("Enumerating E8 vectors of squared norm at most 8 exactly...\n");
enum := AuditEnumerate(E8Gram,8);
AuditCheck(ForAll(enum.minima,m->m<>fail),"all 6561 residue classes covered");
distribution := List([0,2,4,6,8],m->[m,Number(enum.minima,x->x=m)]);
Print("Class minimum distribution: ",distribution,"\n");
AuditCheck(distribution=[[0,1],[2,240],[4,2160],[6,2240],[8,1920]],"class minima distribution");
AuditCheck(enum.counts=[1,0,240,0,2160,0,6720,0,17520],"complete norm<=8 shells");

# The eight basis vectors are roots. Generate their reflection action, then
# check that reflections in EVERY one of the 240 enumerated roots belong to
# the generated group. Thus the computed group is the full root-reflection
# image, not an unverified subgroup chosen for a favorable orbit count.
classes := List([1..6561],AuditCoordinates);
AuditPermutation := function(t)
    return PermList(List(classes,v->AuditClassId(v*t)));
end;
basis := IdentityMat(8);
matrices := List(basis,r->AuditReflection(E8Gram,r));
perms := List(matrices,AuditPermutation);
AuditCheck(ForAll(perms,p->p<>fail),"class actions are permutations");
W := Group(perms);
order := Size(W);
Print("Reflection group order on E8/3E8: ",order,"\n");
AuditCheck(order=696729600,"Weyl E8 image order");
positiveRoots := Filtered(enum.roots,r->First(r,x->x<>0)>0);
AuditCheck(Length(positiveRoots)=120,"root sign pairs");
for r in positiveRoots do
    t := AuditReflection(E8Gram,r);
    p := AuditPermutation(t);
    AuditCheck(p in W,"all root reflections are in the generated group");
od;
orbits := OrbitsDomain(W,[1..6561]);
orbitSizes := SortedList(List(orbits,Length));
AuditCheck(orbitSizes=[1,240,1920,2160,2240],"full residue-class orbit sizes");
AuditCheck(ForAll(orbits,o->Length(Set(List(o,id->enum.minima[id])))=1),"norm minima invariant on all orbits");

deep := Filtered([1..6561],id->enum.minima[id]=8);
a := deep[1]; av := classes[a];
admissible := Filtered(deep,b->enum.minima[AuditClassId(av-classes[b])]=8);
AuditCheck(Length(admissible)=561,"admissible deep partners");
stab := Stabilizer(W,a);
stabOrder := Size(stab);
AuditCheck(order=Length(deep)*stabOrder,"orbit-stabilizer identity");
AuditCheck(ForAll(GeneratorsOfGroup(stab),p->Set(OnTuples(admissible,p))=Set(admissible)),"admissible set preserved by stabilizer");
pairOrbits := OrbitsDomain(stab,admissible);
pairSizes := SortedList(List(pairOrbits,Length));
AuditCheck(pairSizes=[1,560],"two deep-pair stabilizer orbits");
singleton := First(pairOrbits,o->Length(o)=1)[1];
AuditCheck(singleton=AuditClassId(-av),"singleton partner is minus a");
Print("Stabilizer order: ",stabOrder,"\n");
Print("Deep partner orbit sizes: ",pairSizes,"\n");
elapsed := Runtime()-start;
reportStream := OutputTextFile("results/gap_orbits.json",false);
SetPrintFormattingStatus(reportStream,false);
PrintTo(reportStream,
    "{\n  \"status\": \"PASS\",\n  \"gap_version\": \"",GAPInfo.Version,"\",\n",
    "  \"scope\": \"Independent finite E8 glue-orbit checks; not the global rank-ten classification\",\n",
    "  \"input_sha256\": \"",E8InputSHA256,"\",\n",
    "  \"norm_bound\": 8,\n  \"enumerated_vectors\": ",Sum(enum.counts),",\n",
    "  \"enumeration_nodes\": ",enum.nodes,",\n",
    "  \"shell_counts_by_norm_0_to_8\": ",enum.counts,",\n",
    "  \"class_minimum_distribution\": ",distribution,",\n",
    "  \"reflection_group_order\": ",order,",\n",
    "  \"all_120_root_reflections_checked\": true,\n",
    "  \"class_orbit_sizes\": ",orbitSizes,",\n",
    "  \"fixed_deep_class_coordinates\": ",av,",\n",
    "  \"admissible_partners\": ",Length(admissible),",\n",
    "  \"stabilizer_order\": ",stabOrder,",\n",
    "  \"partner_orbit_sizes\": ",pairSizes,",\n",
    "  \"singleton_is_negative_class\": true,\n",
    "  \"cpu_milliseconds\": ",elapsed,"\n}\n");
CloseStream(reportStream);
Print("GAP_ORBIT_CHECK_PASS\n");
QUIT_GAP(0);
