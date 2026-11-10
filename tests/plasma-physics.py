"""Independent coefficient/sign/limit checks for the new teaching bridges.

These targeted algebraic/numerical checks do not prove the physical validity of
an ordering outside the assumptions documented next to each derivation.
Requires only the Python standard library.
"""
from fractions import Fraction as F
from math import erf, exp, sqrt, pi, cos, sin, log


def close(a, b, rtol=1e-7, atol=1e-9):
    assert abs(a-b) <= atol + rtol*max(abs(a),abs(b)), (a,b)

# L1-A: a weak perturbation needs a distinct short-distance/linear overlap.
q,Q,T,lam = 1., .001, 1., 1.
rnl = abs(q*Q)/T
assert rnl < .01 < lam
assert abs(q*Q*exp(-.01/lam)/(.01*T)) < .1
assert abs(q*Q*exp(-.0001/lam)/(.0001*T)) > 1

# L2-A: invert the exact two-component Fourier response, including charge sign.
for omega_c in [-3.,3.]:
    omega,qm,Ex,Ey = .2, .7, 1.3, -.8
    vx=qm*(omega_c*Ey-1j*omega*Ex)/(omega_c**2-omega**2)
    vy=qm*(-omega_c*Ex-1j*omega*Ey)/(omega_c**2-omega**2)
    close(-1j*omega*vx,qm*Ex+omega_c*vy)
    close(-1j*omega*vy,qm*Ey-omega_c*vx)
# L2-B: the gyroaverage gives 1-a²/4+a⁴/64, not 1-a²/2.
for a in [.03,.1,.3]:
    avg=sum(cos(a*cos(2*pi*j/8192)) for j in range(8192))/8192
    close(avg,1-a*a/4+a**4/64,atol=a**6/2300)

# Mirror work, both signs of parallel velocity.
for v,g in [(2.,3.),(-2.,-3.),(2.,-3.),(-2.,3.)]:
    work=-.4*v*g
    assert (work<0)==(v*g>0)

# L3-A: instantaneous J oscillates, but its frozen-period mean derivative is 0.
J,w,wdot=2.,3.,.01
for theta in [.2,1.,2.]:
    x=sqrt(2*J/w)*sin(theta)
    close(wdot*(x*x-J/w),-J*wdot/w*cos(2*theta))
close(sum(cos(4*pi*j/4096) for j in range(4096))/4096,0.)
# L3-B: guiding-centre grad-B current and magnetization cancel their B gradient.
B,p,dB,dp,c=2.,3.,.6,.7,1.
jgc=c*p*dB/B**2
jmag=c*dp/B-c*p*dB/B**2
close(jgc+jmag,c*dp/B)

# L4-A: independently integrate the free-streaming Maxwell density mode.
kvtt=.8; N=10000; lo,hi=-10.,10.; dv=(hi-lo)/N
fn=lambda v: exp(-v*v/2)*cos(kvtt*v)/sqrt(2*pi)
val=dv/3*(fn(lo)+fn(hi)+sum((4 if j%2 else 2)*fn(lo+j*dv) for j in range(1,N)))
close(val,exp(-kvtt**2/2))
# L4-B: a velocity translation leaves level-set volume unchanged, while its
# additional kinetic energy is N m U²/2 (cross term vanishes for zero mean).
Npart,m,sigma,U=5.,2.,.7,1.2
close(Npart*m*(3*sigma*sigma+U*U)/2-Npart*m*3*sigma*sigma/2,Npart*m*U*U/2)

# L5-A: higher small-angle moments carry no large Coulomb logarithm.
Lambda=1e5
for r in [3,4,5]:
    integral=(1-Lambda**(2-r))/(r-2)
    assert 0 < integral/log(Lambda) < 1/log(Lambda)
# L5-B: Legendre l=0,1,2 eigenvalues, hence 0, nu, 3nu relaxation.
for mu in [-.7,.2,.8]:
    for ell,P,dP,ddP in [(0,1.,0.,0.),(1,mu,1.,0.),(2,(3*mu*mu-1)/2,3*mu,3.)]:
        close((1-mu*mu)*ddP-2*mu*dP,-ell*(ell+1)*P)

# L5-C: radial Rosenbluth differentiation, isotropic zero-speed limit and
# the equilibrium relation use flux friction, not the Ito mean increment A.
sigma,nb,Gamma,ms,mb=1.3,1.7,.8,2.1,3.2
Tb=mb*sigma*sigma
phi=lambda v:nb*erf(v/(sqrt(2)*sigma))/v
psi=lambda v:nb*((v+sigma*sigma/v)*erf(v/(sqrt(2)*sigma))+sqrt(2/pi)*sigma*exp(-v*v/(2*sigma*sigma)))
for v in [.5,1.3,4.]:
    x=v/(sqrt(2)*sigma); ff=erf(x)-2*x*exp(-x*x)/sqrt(pi); gg=ff/(2*x*x)
    h=1e-4
    close((phi(v+h)-phi(v-h))/(2*h),-nb*ff/v**2,rtol=2e-7)
    close((psi(v+h)-psi(v-h))/(2*h),nb*(erf(x)-gg),rtol=2e-7)
    close((psi(v+h)-2*psi(v)+psi(v-h))/h**2,2*nb*gg/v,rtol=4e-6)
    Bpar=Gamma*nb*gg/v
    A=-Gamma*nb*(1+ms/mb)*ff/v**2
    divB=-Gamma*nb*ff/v**2
    V=-A+divB
    close(V,ms/Tb*Bpar*v)
