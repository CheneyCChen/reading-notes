# 排版与计算展开版（17 个补充模块）

原始稿原样保存为 derivation-supplements.original.md；数学转写与显式新增说明见 README.md。

## L1-A｜线性屏蔽为何不能一直延伸到试探电荷中心

线性化需要每种参与响应的粒子均满足 \(|q_s\phi|/T_s\ll1\)，而屏蔽解为

\[
\phi(r)=\frac{Q}{r}e^{-r/\lambda_D}.
\]

当 \(r\ll\lambda_D\) 时，指数接近 1，条件变成

\[
r\gg r_{{\rm nl},s}\equiv\frac{|q_sQ|}{T_s}.
\]

因此「距离小于德拜长度」不自动意味着公式可靠。在线性理论中，能与裸 Coulomb 场匹配的重叠区必须满足

\[
\max_s r_{{\rm nl},s}\ll r\ll\lambda_D.
\]

对电荷量与背景粒子相当的试探电荷，弱耦合通常提供这个尺度间隔；但很大的外加 \(Q\) 可以使 \(r_{\rm nl}\) 与 \(\lambda_D\) 相当，即使原来的等离子体弱耦合，试探扰动也可能是非线性的。此时不能把线性解预测的近中心密度发散当作实际密度，必须使用非线性响应及适合的短距物理。

另一个容易混淆的条件是「谁有时间响应」。多组分 \(\lambda_D^{-2}=\sum_s4\pi n_sq_s^2/T_s\) 是允许这些物种都作静态 Boltzmann 响应的结果。对快于离子运动的电子过程，应把离子视为固定背景，只保留电子的屏蔽响应；这不是把同一静态公式任意少算一项，而是换了响应时间排序。第 6 讲的动态响应会把这一点定量化。

## L2-A｜从精确受迫运动推出 \(\mathbf E\times\mathbf B\) 与极化漂移

在空间均匀的常磁场中，取弱电场的 Fourier 分量 \(\mathbf E_\omega e^{-i\omega t}\)，并只求受迫特解，暂不计由初值决定的自由回旋。垂直运动满足

\[
-i\omega\mathbf V_\perp=\frac qm\mathbf E_\perp+\Omega\mathbf V_\perp\times\mathbf b.
\]

利用垂直平面上两次叉乘等于负恒等变换，可直接反演得到

\[
\mathbf V_\perp=\frac{q/m}{\Omega^2-\omega^2}
\left(\Omega\mathbf E_\perp\times\mathbf b-i\omega\mathbf E_\perp\right).
\]

当 \(|\omega/\Omega|\ll1\) 时，将分母展开：

\[
\mathbf V_\perp=
\frac cB\mathbf E_\perp\times\mathbf b
+\frac{mc^2}{qB^2}\partial_t\mathbf E_\perp
+O\!\left(\frac{\omega^2}{\Omega^2}V_E\right).
\]

第一项是 \(\mathbf E\times\mathbf B\) 漂移，第二项就是极化漂移。它们不是互不相关的两个公式，而是同一个受迫响应的零阶与一阶近似。精确分母也说明：靠近 \(|\omega|=|\Omega|\)，小参数展开失效，无碰撞共振强迫一般不能由一个有界稳态特解描述。

这里电场空间均匀，所以导数确实是 \(\partial_t\)；在缓变非均匀场中，相关变化率还包括沿零阶导心轨道看到的对流变化。不能把本节精确均匀场公式直接当作任意空间结构的完整导心解。

## L2-B｜FLR 的二阶项是 Bessel 回旋平均的展开

局部磁场均匀、零阶轨道为圆时，令一项场扰动为 \(\mathbf E_{\mathbf k}e^{i\mathbf k\cdot\mathbf x}\)。选择回旋相位 \(\theta\) 的原点，使 \(\mathbf k_\perp\cdot\boldsymbol\rho=k_\perp\rho_L\cos\theta\)，则

\[
\langle\mathbf E(\mathbf X+\boldsymbol\rho)\rangle
=\mathbf E_k e^{i\mathbf k\cdot\mathbf X}
\frac1{2\pi}\int_0^{2\pi}e^{ik_\perp\rho_L\cos\theta}\,d\theta
=J_0(k_\perp\rho_L)\mathbf E(\mathbf X).
\]

在积分中展开指数。奇次 \(\cos\theta\) 的平均为零，而 \(\langle\cos^2\theta\rangle=1/2\)、\(\langle\cos^4\theta\rangle=3/8\)，因此

\[
J_0(a)=1-\frac{a^2}{4}+\frac{a^4}{64}+\cdots.
\]

