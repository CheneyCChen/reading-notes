# Plasma Lecture 1–7：仍缺失的推导桥梁补充稿

本稿只补现行网页仍省略的中间计算，不重复网页已有的 Rutherford 轨道积分、Landau 核转换、磁镜损失锥、矩方程取矩等完整推导。各段均应标为「新增推导」，放在对应正文之后；原文、原式、校注和原件链接保留。

统一约定：Gaussian-cgs 制，温度 T 为能量，v_T²=T/m，Ω=qB/(mc) 有符号。除另有说明，速度积分边界项为零。以下推导是教学补充，不冒充原作者正文；原讲义位置列于各段开头。

## L1-A｜线性屏蔽为何不能一直延伸到试探电荷中心

**插入位置**：Lecture 1「推导 4：一维屏蔽解、三维 Yukawa 势与电荷补偿」之后。原讲义 p.4–6 的 Boltzmann–Poisson 屏蔽模型。

线性化需要每种参与响应的粒子均满足 |q_s φ|/T_s≪1，而屏蔽解为

\[
\phi(r)=\frac{Q}{r}e^{-r/\lambda_D}.
\]

当 r≪λ_D 时，指数接近 1，条件变成

\[
r\gg r_{{\rm nl},s}\equiv\frac{|q_sQ|}{T_s}.
\]

因此「距离小于德拜长度」不自动意味着公式可靠。在线性理论中，能与裸 Coulomb 场匹配的重叠区必须满足

\[
\max_s r_{{\rm nl},s}\ll r\ll\lambda_D.
\]

对电荷量与背景粒子相当的试探电荷，弱耦合通常提供这个尺度间隔；但很大的外加 Q 可以使 r_nl 与 λ_D 相当，即使原来的等离子体弱耦合，试探扰动也可能是非线性的。此时不能把线性解预测的近中心密度发散当作实际密度，必须使用非线性响应及适合的短距物理。

另一个容易混淆的条件是「谁有时间响应」。多组分 λ_D⁻²=Σ_s 4πn_sq_s²/T_s 是允许这些物种都作静态 Boltzmann 响应的结果。对快于离子运动的电子过程，应把离子视为固定背景，只保留电子的屏蔽响应；这不是把同一静态公式任意少算一项，而是换了响应时间排序。第 6 讲的动态响应会把这一点定量化。

## L2-A｜从精确受迫运动推出 E×B 与极化漂移

**插入位置**：Lecture 2「推导 10：极化漂移、位移与电流」之后。原讲义 p.4–5、p.8–9 的均匀场与极化漂移。

在空间均匀的常磁场中，取弱电场的 Fourier 分量 E_ω e⁻ⁱωt，并只求受迫特解，暂不计由初值决定的自由回旋。垂直运动满足

\[
-i\omega\mathbf V_\perp=\frac qm\mathbf E_\perp+\Omega\mathbf V_\perp\times\mathbf b.
\]

利用垂直平面上两次叉乘等于负恒等变换，可直接反演得到

\[
\mathbf V_\perp=\frac{q/m}{\Omega^2-\omega^2}
\left(\Omega\mathbf E_\perp\times\mathbf b-i\omega\mathbf E_\perp\right).
\]

当 |ω/Ω|≪1 时，将分母展开：

\[
\mathbf V_\perp=
\frac cB\mathbf E_\perp\times\mathbf b
+\frac{mc^2}{qB^2}\partial_t\mathbf E_\perp
+O\!\left(\frac{\omega^2}{\Omega^2}V_E\right).
\]

第一项是 E×B 漂移，第二项就是极化漂移。它们不是互不相关的两个公式，而是同一个受迫响应的零阶与一阶近似。精确分母也说明：靠近 |ω|=|Ω|，小参数展开失效，无碰撞共振强迫一般不能由一个有界稳态特解描述。

这里电场空间均匀，所以导数确实是 ∂_t；在缓变非均匀场中，相关变化率还包括沿零阶导心轨道看到的对流变化。不能把本节精确均匀场公式直接当作任意空间结构的完整导心解。

## L2-B｜FLR 的二阶项是 Bessel 回旋平均的展开

