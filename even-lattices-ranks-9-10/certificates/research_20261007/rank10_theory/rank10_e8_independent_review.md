# Independent conceptual review: rank-ten lattices containing sqrt(3)E8

Reviewed ../rank10/rank10_e8_theorem.txt and the implementing certificate. No mathematical gap found in the stated subclass theorem or classification. The exact certificate was replayed successfully; log rank10_e8_independent_replay.log. This is a replay of the same exact kernel, not an independent implementation of the entire finite enumeration.

1. Primitivity: a nontrivial saturation class lies in J*/J and has a representative of norm≤8/3, contradicting minL≥6. This argument is valid without assuming primitiveness in advance.
2. Binary projection: because J is a rational primitive sublattice, its projection quotient is an actual rank-two lattice. Subtracting J from each lift gives minP≥10/3. The determinant factorization and exact binary Hermite bound imply detL≥54675.
3. Equality forces a hexagonal projected lattice. An acute reduced basis has both squared norms10/3 and pairing5/3; the only projected minimal directions are±z1,±z2,±(z1−z2). Hence a,b,a−b must be deep residue classes.
4. Conversely any deep pair with deep difference produces an even integral rank-ten lattice: representatives u,v have norms8, and the deep difference condition gives (u,v)≡1 modulo3. Therefore the off-diagonal lift pairing((u,v)+5)/3 is integral. The diagonals are6, so the lattice is even. The next projected squared norm is10, already exceeding6, and all minimal projected directions have total minimum6.
5. Class representative changes add vectors of J; parent isometries and these additions yield unimodular block transformations of the extension basis. Thus finite pair orbits do classify every extension surjectively. A subgroup of the actual stabilizer with two orbits suffices to show at most two full-lattice isometry types; full-stabilizer equality is not needed.
6. The displayed rank modulo3 distinguishes the full abstract rank-ten lattices, independent of their chosen E8 embeddings. Both occur, so the two-type conclusion is exact.
7. The claimed discriminant groups follow from determinant3^7·5^2 and ranks modulo3 and5. For the original type, six positive3-adic Smith valuations sum to7, so they are(1,1,1,1,1,2); for the alternative, seven valuations sum to7, hence all1. The two5-adic valuations are1 in both cases. Combining in divisibility order yields the stated groups.

The theorem does not claim global e_10(6)=54675: a lattice avoiding sqrt(3)E8 is not classified by this argument. It also gives no primitive embedding of the alternative lattice into a specified rank48 ambient lattice.
