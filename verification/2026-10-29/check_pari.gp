\\ Independent PARI/GP cross-check. Run from this directory, after export_pari.py.
\\ qfminim uses floating-point enumeration internally, even with flag=2.
\\ This run corroborates the separate exact rational checker; it does not
\\ certify a global determinant bound or an exhaustive lattice classification.
default(realprecision, 100);
read("data/pari_inputs.gp");

ensure(c, message) = if(!c, error(message));

check_lattice(label, G, det_expected, shells_expected) = {
  my(n=matsize(G)[1], d=matdet(G), r, V, counts=vector(10), q, S, A, H, U);
  ensure(G==G~, Str(label, ": Gram matrix not symmetric"));
  ensure(d==det_expected, Str(label, ": determinant mismatch"));
  for(i=1,n, ensure(G[i,i]%2==0, Str(label, ": odd diagonal")));
  for(i=1,n, ensure(matdet(G[1..i,1..i])>0, Str(label, ": not positive definite")));
  r=qfminim(G,10,,2); V=r[3];
  for(i=1,matsize(V)[2],
    q=V[,i]~*G*V[,i];
    ensure(type(q)=="t_INT" && q>0 && q<=10, "invalid returned vector norm");
    counts[q]+=2
  );
  ensure(vecsum(counts)==r[1], Str(label, ": enumeration count mismatch"));
  ensure(counts==shells_expected, Str(label, ": short shell mismatch"));
  print("LATTICE ",label," det=",d," shells_1_to_10=",counts," smith_descending=",matsnf(G));
  print("VECTORS ",label," ",vector(matsize(V)[2],i,Vec(V[,i])));
  \\ Test the isometry backend on a nontrivial unimodular basis change.
  U=matid(n); U[1,2]=1; U[3,4]=-1; H=U~*G*U;
  S=qfisom(G,H);
  ensure(type(S)=="t_MAT", Str(label, ": isometry not found"));
  ensure(abs(matdet(S))==1 && S~*H*S==G, "invalid isometry certificate");
  A=qfauto(G);
  for(i=1,#A[2], H=A[2][i];
    ensure(abs(matdet(H))==1 && H~*G*H==G, "invalid automorphism generator")
  );
  print("AUTOMORPHISMS ",label," order=",A[1]," generators=",#A[2]);
};

check_dual(label,G) = {
  my(d=matdet(G), H=d*G^-1, r, V, q, counts=0);
  \\ Clear denominators exactly so the ellipsoid matrix is integral.
  r=qfminim(H,2*d/5,,2); V=r[3];
  for(i=1,matsize(V)[2],
    q=V[,i]~*H*V[,i]/d;
    ensure(q==2/5, "unexpected vector in dual short ball");
    counts+=2
  );
  ensure(counts==6 && r[1]==6 && matrank(V)==2, "dual shell mismatch");
  print("DUAL ",label," minimum=2/5 count=6 span_rank=2 vectors_up_to_sign=",vector(matsize(V)[2],i,Vec(V[,i])));
};

main() = {
  print("PARI_VERSION ",version());
  print("MODE qfminim flag=2; realprecision=",default(realprecision));
  check_lattice("K9",K9,21870,[0,0,0,0,0,258,0,72,0,252]);
  check_lattice("K10",K10,54675,[0,0,0,0,0,294,0,216,0,756]);
  check_lattice("K10_alt",K10_alt,54675,[0,0,0,0,0,294,0,216,0,762]);
  ensure(matrank(Mod(K10,3))==4, "K10 rank mod3 mismatch");
  ensure(matrank(Mod(K10_alt,3))==3, "K10_alt rank mod3 mismatch");
  ensure(qfisom(K10,K10_alt)==0, "unexpected rank10 isometry");
  check_dual("K10",K10); check_dual("K10_alt",K10_alt);
  print("PASS_PARI_CROSSCHECK");
};

iferr(main(), E, print("FAIL_PARI_CROSSCHECK ",E); quit(1));
quit(0);