**插入位置**：Lecture 2「推导 11：有限拉莫尔半径」最后一个 Fourier 检验之后。原讲义 p.9 的轨道平均。

局部磁场均匀、零阶轨道为圆时，令一项场扰动为 E_k eⁱᵏ·ˣ。选择回旋相位 θ 的原点，使 k_⊥·ρ=k_⊥ρ_L cosθ，则

\[
\langle\mathbf E(\mathbf X+\boldsymbol\rho)\rangle
=\mathbf E_k e^{i\mathbf k\cdot\mathbf X}
\frac1{2\pi}\int_0^{2\pi}e^{ik_\perp\rho_L\cos\theta}\,d\theta
=J_0(k_\perp\rho_L)\mathbf E(\mathbf X).
\]

在积分中展开指数。奇次 cosθ 的平均为零，而 ⟨cos²θ⟩=1/2、⟨cos⁴θ⟩=3/8，因此

\[
J_0(a)=1-\frac{a^2}{4}+\frac{a^4}{64}+\cdots.
\]

这就重现网页中的 1−k_⊥²ρ_L²/4。对有限 a，J₀ 比截断多项式更准确地描述这一圆轨道上的几何平均；但使用 J₀ 并没有自动证明圆轨道近似、低频排序或微扰振幅假设仍成立。尤其不能用它掩盖强场扰动已改变轨道的问题。

## L3-A｜作用量为什么平均守恒：算一遍慢变谐振子

**插入位置**：Lecture 3「推导 2：从作用量看第一绝热不变量」的回旋作用量结果之后。原讲义 p.3–4 的绝热作用量论述。

「瞬时作用量」的定义本身不等于守恒定理。先用最简单的例子看守恒来自何处。考虑

\[
H=\frac{p^2}{2m}+\frac{m\omega(t)^2x^2}{2},\qquad J=\frac H\omega.
\]

沿真实运动，dH/dt=∂H/∂t=mωω̇x²，所以

\[
\dot J=\dot\omega\left(mx^2-\frac H{\omega^2}\right).
\]

在一次快振荡内冻结慢变量，用 x=√[2J/(mω)]sinθ、H=ωJ，得到

\[
\dot J=-J\frac{\dot\omega}{\omega}\cos2\theta.
\]

它并非每一时刻严格为零；关键是右侧为快振荡，周期平均为零。若 ε=|ω̇|/ω²≪1，振荡造成的相对摆动为 O(ε)，首阶没有持续同号的累积。更一般的作用量–角变量变换给出同类结构：慢参数引入的角度周期项，其对角度的导数平均为零。

回旋运动的最低阶 Hamiltonian 正是这种谐振子，且 J_gyro=μmc/|q|，所以这一平均机制解释 μ 的绝热性。但靠近分界轨道、频率趋零、共振或快速参数变化时，「快振荡可以平均掉」不再成立。本例仅说明最低阶机制，不证明未经修正的瞬时 J 在所有情形下都有指数小误差。

## L3-B｜抗磁电流为何不能只把导心漂移相加

**插入位置**：Lecture 3「推导 4：抗磁性、磁化电流与 β」之后，并从 Lecture 2 的抗磁漂移辨析链接至此。原讲义 p.5–6；Lecture 2 p.10 脚注。

取直磁场 B(x)ẑ、缓变的垂直压强 p_⊥(x)，忽略此阶之外的极化电流和有限回旋半径修正。每粒子的磁矩平均满足 n⟨μ⟩=p_⊥/B。梯度漂移带来的导心电流是

\[
\mathbf j_{{\rm gc},\nabla B}
=nq\langle\mathbf V_{\nabla B}\rangle
=\frac{cp_\perp}{B^2}\mathbf b\times\nabla B.
\]

另一方面，磁化强度 M=−(p_⊥/B)b 产生

\[
\mathbf j_M=c\nabla\times\mathbf M
=\frac cB\mathbf b\times\nabla p_\perp
-\frac{cp_\perp}{B^2}\mathbf b\times\nabla B.
\]

两者相加，显式的 ∇B 项抵消：