v=.001; x=v/(sqrt(2)*sigma); ff=erf(x)-2*x*exp(-x*x)/sqrt(pi); gg=ff/(2*x*x)
limit=sqrt(2)*Gamma*nb/(3*sqrt(pi)*sigma)
close(Gamma*nb*gg/v,limit,rtol=2e-6)
close(Gamma*nb*(erf(x)-gg)/(2*v),limit,rtol=2e-6)
# L5-D: at a shared Maxwell T,U the entropy-production vector is parallel
# to relative velocity, so its transverse Landau projection vanishes.
v=[1.,2.,-1.];vp=[-.2,.6,1.2];temp=2.3;flow=[.3,-.1,.2]
u=[v[i]-vp[i] for i in range(3)]
diff=[-(v[i]-flow[i])/temp+(vp[i]-flow[i])/temp for i in range(3)]
u2=sum(x*x for x in u);ud=sum(u[i]*diff[i] for i in range(3))
assert max(abs(diff[i]-u[i]*ud/u2) for i in range(3))<1e-12

# L6-A: Gaussian moments of the Z-function expansion give 1/2,3/4,
# hence the kinetic high-phase-speed pressure coefficient is 3.
close((3/4)/(1/2)*2,3.)
# L6-B: explicit product-rule pressure divergence at a unit-vector frame.
b=[0.,0.,1.]; dpper=[.2,.3,.4]; dpdel=[-.5,.6,.7]; delta=.8
D=[[.1,.2,0.],[.3,.4,0.],[.5,.6,0.]] # D[j][i]=partial_j b_i
actual=[dpper[i]+sum(dpdel[j]*b[i]*b[j]+delta*(D[j][i]*b[j]+b[i]*D[j][j]) for j in range(3)) for i in range(3)]
divb=sum(D[i][i] for i in range(3)); dlnB=-divb
close(actual[2],dpper[2]+dpdel[2]-delta*dlnB)
for i in [0,1]:close(actual[i],dpper[i]+delta*D[2][i])

# L7-A/B: derive every Gaussian coefficient using independent 1-D moments.
def moment(powers):
    result=F(1)
    for power in powers:
        if power%2:return F(0)
        for odd in range(1,power,2):result*=odd
    return result # unit variance; restore a^(total degree/2)
def product(*indices):
    return moment([indices.count(i) for i in range(3)])
def w2_product(*indices):return sum(product(*indices,j,j) for j in range(3))
def w4_product(*indices):return sum(product(*indices,j,j,k,k) for j in range(3) for k in range(3))
w4=sum(product(j,j,k,k) for j in range(3) for k in range(3))
w6=sum(product(j,j,k,k,l,l) for j in range(3) for k in range(3) for l in range(3))
assert (w4,w6)==(15,105)
for i in range(3):
 for j in range(3):
  dij=int(i==j)
  assert product(i,j)==dij
  assert w2_product(i,j)==5*dij
  assert w2_product(i,j)/2-F(5,2)*product(i,j)==0 # heat-driving momentum moment
  assert w2_product(i,j)-F(dij,3)*w4==0 # shear-driving energy moment
  for k in range(3):
   for l in range(3):
    dkl=int(k==l)
    AA=product(i,j,k,l)-F(dkl,3)*w2_product(i,j)-F(dij,3)*w2_product(k,l)+F(dij*dkl,9)*w4
    assert AA==int(i==k)*int(j==l)+int(i==l)*int(j==k)-F(2,3)*dij*dkl
assert (w6/2-F(5,2)*w4)/6==F(5,2) # thermal conductivity coefficient

# L7-C: symmetric traceless strain contracts into half its squared norm.
G=[[F(1),F(2),F(-1)],[F(3),F(-2),F(4)],[F(0),F(1),F(2)]]
tr=sum(G[i][i] for i in range(3))
W=[[G[i][j]+G[j][i]-F(2,3)*tr*int(i==j) for j in range(3)] for i in range(3)]
WG=sum(W[i][j]*G[i][j] for i in range(3) for j in range(3))
WW=sum(x*x for row in W for x in row)
assert WG==WW/2 and WW>=0
E=[1.,2.,3.];field=[0.,0.,1.];hall=[-E[1],E[0],0.]
close(sum(E[i]*hall[i] for i in range(3)),0.)
# L7-D: paired friction turns relative-flow energy into heat; allowing both
# temperatures to evolve doubles the temperature-difference relaxation rate.
alpha=2.;ua=[1.,-.2,3.];ub=[-.5,1.,2.]
rel=[ub[i]-ua[i] for i in range(3)];Re=[alpha*x for x in rel]
heat=sum(Re[i]*rel[i] for i in range(3))
close(heat,alpha*sum(x*x for x in rel));assert heat>=0
rate,Te,Ti=.03,4.,1.
dTe=-2*rate*(Te-Ti);dTi=2*rate*(Te-Ti)
close(dTe-dTi,-4*rate*(Te-Ti));close(dTe+dTi,0.)
print('PASS: 17 supplement bridges and mirror-direction correction: sign, coefficient, Gaussian-moment, equilibrium, limit and energy-balance checks.')