这就重现网页中的 \(1-k_\perp^2\rho_L^2/4\)。对有限 \(a\)，\(J_0\) 比截断多项式更准确地描述这一圆轨道上的几何平均；但使用 \(J_0\) 并没有自动证明圆轨道近似、低频排序或微扰振幅假设仍成立。尤其不能用它掩盖强场扰动已改变轨道的问题。

## L3-A｜作用量为什么平均守恒：算一遍慢变谐振子

「瞬时作用量」的定义本身不等于守恒定理。先用最简单的例子看守恒来自何处。考虑

\[
H=\frac{p^2}{2m}+\frac{m\omega(t)^2x^2}{2},\qquad J=\frac H\omega.
\]

沿真实运动，\(dH/dt=\partial H/\partial t=m\omega\dot\omega x^2\)，所以

\[
\dot J=\dot\omega\left(mx^2-\frac H{\omega^2}\right).
\]

在一次快振荡内冻结慢变量，用 \(x=\sqrt{2J/(m\omega)}\sin\theta\)、\(H=\omega J\)，得到

\[
\dot J=-J\frac{\dot\omega}{\omega}\cos2\theta.
\]

它并非每一时刻严格为零；关键是右侧为快振荡，周期平均为零。若 \(\epsilon=|\dot\omega|/\omega^2\ll1\)，振荡造成的相对摆动为 \(O(\epsilon)\)，首阶没有持续同号的累积。更一般的作用量–角变量变换给出同类结构：慢参数引入的角度周期项，其对角度的导数平均为零。

回旋运动的最低阶 Hamiltonian 正是这种谐振子，且 \(J_{\rm gyro}=\mu mc/|q|\)，所以这一平均机制解释 \(\mu\) 的绝热性。但靠近分界轨道、频率趋零、共振或快速参数变化时，「快振荡可以平均掉」不再成立。本例仅说明最低阶机制，不证明未经修正的瞬时 \(J\) 在所有情形下都有指数小误差。

## L3-B｜抗磁电流为何不能只把导心漂移相加

取直磁场 \(B(x)\hat{\mathbf z}\)、缓变的垂直压强 \(p_\perp(x)\)，忽略此阶之外的极化电流和有限回旋半径修正。每粒子的磁矩平均满足 \(n\langle\mu\rangle=p_\perp/B\)。梯度漂移带来的导心电流是

\[
\mathbf j_{{\rm gc},\nabla B}
=nq\langle\mathbf V_{\nabla B}\rangle
=\frac{cp_\perp}{B^2}\mathbf b\times\nabla B.
\]

另一方面，磁化强度 \(\mathbf M=-(p_\perp/B)\mathbf b\) 产生

\[
\mathbf j_M=c\nabla\times\mathbf M
=\frac cB\mathbf b\times\nabla p_\perp
-\frac{cp_\perp}{B^2}\mathbf b\times\nabla B.
\]

两者相加，显式的 \(\nabla B\) 项抵消：

\[
\boxed{\mathbf j_\perp=\frac cB\mathbf b\times\nabla p_\perp}.
\]

所以即使 \(B\) 完全均匀、每个导心没有 \(\nabla B\) 漂移，只要回旋轨道的占据随位置不均匀，仍可有抗磁电流。反过来，只统计导心漂移会漏掉磁化电流。这里是直磁场下的局部一阶分解；弯曲磁场还要同时处理曲率漂移、磁化几何项和压强各向异性，自洽场还须满足 Ampère 方程及力平衡。

## L4-A｜相混合如何让可见扰动消失，却不增加细粒度熵

不必先讨论自洽波，最简单的自由输运已经展示相混合。取一维周期空间，

\[
\partial_t f+v\partial_xf=0,\qquad
f(x,v,0)=F(v)[1+a\cos kx],\quad |a|<1.
\]

沿特征线 \(x-vt=\mathrm{const}\)，精确解是

\[
f(x,v,t)=F(v)[1+a\cos k(x-vt)].
\]

若 \(F\) 为零均值 Maxwell 分布、方差 \(v_T^2\)，则 Gaussian Fourier 积分给出

\[
\delta n(x,t)=a n_0\cos kx\,e^{-k^2v_T^2t^2/2}.
\]

密度扰动衰减了，但分布函数并未「忘记」扰动：它在速度方向形成尺度 \(\Delta v\sim1/(|k|t)\) 的细纹。坐标剪切 \((x,v)\mapsto(x-vt,v)\) 的 Jacobian 为 1，所以 \(\int f\ln f\,dx\,dv\) 不变。本例是自由相混合，不是自洽 Landau 阻尼的完整计算。

若仪器只分辨每个单元中的平均 \(\bar f\)，凸函数 \(h(f)=f\ln f\) 满足 Jensen 不等式