\[
\boxed{\mathbf j_\perp=\frac cB\mathbf b\times\nabla p_\perp}.
\]

所以即使 B 完全均匀、每个导心没有 ∇B 漂移，只要回旋轨道的占据随位置不均匀，仍可有抗磁电流。反过来，只统计导心漂移会漏掉磁化电流。这里是直磁场下的局部一阶分解；弯曲磁场还要同时处理曲率漂移、磁化几何项和压强各向异性，自洽场还须满足 Ampère 方程及力平衡。

## L4-A｜相混合如何让可见扰动消失，却不增加细粒度熵

**插入位置**：Lecture 4「推导 6：Casimir 与细粒度熵守恒」之后。原讲义 p.6。

不必先讨论自洽波，最简单的自由输运已经展示相混合。取一维周期空间，

\[
\partial_t f+v\partial_xf=0,\qquad
f(x,v,0)=F(v)[1+a\cos kx],\quad |a|<1.
\]

沿特征线 x−vt=常数，精确解是

\[
f(x,v,t)=F(v)[1+a\cos k(x-vt)].
\]

若 F 为零均值 Maxwell 分布、方差 v_T²，则 Gaussian Fourier 积分给出

\[
\delta n(x,t)=a n_0\cos kx\,e^{-k^2v_T^2t^2/2}.
\]

密度扰动衰减了，但分布函数并未「忘记」扰动：它在速度方向形成尺度 Δv∼1/(|k|t) 的细纹。坐标剪切 (x,v)→(x−vt,v) 的 Jacobian 为 1，所以 ∫f ln f dx dv 不变。本例是自由相混合，不是自洽 Landau 阻尼的完整计算。

若仪器只分辨每个单元中的平均 f̄，凸函数 h(f)=f ln f 满足 Jensen 不等式

\[
h(\bar f)\leq\overline{h(f)},\qquad
-\int\bar f\ln\bar f\,dz\geq-\int f\ln f\,dz.
\]

粗粒度熵比同一时刻的细粒度熵更大，因此「看不见的细纹」可造成表观不可逆；但这条不等式本身不保证固定粗粒化下的熵每时每刻单调增加。回波与重现正提醒我们：丢失在观测分辨率之外的信息，不等于 Hamilton 动力学把信息销毁了。

## L4-B｜Gardner 重排怎样从定义变成可计算构造

**插入位置**：Lecture 4「推导 7：Gardner 重排与可用能上界」的交换论证之后。原讲义 p.7。

交换论证说明最低能分布要随能量递减，但还没有给出如何找到它。定义初态的「超水平集体积」

\[
\mathcal V_f(\eta)=\int\Theta(f_0(z)-\eta)\,dz,
\]

即分布值大于 η 的相空间体积。不可压缩重排保留所有 η 对应的 𝒱_f。对体积为 V_x 的均匀三维空间盒，动能低于 E 的相空间体积是

\[
\mathcal V_E(E)=V_x\frac{4\pi}{3}\left(\frac{2E}{m}\right)^{3/2}.
\]

构造最低能态时，把最大的 f 值依次填入最低能的相空间区域。若 f_G(E_η)=η，则匹配条件是

\[
\mathcal V_E(E_\eta)=\mathcal V_f(\eta).
\]

由两个单调函数求广义逆，即可计算 f_G，再积分得到 K_min。存在平台时用广义逆解释，不要求每个值都严格一一对应。

例如，均匀漂移 Maxwell 分布 F(v−U) 与无漂移 F(v) 的超水平集体积相同，因此不约束总动量的 Gardner 重排给 K_G=NmU²/2。但若实际系统还严格守恒总动量，而且没有其他动量储库，这部分整体漂移动能并不能全部提取。这个例子说明：仅用 Casimir 的最低能构造提供上界，实际可达态还受动量、场、几何等附加约束限制。

## L5-A｜为什么只保留小角碰撞的前两个统计矩

**插入位置**：Lecture 5「Kramers–Moyal 展开」的适用条件之后。原讲义 p.5–7。

