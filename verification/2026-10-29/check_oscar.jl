# Run: julia --project=. check_oscar.jl > results/oscar_run.log 2>&1
# Requires Oscar.jl. This checks explicit lattices and their displayed primitive
# sublattices. It does not enumerate all lattices or all rank-48 embeddings.
using Oscar
using SHA

const H = Oscar.Hecke
include(joinpath(@__DIR__, "data", "lattices.jl"))
@assert bytes2hex(sha256(read(joinpath(@__DIR__, "data", "lattices.json")))) == INPUT_SHA256
println("INPUT_SHA256 ", INPUT_SHA256)
println("JULIA_VERSION ", VERSION)
println("OSCAR_VERSION ", Base.pkgversion(Oscar))

# A returned enumeration vector uses coordinates in the lattice basis.
function exact_norm(v, G)
    return sum(QQ(v[i]) * G[i,j] * QQ(v[j]) for i in 1:nrows(G), j in 1:ncols(G))
end

const LATTICES = Dict{String,Any}()
for name in ["K9", "K10", "K10_alt", "E8"]
    G = MATRICES[name]
    n = nrows(G)
    @assert G == transpose(G)
    @assert all(iseven(G[i,i]) for i in 1:n)
    @assert all(det(G[1:k,1:k]) > 0 for k in 1:n)
    L = H.integer_lattice(; gram=G)
    LATTICES[name] = L
    @assert H.gram_matrix(L) == G
    @assert det(L) == EXPECTED_DET[name]
    @assert H.minimum(L) == EXPECTED_MIN[name]
    bound = name == "E8" ? 8 : 10
    shell_counts = Dict(k => 0 for k in 1:bound)
    seen = Set{Tuple}()
    for (v, norm) in H.short_vectors_iterator(L, 0, bound; check=true)
        @assert exact_norm(v, G) == norm
        @assert denominator(norm) == 1
        @assert 0 < norm <= bound
        key = Tuple(v)
        @assert !(key in seen) && !(Tuple(-x for x in v) in seen)
        push!(seen, key)
        # Hecke returns one representative per pair {v,-v}.
        shell_counts[Int(norm)] += 2
    end
    @assert minimum(k for (k,c) in shell_counts if c > 0) == EXPECTED_MIN[name]
    for (k,c) in EXPECTED_SHELLS[name]
        @assert shell_counts[k] == c
    end
    D = H.discriminant_group(L)
    @assert H.order(H.abelian_group(D)) == det(L)
    println(name, " determinant=", det(L), " minimum=", H.minimum(L), " shells=", shell_counts)
    println(name, " discriminant_group=", H.abelian_group(D))
    println(name, " discriminant_quadratic_gram=", H.gram_matrix_quadratic(D))

    if name in ["K10", "K10_alt"]
        Ldual = H.dual(L)
        @assert det(Ldual) == inv(QQ(det(L)))
        @assert H.minimum(Ldual) == QQ(2)/5
        VD = collect(H.short_vectors_iterator(Ldual, 0, QQ(2)/5; check=true))
        @assert length(VD) == 3
        for (v,norm) in VD
            @assert norm == QQ(2)/5
            @assert exact_norm(v, H.gram_matrix(Ldual)) == norm
        end
        VDM = matrix(QQ, length(VD), n, [VD[i][1][j] for i in 1:length(VD) for j in 1:n])
        @assert rank(VDM) == 2
        println(name, " dual_minimum=", H.minimum(Ldual), " dual_pair_count=", length(VD))
    end
end

@assert H.is_isometric(LATTICES["E8"], H.root_lattice(:E, 8))
@assert !H.is_isometric(LATTICES["K10"], LATTICES["K10_alt"])

# Reconstruct the two explicit glue descriptions from their actual embeddings.
# Every check is in the ambient space of the given rank-ten lattice.
for name in ["K10", "K10_alt"]
    L = LATTICES[name]
    B = H.basis_matrix(L)
    J = H.lattice_in_same_ambient_space(L, B[1:8,:])
    K = H.lattice_in_same_ambient_space(L, B[1:9,:])
    @assert H.gram_matrix(J) == MATRICES["G8"]
    @assert H.gram_matrix(K) == MATRICES["K9"]
    @assert H.is_primitive(L, J)
    @assert H.is_primitive(L, K)
    @assert H.is_isometric(J, H.root_lattice(:E, 8, 3))
    N = H.orthogonal_submodule(L, J)
    @assert rank(N) == 2
    @assert H.is_primitive(L, N)
    scale = name == "K10" ? 15 : 5
    glue_index = name == "K10" ? 9 : 3
    @assert det(N) == 3 * scale^2
    @assert H.is_isometric(N, H.root_lattice(:A, 2, scale))
    S = J + N
    # Determinant identity gives the index; quotient order checks it independently.
    @assert det(S) == det(J) * det(N)
    @assert det(S) == glue_index^2 * det(L)
    glue = H.torsion_quadratic_module(L, S; modulus=QQ(1), modulus_qf=QQ(2), check=true)
    @assert H.order(H.abelian_group(glue)) == glue_index
    F = H.gram_matrix_quadratic(glue)
    # The quotient L/(J+N) is isotropic: integer pairings, even self-pairings.
    @assert all(denominator(F[i,j]) == 1 for i in 1:nrows(F), j in 1:ncols(F))
    @assert all(iseven(ZZ(F[i,i])) for i in 1:nrows(F))
    println(name, " primitive_E8=true primitive_K9=true complement_gram=", H.gram_matrix(N))
    println(name, " complement_scale=", scale, " glue_index=", glue_index, " glue_group=", H.abelian_group(glue))
end

println("ALL_OSCAR_EXPLICIT_CHECKS_PASS")
