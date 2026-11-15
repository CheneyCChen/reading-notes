"""Lecture 7–8 independent physics checks; stdlib only, no document assertions."""
import math
import random
v = [i / 20 for i in range(-240, 241)]
dv = v[1] - v[0]
f = [0.7 * math.exp(-(x - 1.1)**2 / 0.8) + 0.3 * math.exp(-(x + 0.4)**2 / 2.2) for x in v]
n = sum(f) * dv
U = sum(x * y for x, y in zip(v, f)) * dv / n
base = [math.exp(-x*x / 2) for x in v]
f0 = [n * y / (sum(base) * dv) for y in base]
m, nu = 3.0, 2.3
C = [-nu * (y-z) for y,z in zip(f,f0)]
R = sum(m*x*c for x,c in zip(v,C))*dv
Rc = sum(m*(x-U)*c for x,c in zip(v,C))*dv
assert abs(sum(C)*dv)<1e-12
assert math.isclose(R,-m*nu*n*U,rel_tol=1e-12)
assert math.isclose(Rc,R,rel_tol=1e-12)
for L in (0.01,1.,100.):
    Kn=1/(nu*L)
    assert math.isclose(R,-m*nu*n*U,rel_tol=1e-12)
    print(f'BGK moment at Kn={Kn:.6g}: residual={R+m*nu*n*U:.3g}')
rng=random.Random(78)
for _ in range(100):
    A=[[rng.uniform(-2,2) for j in range(3)] for i in range(3)]
    G=[[rng.uniform(-2,2) for j in range(3)] for i in range(3)]
    Pi=[[(A[i][j]+A[j][i])/2 for j in range(3)] for i in range(3)]
    tr=sum(Pi[i][i] for i in range(3))
    for i in range(3): Pi[i][i]-=tr/3
    p=4.
    P=[[Pi[i][j]+(p if i==j else 0) for j in range(3)] for i in range(3)]
    theta=sum(G[i][i] for i in range(3))
    visc=sum(Pi[i][j]*G[i][j] for i in range(3) for j in range(3))
    trace=sum(P[i][j]*G[i][j]+P[j][i]*G[i][j] for i in range(3) for j in range(3))
    assert math.isclose(trace/2,p*theta+visc,abs_tol=1e-12)
print('100 pressure tensors: internal-energy viscous-work coefficient is one.')
# Ti=T and beta=nT/(B²/8π): delta_i/rho_i=sqrt(2/beta).
# Not a Hall dispersion solver: the cold fast-mode estimate fails its own
# low-frequency ordering despite small k*rho_i.
beta,k_rhoi=1e-8,1e-3
k_di=k_rhoi*math.sqrt(2/beta)
assert k_rhoi<.01 and k_di>1
omega_fast_over_Omega_i=k_di
assert omega_fast_over_Omega_i>1
print(f'Low-beta counterexample: k*rho_i={k_rhoi}, k*delta_i={k_di:.6g}')
print('All Lecture 7–8 physics checks passed.')

# A small gyroradius alone does not bound transit through parallel gradients.
rho_over_L=1e-3;vparallel_over_vperp=1e4
assert rho_over_L<.01 and vparallel_over_vperp*rho_over_L>1
# Finite local filtering need not be a Reynolds projector.
f=[0.,0.,0.,9.,0.,0.,0.]
def filt(a):return [(a[(i-1)%len(a)]+a[i]+a[(i+1)%len(a)])/3 for i in range(len(a))]
mean=filt(f)
assert max(abs(x) for x in filt([x-y for x,y in zip(f,mean)]))>.9
# Incompressible plane extension has nonzero DIAGONAL deviatoric stress.
a,eta=2.,3.;strain=[a,-a,0.];pi=[-2*eta*x for x in strain]
assert sum(strain)==sum(pi)==0 and pi[0]!=0 and pi[1]!=0
assert -sum(x*y for x,y in zip(pi,strain))==4*eta*a*a>0
print('PASS additional ordering, filtering and diagonal-stress checks')