Rutherford 小角散射给 χ∼|b₀|/b，而一次速度增量大小为 |Δv|∼uχ。遭遇权重是 nu·2πb db。因此第 r 阶增量率的数量级为

\[
M_r\sim nu^{r+1}|b_0|^r
\int_{b_{\min}}^{b_{\max}}b^{1-r}\,db.
\]

取经典 b_min∼|b₀|。r=2 给

\[
M_2\sim nu^3b_0^2\ln\Lambda.
\]

而 r>2 的非零项主要由短距端贡献，通常只有

\[
M_r\sim nu^{r+1}b_0^2,
\]

不再带大对数。下端的小角近似本身已失效，这里只作标度估计；使用完整散射角仍给出同类非对数贡献，不能靠此估计求出精确系数。若分布在速度尺度 u 上变化，r 阶 Kramers–Moyal 项还带 u⁻ʳ；于是较高阶项相对二阶项约小 1/lnΛ。平均纵向增量虽是一阶矩，却从 χ² 开始，因而同样保留对数贡献。方位对称性也会使部分奇次张量矩直接为零。

这说明 Landau/Fokker–Planck 近似首先是弱耦合下的「对数精度」近似，不是每一个真实碰撞都无限小。罕见大角事件给非对数修正；对尾部逃逸、稀有大能量转移等特别依赖这些事件的问题，仅靠 lnΛ 较大并不足以保证精度。

## L5-B｜同一 Lorentz 算子为什么有不同的弛豫频率

**插入位置**：Lecture 5「Lorentz 算子」的球坐标式之后。原讲义 p.8。

在固定速率 v 的球面上，将角分布展开为球谐函数：

\[
f(v,\theta,\varphi,t)=\sum_{\ell,m}f_{\ell m}(v,t)Y_{\ell m}(\theta,\varphi).
\]

利用 Δ_ΩY_ℓm=−ℓ(ℓ+1)Y_ℓm 和 C=(ν(v)/2)Δ_Ωf，得到

\[
f_{\ell m}(v,t)=f_{\ell m}(v,0)
\exp\!\left[-\frac{\ell(\ell+1)}2\nu(v)t\right].
\]

ℓ=0 的各向同性部分完全不变；ℓ=1 的偶极角分布按 ν 衰减，对应速度矢量的一阶矩；ℓ=2 的四极角分布按 3ν 衰减，对应无迹压力各向异性。因此，即使只有一种碰撞算子，「碰撞频率」「动量弛豫频率」「压力各向同性化频率」也可以不同。

若 ν 随 v 变化，将不同速率球面再积分之后，整体流速或整体压力未必遵循一个单指数。不能不加平均定义就把球面上的 ν(v) 替换成唯一的热碰撞频率。

## L5-C｜把 Rosenbluth 势真正算成 Maxwell 背景的慢化与扩散

**插入位置**：Lecture 5「Landau 核与 Rosenbluth 势」之后，作为可展开的计算例。原讲义 p.8–10，式 (34)、(36)–(40)。

设背景物种 b 静止、各向同性，

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

先算包围的速度空间粒子数 4π∫₀ᵛs²f_b(s)ds=n_bF(x)，便有 v²φ_b′=−n_bF(x)。在 v=0 处取正则解、无穷远取 φ_b∼n_b/v，继续积分得到

\[
\phi_b(v)=\frac{n_b}{v}\operatorname{erf}x,\qquad
\phi_b'=-\frac{n_b}{v^2}F(x),\quad
F(x)=\operatorname{erf}x-\frac{2x}{\sqrt\pi}e^{-x^2}.
\]

再由 (v²ψ_b′)′=2v²φ_b 积分，可写成

\[
\psi_b=n_b\left[\left(v+\frac{\sigma^2}{v}\right)\operatorname{erf}x
+\sqrt{\frac2\pi}\sigma e^{-x^2}\right].
\]

定义 G(x)=F(x)/(2x²)。直接求导得

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

令 Γ_sb=4πq_s²q_b²lnΛ_sb/m_s²，并沿用网页的 Kramers–Moyal 约定 C=−∂_i(A_if)+∂_i∂_j(B_ijf)，便得到

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

