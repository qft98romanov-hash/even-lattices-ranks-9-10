// Independent checks of the explicit lattices using Magma's lattice intrinsics.
// Run FROM THIS DIRECTORY: magma -b check_magma.m > results/magma_run.log 2>&1
// A successful run MUST end with ALL_MAGMA_EXPLICIT_CHECKS_PASS.
// These checks do not assert a global determinant lower bound or completeness
// of the rank-ten equality classification.  No expected minimum is assigned
// as a cached lattice attribute.  No Max bound or heuristic Prune is supplied.

SetQuitOnError(true);
load "data/lattices.m";
printf "INPUT_SHA256 %o\n", InputSHA256;
assert Matrices["G8"] eq 3 * Matrices["E8"];

Lattices := AssociativeArray();
for name in ["K9", "K10", "K10_alt", "E8"] do
    G := Matrices[name];
    n := Nrows(G);
    assert G eq Transpose(G);
    assert forall{i : i in [1..n] | IsEven(G[i,i])};
    // Exact Sylvester criterion; construction also checks positivity.
    assert forall{k : k in [1..n] | Determinant(Submatrix(G,1,1,k,k)) gt 0};
    L := LatticeWithGram(G);
    Lattices[name] := L;
    d := Determinant(L);
    m := Minimum(L : Proof := true);
    assert d eq ExpectedDet[name];
    assert m eq ExpectedMin[name];
    assert IsEven(L);
    assert IsIntegral(L);
    V := ShortestVectors(L : Proof := true);
    assert forall{v : v in V | Norm(v) eq m};
    // ShortestVectors returns exactly one vector from each pair {v,-v}.
    kissing := 2 * #V;
    assert kissing eq KissingNumber(L : Proof := true);
    bound := (name eq "E8") select 8 else 10;
    theta := ThetaSeries(L, bound : Proof := true);
    for kv in ExpectedShells[name] do
        assert Coefficient(theta, kv[1]) eq kv[2];
    end for;
    printf "%o determinant=%o minimum=%o kissing=%o theta=%o\n", name,d,m,kissing,theta;

    D, LD, projection := DualQuotient(L);
    assert #D eq d;
    printf "%o discriminant_group=%o\n", name, D;
    if name in ["K10", "K10_alt"] then
        S, P, Q := SmithForm(G);
        assert P * G * Q eq S;
        assert Abs(Determinant(P)) eq 1 and Abs(Determinant(Q)) eq 1;
        diag := [Abs(S[i,i]) : i in [1..n]];
        assert diag eq ExpectedSmith[name];
        r3 := Rank(ChangeRing(G, GF(3)));
        assert r3 eq ((name eq "K10") select 4 else 3);
        assert Rank(ChangeRing(G, GF(5))) eq 8;
        // Dual(L) alone rescales by default and is inappropriate here.
        Ldual := Dual(L : Rescale := false);
        assert Determinant(Ldual) eq 1/d;
        md := Minimum(Ldual : Proof := true);
        VD := ShortestVectors(Ldual : Proof := true);
        assert md eq 2/5;
        assert #VD eq 3;
        assert forall{v : v in VD | Norm(v) eq 2/5};
        assert Rank(Matrix([Eltseq(v) : v in VD])) eq 2;
        printf "%o smith=%o rank_mod3=%o dual_minimum=%o dual_pair_count=%o\n", name,diag,r3,md,#VD;
        printf "%o smith_left=%o smith_right=%o\n", name,P,Q;
        printf "%o dual_representatives=%o\n", name, VD;
    end if;
end for;

// Positive isometry certificate: independently identify the unscaled E8.
standardE8 := Lattice("E", 8);
ok, T := IsIsometric(Lattices["E8"], standardE8);
assert ok;
assert Abs(Determinant(T)) eq 1;
assert T * GramMatrix(Lattices["E8"]) * Transpose(T) eq GramMatrix(standardE8);
printf "E8_ISOMETRY_MATRIX %o\n", T;
ok := IsIsometric(Lattices["K10"], Lattices["K10_alt"]);
assert not ok;
print "RANK10_TYPES_NOT_ISOMETRIC";

// This also produces new group data, without assuming the group orders.
for name in ["K9", "K10", "K10_alt"] do
    A := AutomorphismGroup(Lattices[name]);
    G := GramMatrix(Lattices[name]);
    for a in Generators(A) do
        U := Matrix(a);
        assert Abs(Determinant(U)) eq 1;
        assert U * G * Transpose(U) eq G;
    end for;
    printf "%o automorphism_order=%o generators=%o\n", name,#A,Generators(A);
end for;

print "ALL_MAGMA_EXPLICIT_CHECKS_PASS";
quit;