\[
h(\bar f)\leq\overline{h(f)},\qquad
-\int\bar f\ln\bar f\,dz\geq-\int f\ln f\,dz.
\]

粗粒度熵比同一时刻的细粒度熵更大，因此「看不见的细纹」可造成表观不可逆；但这条不等式本身不保证固定粗粒化下的熵每时每刻单调增加。回波与重现正提醒我们：丢失在观测分辨率之外的信息，不等于 Hamilton 动力学把信息销毁了。

## L4-B｜Gardner 重排怎样从定义变成可计算构造

交换论证说明最低能分布要随能量递减，但还没有给出如何找到它。定义初态的「超水平集体积」

\[
\mathcal V_f(\eta)=\int\Theta(f_0(z)-\eta)\,dz,
\]

即分布值大于 \(\eta\) 的相空间体积。不可压缩重排保留所有 \(\eta\) 对应的 \(\mathcal V_f\)。对体积为 \(V_x\) 的均匀三维空间盒，动能低于 \(E\) 的相空间体积是

\[
\mathcal V_E(E)=V_x\frac{4\pi}{3}\left(\frac{2E}{m}\right)^{3/2}.
\]

构造最低能态时，把最大的 \(f\) 值依次填入最低能的相空间区域。若 \(f_G(E_\eta)=\eta\)，则匹配条件是

\[
\mathcal V_E(E_\eta)=\mathcal V_f(\eta).
\]

由两个单调函数求广义逆，即可计算 \(f_G\)，再积分得到 \(K_{\min}\)。存在平台时用广义逆解释，不要求每个值都严格一一对应。

例如，均匀漂移 Maxwell 分布 \(F(\mathbf v-\mathbf U)\) 与无漂移 \(F(\mathbf v)\) 的超水平集体积相同，因此不约束总动量的 Gardner 重排给 \(K_G=NmU^2/2\)。但若实际系统还严格守恒总动量，而且没有其他动量储库，这部分整体漂移动能并不能全部提取。这个例子说明：仅用 Casimir 的最低能构造提供上界，实际可达态还受动量、场、几何等附加约束限制。

## L5-A｜为什么只保留小角碰撞的前两个统计矩

Rutherford 小角散射给 \(\chi\sim|b_0|/b\)，而一次速度增量大小为 \(|\Delta\mathbf v|\sim u\chi\)。遭遇权重是 \(nu\,2\pi b\,db\)。因此第 \(r\) 阶增量率的数量级为

\[
M_r\sim nu^{r+1}|b_0|^r
\int_{b_{\min}}^{b_{\max}}b^{1-r}\,db.
\]

取经典 \(b_{\min}\sim|b_0|\)。\(r=2\) 给

\[
M_2\sim nu^3b_0^2\ln\Lambda.
\]

而 \(r>2\) 的非零项主要由短距端贡献，通常只有

\[
M_r\sim nu^{r+1}b_0^2,
\]

不再带大对数。下端的小角近似本身已失效，这里只作标度估计；使用完整散射角仍给出同类非对数贡献，不能靠此估计求出精确系数。若分布在速度尺度 \(u\) 上变化，\(r\) 阶 Kramers–Moyal 项还带 \(u^{-r}\)；于是较高阶项相对二阶项约小 \(1/\ln\Lambda\)。平均纵向增量虽是一阶矩，却从 \(\chi^2\) 开始，因而同样保留对数贡献。方位对称性也会使部分奇次张量矩直接为零。

这说明 Landau/Fokker–Planck 近似首先是弱耦合下的「对数精度」近似，不是每一个真实碰撞都无限小。罕见大角事件给非对数修正；对尾部逃逸、稀有大能量转移等特别依赖这些事件的问题，仅靠 \(\ln\Lambda\) 较大并不足以保证精度。

## L5-B｜同一 Lorentz 算子为什么有不同的弛豫频率

在固定速率 \(v\) 的球面上，将角分布展开为球谐函数：

\[
f(v,\theta,\varphi,t)=\sum_{\ell,m}f_{\ell m}(v,t)Y_{\ell m}(\theta,\varphi).
\]

利用 \(\Delta_\Omega Y_{\ell m}=-\ell(\ell+1)Y_{\ell m}\) 和 \(C=(\nu(v)/2)\Delta_\Omega f\)，得到

\[
f_{\ell m}(v,t)=f_{\ell m}(v,0)
\exp\!\left[-\frac{\ell(\ell+1)}2\nu(v)t\right].
\]

\(\ell=0\) 的各向同性部分完全不变；\(\ell=1\) 的偶极角分布按 \(\nu\) 衰减，对应速度矢量的一阶矩；\(\ell=2\) 的四极角分布按 \(3\nu\) 衰减，对应无迹压力各向异性。因此，即使只有一种碰撞算子，「碰撞频率」「动量弛豫频率」「压力各向同性化频率」也可以不同。