这里 B_⊥ 是每一个垂直方向的扩散系数，并不是两个方向之和。与原式 (34) 对照：

\[
\nu^{\rm slow}=\frac{\Gamma_{sb}n_b}{v^3}
\left(1+\frac{m_s}{m_b}\right)F,
\quad \nu^\parallel=\frac{2\Gamma_{sb}n_b}{v^3}G,
\quad \nu^\perp=\frac{2\Gamma_{sb}n_b}{v^3}(\operatorname{erf}x-G).
\]

**两个极限检验。** 当 v≫σ，F→1、G∼σ²/v²，所以 B_∥∼Γn_bσ²/v³，B_⊥∼Γn_b/(2v)：快粒子的速度扩散以改变方向为主。当 v→0，F∼4x³/(3√π)、G∼2x/(3√π)，于是

\[
B_\parallel=B_\perp\longrightarrow
\frac{\sqrt2\,\Gamma_{sb}n_b}{3\sqrt\pi\,\sigma},
\]

扩散恢复各向同性且有限，A 与 v 成正比。公式中看似奇异的 v⁻¹、v⁻³ 被 F、G 的小 x 行为抵消。

**为什么不能直接用 A 配 Einstein 关系？** 这里 ∇_v·B=Γ_sb∇_vφ_b，因此通量中的摩擦是

\[
\mathbf V=-\mathbf A+\nabla_v\cdot\mathsf B
=-\Gamma_{sb}\frac{m_s}{m_b}\nabla_v\phi_b,
\]

其质量系数是 m_s/m_b，而不是 A 中的 1+m_s/m_b。用 F=2x²G=v²G/σ² 可检查

\[
\mathbf V=\frac{m_s}{T_b}\mathsf B\cdot\mathbf v.
\]

因此温度为 T_b 的测试粒子 Maxwell 分布满足 V f+B·∇_vf=0。这个计算同时核对质量因子、扩散的 1/2 约定和共同温度平衡。

## L5-D｜从 H 定理的等号条件推出 Maxwell 分布，而不只是代入验证

**插入位置**：Lecture 5「Landau 对称积分形式」末尾；Lecture 7「局域 Maxwell 分布」链接至此。原讲义 Lecture 5 p.10；Lecture 7 p.5 脚注 3。

H 定理给出非负熵产生。对光滑、严格正、具有有限密度和能量的分布，等号要求每一对速度的横向投影消失：

\[
\mathsf U(\mathbf v-\mathbf v')
[\mathbf a_s(\mathbf v)-\mathbf a_{s'}(\mathbf v')]=0,
\qquad \mathbf a_s=\frac1{m_s}\nabla_v\ln f_s.
\]

先取同种粒子，并令 v′=v+δv。由于 U 只消去与 δv 平行的向量，Jacobian 矩阵 ∇a_s 必须把任意 δv 映到与它平行的方向，所以 ∇a_s=λ_s(v)I。不同分量的混合偏导相容性进一步要求 ∇λ_s=0，因而

\[
\mathbf a_s=\mathbf c_s+\lambda_s\mathbf v,
\quad
\ln f_s=A_s+m_s\mathbf c_s\cdot\mathbf v
+\frac{m_s\lambda_s}2v^2.
\]

可积性要求 λ_s<0。配方即得 Maxwell 分布，T_s=−1/λ_s、U_s=−c_s/λ_s。对于彼此有碰撞耦合的不同物种，再将这两个线性函数代回等号条件，可得 λ_s=λ_s′、c_s=c_s′：它们必须有共同温度和共同流速，而各物种密度可以不同。

这里的密度、共同流速与共同温度仍可依赖位置和时间：这是碰撞算子的局域平衡条件，并不自动满足完整动理学方程的输运与自洽场平衡。此结论依赖完整、相互连通的碰撞网络及上述正则性条件。只有 Lorentz 角散射时，速率方向没有耗散，等号条件不能唯一确定 Maxwell 分布；这正是两种模型的本质差别。

## L6-A｜从同一个 Vlasov 响应得到「冷流体」与「Boltzmann 电子」

**插入位置**：Lecture 6 的 Langmuir 与等温两组推导之间；可把两处重复的条件提醒改为链接。原讲义 p.7–10 的两种相速度极限。

取无磁、均匀 Maxwell 背景的一维纵向扰动，已把两个横向速度积分掉。设 f₁,φ₁∝eⁱᵏˣ⁻ⁱωᵗ，线性 Vlasov 方程给

\[
(-i\omega+ikv)f_1-\frac qm ik\phi_1 f_0'=0,
\qquad
f_1=\frac{q\phi_1}{m}\frac{f_0'}{v-\omega/k}.
\]

分母中的共振极点不能随便删掉。因果初值问题从 Imω>0 定义响应，再作 Landau 延拓。对 k>0，定义

\[
\zeta=\frac\omega{\sqrt2kv_T},\qquad
Z(\zeta)=\frac1{\sqrt\pi}\int_{\mathcal L}
\frac{e^{-u^2}}{u-\zeta}\,du.
\]

由 f₀′=−vf₀/v_T² 和 v/(v−ω/k)=1+(ω/k)/(v−ω/k)，速度积分得到

\[
\boxed{\frac{n_1}{n_0}=-\frac{q\phi_1}{T}[1+\zeta Z(\zeta)]}.
\]

**高相速度 |ζ|≫1。** 展开 1/(u−ζ)，奇次 Gaussian 矩为零，⟨u²⟩=1/2、⟨u⁴⟩=3/4，因此非共振的渐近部分为

\[
1+\zeta Z(\zeta)
=-\frac1{2\zeta^2}-\frac3{4\zeta^4}+\cdots,
\]

\[
\frac{n_1}{n_0}=\frac{qk^2\phi_1}{m\omega^2}
\left(1+\frac{3k^2v_T^2}{\omega^2}+\cdots\right).
\]

取单一响应物种、另一组分为固定中性化背景，代入 Poisson 方程便重现 ω²=ω_p²+3k²v_T²+…；系数 3 与压力矩推导一致。有限阶的这类代数展开不会得到一般的共振阻尼，不能把「实频率算对了」理解为完整动力学都已保留。

**低相速度 |ζ|≪1。** 对接近实轴的因果 Maxwell 响应，Z(ζ)=i√π−2ζ+…，所以

\[
\frac{n_1}{n_0}=-\frac{q\phi_1}{T}
[1+i\sqrt\pi\zeta-2\zeta^2+\cdots].
\]

主阶正是 Boltzmann 响应。后续虚部是相位滞后/共振响应，证明「忽略惯性」并不等于所有动力学修正都消失。离子声模型同时用电子的低相速度极限和离子的高相速度极限，需要 v_Ti≪|ω/k|≪v_Te；通常 Te≫Ti 才能使离子阻尼也小。这里不把原稿的无碰撞准静态假设说成碰撞热化。

## L6-B｜回旋对称压力的散度如何包含镜力和曲率力

**插入位置**：Lecture 6「强磁场与回旋对称」之后。原讲义 p.10–12。

令 Δp=p_∥−p_⊥，压力张量为 P=p_⊥I+Δp bb。按分量对乘积求导：

\[
\nabla\cdot\mathsf P=\nabla p_\perp
+\mathbf b\,\partial_\parallel\Delta p
+\Delta p[(\nabla\cdot\mathbf b)\mathbf b+\boldsymbol\kappa],
\quad \boldsymbol\kappa=(\mathbf b\cdot\nabla)\mathbf b.
\]

再用 ∇·b=−∂_∥lnB，得到平行与垂直分量：

\[
\mathbf b\cdot\nabla\cdot\mathsf P
=\partial_\parallel p_\parallel
+(p_\perp-p_\parallel)\partial_\parallel\ln B,
\]

\[
(\nabla\cdot\mathsf P)_\perp
=\nabla_\perp p_\perp+(p_\parallel-p_\perp)\boldsymbol\kappa.
\]

动量方程里的力为 −∇·P，所以这些式子不能只按 ∇p 的直觉写。若 p_∥ 很小且只看平行磁场梯度项，每粒子受力为

\[
-\frac{p_\perp}{n}\partial_\parallel\ln B
=-\langle\mu\rangle\partial_\parallel B,
\]

正是单粒子镜力的平均。压力张量的几何导数把第 2–3 讲的轨道物理带入流体方程；只保留两个压力标量而忽略 b 的空间变化，会把这一项丢失。

## L7-A｜把「繁琐但直接」的 BGK 高斯积分逐行算完

**插入位置**：Lecture 7「BGK 一阶闭合」已有学习补充处，用此段替代仅列矩的短提示，不重复放两份。原讲义 p.8，式 (39)–(42)。

记 a=v_T²=T/m、⟨h⟩=n⁻¹∫h g₀d³w，定义无迹二阶多项式 A_ij=w_iw_j−δ_ijw²/3。式 (39)–(40) 给

\[
\widetilde g=-\frac{g_0}{\nu}
\left[\left(\frac{w^2}{2a}-\frac52\right)
\frac{w_k\partial_kT}{T}
+\frac{A_{kl}}a\partial_lU_k\right].
\]

**先求应力。** 温度梯度项为奇函数，对 Π_ij 的积分为零。Gaussian 四阶矩给

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

**再求热流。** 剪切项为偶函数，对 Q_i 的积分为零。各向同性意味着 ⟨w_iw_jF(w²)⟩=δ_ij⟨w²F(w²)⟩/3，所以

\[
\begin{aligned}
Q_i&=-\frac{mn}{2\nu T}\partial_jT
\left\langle w_iw_jw^2\left(\frac{w^2}{2a}-\frac52\right)\right\rangle\\
&=-\frac{mn}{6\nu T}\partial_iT
\left[\frac{\langle w^6\rangle}{2a}-\frac52\langle w^4\rangle\right].
\end{aligned}
\]

代入 ⟨w⁴⟩=15a²、⟨w⁶⟩=105a³，方括号为 15a²，故

\[
\boxed{\mathbf Q=-\frac{5mn a^2}{2\nu T}\nabla T
=-\frac{5P}{2m\nu}\nabla T}.
\]

现在 η=P/ν 与 κ=5P/(2mν) 的每个系数都有来源。它们是这一个常频率、守恒型 BGK 近似的结果；不能期待它同时复现 Landau 算子对所有非平衡矩的不同弛豫率。

## L7-B｜零矩条件不只是选规范，还给出可解性检验

**插入位置**：Lecture 7「守恒零模」之后，或紧接上一段。原讲义 p.7–8，式 (35)–(39)。

线性碰撞算子的像必须与守恒的左零模相容。因此方程 Ĉg̃=源项的右侧必须具有零粒子数、零动量和零能量矩。只写 ∫g̃{1,w,w²}=0 固定解的定义，还不够；也应检查源项是否满足这些条件。

对本讲无磁、仅自碰撞的一阶驱动，剪切项的粒子数矩因 ⟨A_ij⟩=0 消失，动量矩因奇偶性消失，能量矩因

\[
\langle w^2w_iw_j\rangle=5a^2\delta_{ij},\qquad
\frac{\delta_{ij}}3\langle w^4\rangle=5a^2\delta_{ij}
\]

相消。温度梯度项的粒子数、能量矩是奇函数；其动量矩则需要真正计算：

\[
\left\langle w_iw_j\left(\frac{w^2}{2a}-\frac52\right)\right\rangle
=\left(\frac{5a^2}{2a}-\frac52a\right)\delta_{ij}=0.
\]

因此温度多项式里的 5/2 不只是代数巧合，它恰好去掉会改变局域流速的分量。一般 Chapman–Enskog 方法先用零阶流体方程消去时间导数，正是在保证这些可解性条件，而非随意丢掉时间演化。

## L7-C｜热流和黏性如何产生熵，Hall 项为什么不产生同类耗散

**插入位置**：Lecture 7「压力取迹」后可给守恒式，在「BGK 一阶闭合」后链接完成符号检验。原讲义 p.5–6、p.8；采用网页已校正的温度方程。

对单物种自碰撞、无外部热源，正确的三维内能式为

\[
\frac32nD_tT+P\nabla\cdot\mathbf U
=-\nabla\cdot\mathbf Q-\boldsymbol\Pi:\nabla\mathbf U.
\]

令每粒子熵 s=(3/2)lnT−lnn+常数，用连续性方程消去 D_tn，得到 nT D_ts=−∇·Q−Π:∇U。除以 T，并把热流散度改写为熵通量：

\[
\partial_t(ns)+\nabla\cdot\left(ns\mathbf U+\frac{\mathbf Q}{T}\right)
=-\frac{\mathbf Q\cdot\nabla T}{T^2}
-\frac{\boldsymbol\Pi:\nabla\mathbf U}{T}.
\]

对 Q=−κ∇T、Π=−ηW，其中 W=∇U+(∇U)ᵀ−(2/3)I∇·U，由 W 的对称无迹性有 W:∇U=W:W/2。因此

\[
\boxed{\sigma_{\rm entropy}=\frac{\kappa|\nabla T|^2}{T^2}
+\frac{\eta}{2T}W:W\geq0}.
\]

这也核查了应力负号：黏性使有序动能转化为热，不能使热源符号任意翻转。磁化热流中的 Q_×∝b×∇T 与 ∇T 正交，所以该项不直接贡献此处的局域熵产生；但它在系数或磁场方向不均匀时仍可能有非零散度，仍可重新分配热量。类似地，Hall 电流满足 E·j_H=0，但不代表 Hall 电流在每一种几何中都没有输运作用。

## L7-D｜碰撞摩擦与热源为什么必须成对满足同一个能量恒等式

**插入位置**：Lecture 7「物理解读与边界」的焦耳热解释之后。原讲义 p.10–11，式 (51h)、(52f)–(52g)。

把实验室系的碰撞能量源写成中心矩：

\[
\int\frac{m_sv^2}{2}C_s\,d^3v
=S_s+\mathbf U_s\cdot\mathbf R_s,
\]

因为 v=U_s+w，粒子数矩为零，交叉项恰为 U_s·R_s。对一对物种 a,b，碰撞保持总动量及总实验室系能量，因此

\[
\mathbf R_a+\mathbf R_b=0,
\qquad
S_a+S_b+\mathbf R_a\cdot(\mathbf U_a-\mathbf U_b)=0.
\]

取 a=e、b=i，马上得到

\[
S_{ei}=-S_{ie}+\mathbf R_{ei}\cdot(\mathbf U_i-\mathbf U_e),
\]

这不是独立猜出的加热项，而是总能量守恒强制要求的关系。若只保留摩擦 R_e=α(U_i−U_e)、α>0，则两物种内能增加总量为 α|U_i−U_e|²，正好抵消相对流动能的减少。

原式中的热力 R_e∝−∇T_e 还带有与热流配对的交叉项，不能把完整的 R_e·(U_i−U_e) 每一部分都单独理解成严格非负的纯电阻加热。

最后，用本讲单价、n_e=n_i=n、无流差与无空间输运的简化条件，式 (52g) 给

\[
\dot T_i=2\frac{m_e}{m_i}\nu_{ei}(T_e-T_i),\qquad
\dot T_e=-2\frac{m_e}{m_i}\nu_{ei}(T_e-T_i).
\]

因此两温差满足

\[
\frac d{dt}(T_e-T_i)=-4\frac{m_e}{m_i}\nu_{ei}(T_e-T_i).
\]

系数 4 属于这里“两边温度都允许改变”的条件；若离子是固定温度热浴，电子方程给系数 2。两者都说明温度交换时间比电子动量弛豫时间长约 m_i/m_e，不能用「电子碰撞快」直接推出 Te=Ti。ν_ei 随温度变化时，上式仍是瞬时方程，不是全程常系数单指数。

## 整合建议

- 以上 17 段均为由讲义现有方程进一步展开的教学补充，部分是跨讲桥梁。
- 建议默认展开 L1-A、L3-B、L5-B、L6-B、L7-A/B/D；较长的 Maxwell 背景计算、Vlasov 响应与 Gardner 构造可置于可展开推导。每个知识点保留一个主讲位置，用交叉链接避免重复。