若 \(\nu\) 随 \(v\) 变化，将不同速率球面再积分之后，整体流速或整体压力未必遵循一个单指数。不能不加平均定义就把球面上的 \(\nu(v)\) 替换成唯一的热碰撞频率。

## L5-C｜把 Rosenbluth 势真正算成 Maxwell 背景的慢化与扩散

设背景物种 \(b\) 静止、各向同性，

\[
f_b(\mathbf v')=\frac{n_b}{(2\pi\sigma^2)^{3/2}}
e^{-v'^2/(2\sigma^2)},\quad
\sigma^2=\frac{T_b}{m_b},\quad x=\frac{v}{\sqrt2\sigma}.
\]

此处把背景当给定热浴；测试粒子算子本身不承担背景的反冲，讨论全体系守恒时必须补回背景方程。

球对称使速度空间 Poisson 方程降为

\[
\frac{d}{dv}(v^2\phi_b')=-4\pi v^2f_b(v).
\]

先算包围的速度空间粒子数 \(4\pi\int_0^v s^2f_b(s)\,ds=n_bF(x)\)，便有 \(v^2\phi_b^\prime=-n_bF(x)\)。在 \(v=0\) 处取正则解、无穷远取 \(\phi_b\sim n_b/v\)，继续积分得到

\[
\phi_b(v)=\frac{n_b}{v}\operatorname{erf}x,\qquad
\phi_b'=-\frac{n_b}{v^2}F(x),\quad
F(x)=\operatorname{erf}x-\frac{2x}{\sqrt\pi}e^{-x^2}.
\]

再由 \((v^2\psi_b^\prime)^\prime=2v^2\phi_b\) 积分，可写成

\[
\psi_b=n_b\left[\left(v+\frac{\sigma^2}{v}\right)\operatorname{erf}x
+\sqrt{\frac2\pi}\sigma e^{-x^2}\right].
\]

定义 \(G(x)=F(x)/(2x^2)\)。直接求导得

\[
\psi_b'=n_b[\operatorname{erf}x-G(x)],\qquad
\psi_b''=\frac{2n_b}{v}G(x).
\]

径向函数的 Hessian 为

\[
\partial_i\partial_j\psi_b
=\psi_b''\hat v_i\hat v_j+
\frac{\psi_b'}v(\delta_{ij}-\hat v_i\hat v_j).
\]

令 \(\Gamma_{sb}=4\pi q_s^2q_b^2\ln\Lambda_{sb}/m_s^2\)，并沿用网页的 Kramers–Moyal 约定 \(C=-\partial_i(A_if)+\partial_i\partial_j(B_{ij}f)\)，便得到

\[
\mathbf A=-\Gamma_{sb}n_b\left(1+\frac{m_s}{m_b}\right)
\frac{F(x)}{v^3}\mathbf v,
\]

\[
\mathsf B=B_\parallel\hat{\mathbf v}\hat{\mathbf v}
+B_\perp(\mathsf I-\hat{\mathbf v}\hat{\mathbf v}),
\quad
B_\parallel=\frac{\Gamma_{sb}n_b}{v}G(x),\quad
B_\perp=\frac{\Gamma_{sb}n_b}{2v}[\operatorname{erf}x-G(x)].
\]

这里 \(B_\perp\) 是每一个垂直方向的扩散系数，并不是两个方向之和。与原式 (34) 对照：

\[
\nu^{\rm slow}=\frac{\Gamma_{sb}n_b}{v^3}
\left(1+\frac{m_s}{m_b}\right)F,
\quad \nu^\parallel=\frac{2\Gamma_{sb}n_b}{v^3}G,
\quad \nu^\perp=\frac{2\Gamma_{sb}n_b}{v^3}(\operatorname{erf}x-G).
\]

**两个极限检验。** 当 \(v\gg\sigma\)，\(F\to1\)、\(G\sim\sigma^2/v^2\)，所以 \(B_\parallel\sim\Gamma n_b\sigma^2/v^3\)，\(B_\perp\sim\Gamma n_b/(2v)\)：快粒子的速度扩散以改变方向为主。当 \(v\to0\)，\(F\sim4x^3/(3\sqrt\pi)\)、\(G\sim2x/(3\sqrt\pi)\)，于是

\[
B_\parallel=B_\perp\longrightarrow
\frac{\sqrt2\,\Gamma_{sb}n_b}{3\sqrt\pi\,\sigma},
\]

扩散恢复各向同性且有限，\(\mathbf A\) 与 \(v\) 成正比。公式中看似奇异的 \(v^{-1}\)、\(v^{-3}\) 被 \(F\)、\(G\) 的小 \(x\) 行为抵消。

**为什么不能直接用 \(\mathbf A\) 配 Einstein 关系？** 这里 \(\nabla_v\cdot\mathsf B=\Gamma_{sb}\nabla_v\phi_b\)，因此通量中的摩擦是

\[
\mathbf V=-\mathbf A+\nabla_v\cdot\mathsf B
=-\Gamma_{sb}\frac{m_s}{m_b}\nabla_v\phi_b,
\]

其质量系数是 \(m_s/m_b\)，而不是 \(\mathbf A\) 中的 \(1+m_s/m_b\)。用 \(F=2x^2G=v^2G/\sigma^2\) 可检查

\[
\mathbf V=\frac{m_s}{T_b}\mathsf B\cdot\mathbf v.
\]

因此温度为 \(T_b\) 的测试粒子 Maxwell 分布满足 \(\mathbf V f+\mathsf B\cdot\nabla_vf=0\)。这个计算同时核对质量因子、扩散的 \(1/2\) 约定和共同温度平衡。

## L5-D｜从 \(H\) 定理的等号条件推出 Maxwell 分布，而不只是代入验证

\(H\) 定理给出非负熵产生。对光滑、严格正、具有有限密度和能量的分布，等号要求每一对速度的横向投影消失：

\[
\mathsf U(\mathbf v-\mathbf v')
[\mathbf a_s(\mathbf v)-\mathbf a_{s'}(\mathbf v')]=0,
\qquad \mathbf a_s=\frac1{m_s}\nabla_v\ln f_s.
\]

先取同种粒子，并令 \(\mathbf v^\prime=\mathbf v+\delta\mathbf v\)。由于 \(\mathsf U\) 只消去与 \(\delta\mathbf v\) 平行的向量，Jacobian 矩阵 \(\nabla\mathbf a_s\) 必须把任意 \(\delta\mathbf v\) 映到与它平行的方向，所以 \(\nabla\mathbf a_s=\lambda_s(\mathbf v)\mathsf I\)。不同分量的混合偏导相容性进一步要求 \(\nabla\lambda_s=0\)，因而

\[
\mathbf a_s=\mathbf c_s+\lambda_s\mathbf v,
\quad
\ln f_s=A_s+m_s\mathbf c_s\cdot\mathbf v
+\frac{m_s\lambda_s}2v^2.
\]

可积性要求 \(\lambda_s<0\)。配方即得 Maxwell 分布，\(T_s=-1/\lambda_s\)、\(\mathbf U_s=-\mathbf c_s/\lambda_s\)。对于彼此有碰撞耦合的不同物种，再将这两个线性函数代回等号条件，可得 \(\lambda_s=\lambda_{s^\prime}\)、\(\mathbf c_s=\mathbf c_{s^\prime}\)：它们必须有共同温度和共同流速，而各物种密度可以不同。

这里的密度、共同流速与共同温度仍可依赖位置和时间：这是碰撞算子的局域平衡条件，并不自动满足完整动理学方程的输运与自洽场平衡。此结论依赖完整、相互连通的碰撞网络及上述正则性条件。只有 Lorentz 角散射时，速率方向没有耗散，等号条件不能唯一确定 Maxwell 分布；这正是两种模型的本质差别。

## L6-A｜从同一个 Vlasov 响应得到「冷流体」与「Boltzmann 电子」

取无磁、均匀 Maxwell 背景的一维纵向扰动，已把两个横向速度积分掉。设 \(f_1,\phi_1\propto e^{ikx-i\omega t}\)，线性 Vlasov 方程给

\[
(-i\omega+ikv)f_1-\frac qm ik\phi_1 f_0'=0,
\qquad
f_1=\frac{q\phi_1}{m}\frac{f_0'}{v-\omega/k}.
\]

分母中的共振极点不能随便删掉。因果初值问题从 \(\operatorname{Im}\omega>0\) 定义响应，再作 Landau 延拓。对 \(k>0\)，定义

\[
\zeta=\frac\omega{\sqrt2kv_T},\qquad
Z(\zeta)=\frac1{\sqrt\pi}\int_{\mathcal L}
\frac{e^{-u^2}}{u-\zeta}\,du.
\]

由 \(f_0^\prime=-vf_0/v_T^2\) 和 \(v/(v-\omega/k)=1+(\omega/k)/(v-\omega/k)\)，速度积分得到

\[
\boxed{\frac{n_1}{n_0}=-\frac{q\phi_1}{T}[1+\zeta Z(\zeta)]}.
\]

**高相速度 \(|\zeta|\gg1\)。** 展开 \(1/(u-\zeta)\)，奇次 Gaussian 矩为零，\(\langle u^2\rangle=1/2\)、\(\langle u^4\rangle=3/4\)，因此非共振的渐近部分为

\[
1+\zeta Z(\zeta)
=-\frac1{2\zeta^2}-\frac3{4\zeta^4}+\cdots,
\]

\[
\frac{n_1}{n_0}=\frac{qk^2\phi_1}{m\omega^2}
\left(1+\frac{3k^2v_T^2}{\omega^2}+\cdots\right).
\]

取单一响应物种、另一组分为固定中性化背景，代入 Poisson 方程便重现 \(\omega^2=\omega_p^2+3k^2v_T^2+\cdots\)；系数 3 与压力矩推导一致。有限阶的这类代数展开不会得到一般的共振阻尼，不能把「实频率算对了」理解为完整动力学都已保留。

**低相速度 \(|\zeta|\ll1\)。** 对接近实轴的因果 Maxwell 响应，\(Z(\zeta)=i\sqrt\pi-2\zeta+\cdots\)，所以

\[
\frac{n_1}{n_0}=-\frac{q\phi_1}{T}
[1+i\sqrt\pi\zeta-2\zeta^2+\cdots].
\]

主阶正是 Boltzmann 响应。后续虚部是相位滞后/共振响应，证明「忽略惯性」并不等于所有动力学修正都消失。离子声模型同时用电子的低相速度极限和离子的高相速度极限，需要 \(v_{Ti}\ll|\omega/k|\ll v_{Te}\)；通常 \(T_e\gg T_i\) 才能使离子阻尼也小。这里不把原稿的无碰撞准静态假设说成碰撞热化。

## L6-B｜回旋对称压力的散度如何包含镜力和曲率力

令 \(\Delta p=p_\parallel-p_\perp\)，压力张量为 \(\mathsf P=p_\perp\mathsf I+\Delta p\,\mathbf b\mathbf b\)。按分量对乘积求导：

\[
\nabla\cdot\mathsf P=\nabla p_\perp
+\mathbf b\,\partial_\parallel\Delta p
+\Delta p[(\nabla\cdot\mathbf b)\mathbf b+\boldsymbol\kappa],
\quad \boldsymbol\kappa=(\mathbf b\cdot\nabla)\mathbf b.
\]

再用 \(\nabla\cdot\mathbf b=-\partial_\parallel\ln B\)，得到平行与垂直分量：

\[
\mathbf b\cdot\nabla\cdot\mathsf P
=\partial_\parallel p_\parallel
+(p_\perp-p_\parallel)\partial_\parallel\ln B,
\]

\[
(\nabla\cdot\mathsf P)_\perp
=\nabla_\perp p_\perp+(p_\parallel-p_\perp)\boldsymbol\kappa.
\]

动量方程里的力为 \(-\nabla\cdot\mathsf P\)，所以这些式子不能只按 \(\nabla p\) 的直觉写。若 \(p_\parallel\) 很小且只看平行磁场梯度项，每粒子受力为

\[
-\frac{p_\perp}{n}\partial_\parallel\ln B
=-\langle\mu\rangle\partial_\parallel B,
\]

正是单粒子镜力的平均。压力张量的几何导数把第 2–3 讲的轨道物理带入流体方程；只保留两个压力标量而忽略 \(\mathbf b\) 的空间变化，会把这一项丢失。

## L7-A｜把「繁琐但直接」的 BGK 高斯积分逐行算完

记 \(a=v_T^2=T/m\)、\(\langle h\rangle=n^{-1}\int hg_0\,d^3w\)，定义无迹二阶多项式 \(A_{ij}=w_iw_j-\delta_{ij}w^2/3\)。式 (39)–(40) 给

\[
\widetilde g=-\frac{g_0}{\nu}
\left[\left(\frac{w^2}{2a}-\frac52\right)
\frac{w_k\partial_kT}{T}
+\frac{A_{kl}}a\partial_lU_k\right].
\]


**高斯矩的来源。** 将归一化三维 Maxwell 权重写成三个独立的一维 Gaussian 权重的乘积。一维偶次矩由分部积分递推：

\[
\begin{aligned}
I_{2r}\equiv\frac1{\sqrt{2\pi a}}\int_{-\infty}^{\infty}
y^{2r}e^{-y^2/(2a)}\,dy
&=-\frac{a}{\sqrt{2\pi a}}\int_{-\infty}^{\infty}
y^{2r-1}\frac d{dy}e^{-y^2/(2a)}\,dy\\
&=a(2r-1)I_{2r-2},\qquad I_0=1.
\end{aligned}
\]

边界项因 Gaussian 衰减为零，奇次矩由奇偶性为零。因此每个分量的二、四、六阶矩分别是 \(a\)、\(3a^2\)、\(15a^3\)，不同分量的矩相乘。三维四阶张量只有全同指标或两两相同指标时非零，故

\[
\langle w_iw_jw_kw_l\rangle
=a^2(\delta_{ij}\delta_{kl}+\delta_{ik}\delta_{jl}
+\delta_{il}\delta_{jk}).
\]

把 \(w^2=w_1^2+w_2^2+w_3^2\) 的平方、立方展开，明确数出同分量、两分量、三分量项：

\[
\begin{aligned}
\langle w^4\rangle
&=3(3a^2)+2\binom32a^2=15a^2,\\
\langle w^6\rangle
&=3(15a^3)+3(3\cdot2)(3a^3)+6a^3=105a^3,\\
\langle w_iw_jw^2\rangle&=5a^2\delta_{ij}.
\end{aligned}
\]

最后展开两个无迹多项式。除去两个迹、再加回双迹后，\(\delta_{ij}\delta_{kl}\) 的系数变为 \(1-5/3-5/3+15/9=-2/3\)：

\[
\begin{aligned}
\langle A_{ij}A_{kl}\rangle
&=\langle w_iw_jw_kw_l\rangle
-\frac{\delta_{ij}}3\langle w^2w_kw_l\rangle
-\frac{\delta_{kl}}3\langle w_iw_jw^2\rangle
+\frac{\delta_{ij}\delta_{kl}}9\langle w^4\rangle.
\end{aligned}
\]

这就给出下一步应力积分所需的无迹四阶矩，热流中的四阶、六阶径向矩也已有直接来源。

**先求应力。** 温度梯度项为奇函数，对 \(\Pi_{ij}\) 的积分为零。Gaussian 四阶矩给

\[
\langle A_{ij}A_{kl}\rangle
=a^2\left(\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk}
-\frac23\delta_{ij}\delta_{kl}\right).
\]

于是

\[
\Pi_{ij}=-\frac{mn}{\nu a}\langle A_{ij}A_{kl}\rangle\partial_lU_k
=-\frac{P}{\nu}
\left(\partial_jU_i+\partial_iU_j-\frac23\delta_{ij}\nabla\cdot\mathbf U\right).
\]

**再求热流。** 剪切项为偶函数，对 \(Q_i\) 的积分为零。各向同性意味着 \(\langle w_iw_jF(w^2)\rangle=\delta_{ij}\langle w^2F(w^2)\rangle/3\)，所以

\[
\begin{aligned}
Q_i&=-\frac{mn}{2\nu T}\partial_jT
\left\langle w_iw_jw^2\left(\frac{w^2}{2a}-\frac52\right)\right\rangle\\
&=-\frac{mn}{6\nu T}\partial_iT
\left[\frac{\langle w^6\rangle}{2a}-\frac52\langle w^4\rangle\right].
\end{aligned}
\]

代入 \(\langle w^4\rangle=15a^2\)、\(\langle w^6\rangle=105a^3\)，方括号为 \(15a^2\)，故

\[
\boxed{\mathbf Q=-\frac{5mn a^2}{2\nu T}\nabla T
=-\frac{5P}{2m\nu}\nabla T}.
\]

现在 \(\eta=P/\nu\) 与 \(\kappa=5P/(2m\nu)\) 的每个系数都有来源。它们是这一个常频率、守恒型 BGK 近似的结果；不能期待它同时复现 Landau 算子对所有非平衡矩的不同弛豫率。

## L7-B｜零矩条件不只是选规范，还给出可解性检验

线性碰撞算子的像必须与守恒的左零模相容。因此方程 \(\widehat C\widetilde g=\text{源项}\)的右侧必须具有零粒子数、零动量和零能量矩。只写 \(\int\widetilde g\{1,\mathbf w,w^2\}\,d^3w=0\) 固定解的定义，还不够；也应检查源项是否满足这些条件。

对本讲无磁、仅自碰撞的一阶驱动，剪切项的粒子数矩因 \(\langle A_{ij}\rangle=0\) 消失，动量矩因奇偶性消失，能量矩因

\[
\langle w^2w_iw_j\rangle=5a^2\delta_{ij},\qquad
\frac{\delta_{ij}}3\langle w^4\rangle=5a^2\delta_{ij}
\]

相消。温度梯度项的粒子数、能量矩是奇函数；其动量矩则需要真正计算：

\[
\left\langle w_iw_j\left(\frac{w^2}{2a}-\frac52\right)\right\rangle
=\left(\frac{5a^2}{2a}-\frac52a\right)\delta_{ij}=0.
\]

因此温度多项式里的 \(5/2\) 不只是代数巧合，它恰好去掉会改变局域流速的分量。一般 Chapman–Enskog 方法先用零阶流体方程消去时间导数，正是在保证这些可解性条件，而非随意丢掉时间演化。

## L7-C｜热流和黏性如何产生熵，Hall 项为什么不产生同类耗散

对单物种自碰撞、无外部热源，正确的三维内能式为

\[
\frac32nD_tT+P\nabla\cdot\mathbf U
=-\nabla\cdot\mathbf Q-\boldsymbol\Pi:\nabla\mathbf U.
\]

令每粒子熵 \(s=(3/2)\ln T-\ln n+\mathrm{const}\)，用连续性方程消去 \(D_tn\)，得到 \(nT D_ts=-\nabla\cdot\mathbf Q-\boldsymbol\Pi:\nabla\mathbf U\)。除以 \(T\)，并把热流散度改写为熵通量：

\[
\partial_t(ns)+\nabla\cdot\left(ns\mathbf U+\frac{\mathbf Q}{T}\right)
=-\frac{\mathbf Q\cdot\nabla T}{T^2}
-\frac{\boldsymbol\Pi:\nabla\mathbf U}{T}.
\]

对 \(\mathbf Q=-\kappa\nabla T\)、\(\boldsymbol\Pi=-\eta\mathsf W\)，其中 \(\mathsf W=\nabla\mathbf U+(\nabla\mathbf U)^{\mathsf T}-(2/3)\mathsf I\nabla\cdot\mathbf U\)，由 \(\mathsf W\) 的对称无迹性有 \(\mathsf W:\nabla\mathbf U=\mathsf W:\mathsf W/2\)。因此

\[
\boxed{\sigma_{\rm entropy}=\frac{\kappa|\nabla T|^2}{T^2}
+\frac{\eta}{2T}W:W\geq0}.
\]

这也核查了应力负号：黏性使有序动能转化为热，不能使热源符号任意翻转。磁化热流中的 \(\mathbf Q_\times\propto\mathbf b\times\nabla T\) 与 \(\nabla T\) 正交，所以该项不直接贡献此处的局域熵产生；但它在系数或磁场方向不均匀时仍可能有非零散度，仍可重新分配热量。类似地，Hall 电流满足 \(\mathbf E\cdot\mathbf j_H=0\)，但不代表 Hall 电流在每一种几何中都没有输运作用。

## L7-D｜碰撞摩擦与热源为什么必须成对满足同一个能量恒等式

把实验室系的碰撞能量源写成中心矩：

\[
\int\frac{m_sv^2}{2}C_s\,d^3v
=S_s+\mathbf U_s\cdot\mathbf R_s,
\]

因为 \(\mathbf v=\mathbf U_s+\mathbf w\)，粒子数矩为零，交叉项恰为 \(\mathbf U_s\cdot\mathbf R_s\)。对一对物种 \(a,b\)，碰撞保持总动量及总实验室系能量，因此

\[
\mathbf R_a+\mathbf R_b=0,
\qquad
S_a+S_b+\mathbf R_a\cdot(\mathbf U_a-\mathbf U_b)=0.
\]

取 \(a=e\)、\(b=i\)，马上得到

\[
S_{ei}=-S_{ie}+\mathbf R_{ei}\cdot(\mathbf U_i-\mathbf U_e),
\]

这不是独立猜出的加热项，而是总能量守恒强制要求的关系。若只保留摩擦 \(\mathbf R_e=\alpha(\mathbf U_i-\mathbf U_e)\)、\(\alpha>0\)，则两物种内能增加总量为 \(\alpha|\mathbf U_i-\mathbf U_e|^2\)，正好抵消相对流动能的减少。

原式中的热力 \(\mathbf R_e\propto-\nabla T_e\) 还带有与热流配对的交叉项，不能把完整的 \(\mathbf R_e\cdot(\mathbf U_i-\mathbf U_e)\) 每一部分都单独理解成严格非负的纯电阻加热。

最后，用本讲单价、\(n_e=n_i=n\)、无流差与无空间输运的简化条件，式 (52g) 给

\[
\dot T_i=2\frac{m_e}{m_i}\nu_{ei}(T_e-T_i),\qquad
\dot T_e=-2\frac{m_e}{m_i}\nu_{ei}(T_e-T_i).
\]

因此两温差满足

\[
\frac d{dt}(T_e-T_i)=-4\frac{m_e}{m_i}\nu_{ei}(T_e-T_i).
\]

系数 4 属于这里“两边温度都允许改变”的条件；若离子是固定温度热浴，电子方程给系数 2。两者都说明温度交换时间比电子动量弛豫时间长约 \(m_i/m_e\)，不能用「电子碰撞快」直接推出 \(T_e=T_i\)。\(\nu_{ei}\) 随温度变化时，上式仍是瞬时方程，不是全程常系数单指数。
