from pathlib import Path
import json
S=[]
def sec(title,pages,body): S.append(dict(title=title,pages=pages,body=body))
sec('阅读路线：从双流体到单流体 MHD','1–13',r'''
<p>MHD 把磁化等离子体视为导电流体，描述低频、长尺度动力学。本讲从一般流体矩方程出发，建立电阻 MHD，再取理想极限，最后推导剪切与压缩 Alfvén 波。液态金属同样适用，例如行星发电机与实验室液态金属实验。</p>
<p>逻辑链是：尺度排序 → 电子/离子近乎共速与准中性 → 广义欧姆定律 → 总动量方程 → 选择压强闭合 → 感应方程 → 线性波。<strong>长尺度、强磁化不自动保证标量压强；单流体近似与热力学闭合必须分别检查。</strong></p>
<p>沿用高斯单位制；温度以能量计，\(v_{Ti}=\sqrt{T_i/m_i}\)，\(\rho_i=v_{Ti}/\Omega_i\)，\(\rho_m\) 表示质量密度，避免与回旋半径混淆。除特别说明，尺度估计取 \(T_e\sim T_i\sim T\)。原件更新于 2026-11-10，共13页；本文覆盖原式(1)–(55)、3幅图、12道自测题。新增推导与校注明确标识，原 PDF 完整保留。</p>
''')
sec('MHD 排序与离子惯性长度','1–2',r'''
<p>考虑非相对论、单价单离子组分等离子体。本讲采用以下排序；不同 MHD 版本可以有不同排序，不应把它当成唯一可能定义。</p>
$$\epsilon\equiv\frac{\rho_i}{L}\sim\frac{\omega}{\Omega_i}\ll1,\qquad \beta\equiv\frac{nT}{B^2/(8\pi)}\sim1,\qquad \frac{U_e}{v_{Ti}}\sim\frac{U_i}{v_{Ti}}\sim1.\tag{L8-1}$$
$$\delta_i\equiv\frac{c}{\omega_{pi}},\qquad V_A\equiv\frac{B}{\sqrt{4\pi\rho_m}},\qquad \rho_m\simeq nm_i.\tag{L8-2}$$
$$\frac{\delta_i}{\rho_i}=\frac{V_A}{v_{Ti}}\sim\beta^{-1/2}\sim1.\tag{L8-3}$$
$$U_e\sim U_i\sim V_A,\qquad \frac{V_A}{c}\sim\frac{v_{Ti}}c\ll1.\tag{L8-4}$$
<p><strong>学习补充：</strong>由 \(\Omega_i\delta_i=V_A\) 立即得式(3)。若严格采用上述 \(\beta\) 与热速度定义，比例为 \(\sqrt{2/\beta}\)；原文只保留量级。这里的 \(nT\) 是尺度，不应与总压强 \(P=n_eT_e+n_iT_i\) 混用。\(\delta_i\) 是 ion <em>skin</em> depth，原件“skip”是笔误。</p>
<p>聚变等离子体平均自由程可能达公里量级，不能一般地从 \(\lambda_{\rm mfp}/L\ll1\) 的 Braginskii 理论直接推出本讲所有闭合。</p>
''')
sec('为何忽略位移电流，以及为何两种流体近乎共速','2',r'''
<p>低频横向响应包含极化电流，\(j_{\rm pol}\sim(nm_ic^2/B^2)\omega E\)。按该尺度估计，位移电流相对传导电流很小：</p>
$$\frac{|c^{-1}\partial_t\mathbf E|}{|(4\pi/c)\mathbf j|}\lesssim\frac{V_A^2}{c^2}\ll1.\tag{L8-5}$$
$$\nabla\times\mathbf B=\frac{4\pi}{c}\mathbf j.\tag{L8-6}$$
<p>低频且 \(V_A\ll c\) 是这一磁准静态近似的核心；\(\beta\sim1\) 只是本讲建立它的一条路径。以 \(L\) 为磁场变化尺度：</p>
$$j\sim\frac{cB}{4\pi L}=neV_A\frac{\delta_i}{L}\sim\epsilon neV_A.\tag{L8-7}$$
$$\frac{|\mathbf U_i-\mathbf U_e|}{U_{e,i}}\simeq\frac{j}{neU_{e,i}}\sim\epsilon\ll1.\tag{L8-8}$$
<p>这里先用近准中性的电流尺度，下一节由高斯定律核实其自洽性。单流体并非电子与离子速度完全相等：它们的微小差产生有限电流，不能在洛伦兹力中一并抹去。</p>
''')
sec('电子动量与有效摩擦：先区分定律和闭合','2–3',r'''
$$m_en_e\frac{D_e\mathbf U_e}{Dt}=-en_e\left(\mathbf E+\frac{\mathbf U_e}{c}\times\mathbf B\right)-\nabla\cdot\mathbf P_e+\mathbf R_{ei}.\tag{L8-9}$$
$$\frac{\mathbf U_e\cdot\nabla}{\partial_t}\sim\frac{v_{Ti}}{\omega L}=\frac{\Omega_i}{\omega}\frac{\rho_i}{L}\sim1,\qquad D_e/Dt=\partial_t+\mathbf U_e\cdot\nabla.\tag{L8-10}$$
<p>惯性中的对流项通常与时间导数同阶。对弱碰撞等离子体，局域 Braginskii 摩擦（尤其平行热力项）未必适用。本讲选用现象学闭合：</p>
$$\mathbf R_{ei}=m_en_e\nu_{ei}(\mathbf U_i-\mathbf U_e)\simeq\frac{m_e\nu_{ei}}e\mathbf j=\frac{n_ee}{\sigma}\mathbf j,\qquad \sigma=\frac{n_ee^2}{m_e\nu_{ei}}.\tag{L8-11}$$
<p>它是相对流速的一阶近似；一般摩擦系数可为张量，这里简化为标量。有效 \(\nu_{ei}\) 不必等于经典碰撞频率。所需条件是 \(\epsilon\nu_{ei}/|\Omega_e|\ll1\)，并非假定碰撞足够强。</p>
''')
sec('电子主平衡：电场如何出现','3',r'''
<p>以电子磁力尺度 \(enV_AB/c\) 归一化，各项大小为：</p>
$$\frac{m_en\omega V_A}{enV_AB/c}\sim\frac{\omega}{|\Omega_e|}\sim\epsilon\frac{m_e}{m_i}\ll1,\tag{L8-12}$$
$$\frac{|\nabla\cdot\mathbf P_e|}{enV_AB/c}\sim\frac{nT/L}{enV_AB/c}\sim\frac{v_{Ti}}{V_A}\frac{\rho_i}{L}\sim\epsilon,\tag{L8-13}$$
$$\frac{R_{ei}}{enV_AB/c}\sim\epsilon\frac{\nu_{ei}}{|\Omega_e|}\ll1.\tag{L8-14}$$
<p>因而垂直电场与磁力的主项相抵：</p>
$$E\sim\frac{V_A}{c}B\sim\frac{v_{Ti}}cB.\tag{L8-15}$$
<p><strong>学习补充：</strong>这不是平行电场必须同样大的结论。磁力没有平行分量，\(E_\parallel\) 由压强、摩擦或电子惯性等较小项决定。将此电场尺度代回极化电流可得 \(j_{\rm pol}\sim\epsilon neV_A\)，与安培定律估计相容。</p>
''')
sec('准中性与质心流速','3',r'''
<p>高斯定律估计电荷分离：</p>
$$\frac{|n_e-n_i|}{n}\sim\frac{E}{4\pi neL}\sim\frac{\lambda_D^2}{\rho_iL}\sim\epsilon\frac{\Omega_i^2}{\omega_{pi}^2}=\epsilon\frac{V_A^2}{c^2}\ll1.\tag{L8-16}$$
<p>这里 \(\lambda_D^2\sim T/(4\pi ne^2)\)；忽略物种相关的阶一因子。故可令 \(n_e\simeq n_i\equiv n\)。质心速度与离子速度仅相差电子质量修正：</p>
$$\mathbf U\equiv\frac{n_em_e\mathbf U_e+n_im_i\mathbf U_i}{n_em_e+n_im_i}\simeq\mathbf U_i.\tag{L8-17}$$
$$\mathbf U_e\simeq\mathbf U-\frac{\mathbf j}{ne}=\mathbf U+O(\epsilon V_A),\tag{L8-18}$$
$$\frac{\mathbf U_e\times\mathbf B}{c}\simeq\frac{\mathbf U\times\mathbf B}{c}-\frac{\mathbf j\times\mathbf B}{nec}.\tag{L8-19}$$
<p><strong>学习补充：</strong>在严格准中性下，\(\mathbf U_i-\mathbf U=[m_e/(m_i+m_e)]\mathbf j/(ne)\)，所以误差其实为 \(O[(m_e/m_i)\epsilon V_A]\)。准中性不代表电场为零；它只说维持该电场所需的相对电荷不平衡很小。</p>
''')
sec('广义欧姆定律：Hall 项与压强项从哪里来','4',r'''
<p>在电子动量式中略去最小的电子惯性，除以 \(en\)，再代入电子流速：</p>
$$\mathbf E+\frac{\mathbf U\times\mathbf B}{c}=\frac{\mathbf j\times\mathbf B}{nec}-\frac{\nabla\cdot\mathbf P_e}{en}+\frac{\mathbf j}{\sigma}.\tag{L8-20a}$$
$$\frac{\mathbf j}{\sigma}=\mathbf E'-\frac{\mathbf j\times\mathbf B}{nec}+\frac{\nabla\cdot\mathbf P_e}{en},\qquad \mathbf E'=\mathbf E+\frac{\mathbf U\times\mathbf B}{c}.\tag{L8-20b}$$
<p>Hall 项来自电子与质心的相对运动；压强项来自电子内应力；电阻项来自摩擦。\(\mathbf E'\) 是低速变换下流体静止系电场。左侧电磁主项相消，不能把“小的净电场”误认为两个大项各自都小。</p>
<p>忽略 Hall 和压强项后，\(\mathbf j=\sigma\mathbf E'\) 才是最简单的欧姆定律。电流变换本有 \(-\rho_q\mathbf U\)，但 \(\rho_q U/j\sim V_A^2/c^2\ll1\)，因此此处可以忽略（原脚注3）。</p>
''')
sec('电阻与理想欧姆定律：选择保留哪种物理','4',r'''
$$\mathbf j=\sigma\left(\mathbf E+\frac{\mathbf U\times\mathbf B}{c}\right).\tag{L8-21}$$
$$\mathbf E+\frac{\mathbf U\times\mathbf B}{c}=0\qquad(\sigma\to\infty).\tag{L8-22}$$
<p>电阻 MHD 保留耗散，理想 MHD 再令电阻为零。本讲略去 Hall/电子压强修正而保留电阻，不是声称电阻一定更大，而是选择一个能表达不可逆效应的最小模型。</p>
<p><strong>适用边界：</strong>当 \(L\sim\delta_i\)、电子压强梯度对电场重要、或需要解析重联微观层时，这种取舍会失效。局部理想欧姆定律给出 \(\mathbf E\cdot\mathbf B=0\)；磁通冻结还需与法拉第定律、光滑流场共同使用。</p>
''')
sec('相加双流体动量方程：内部摩擦消失','4–5',r'''
$$m_en_e\frac{D_e\mathbf U_e}{Dt}=-en_e\left(\mathbf E+\frac{\mathbf U_e\times\mathbf B}{c}\right)-\nabla\cdot\mathbf P_e+\mathbf R_{ei},\tag{L8-23a}$$
$$m_in_i\frac{D_i\mathbf U_i}{Dt}=+en_i\left(\mathbf E+\frac{\mathbf U_i\times\mathbf B}{c}\right)-\nabla\cdot\mathbf P_i+\mathbf R_{ie}.\tag{L8-23b}$$
<p>相加时 \(\mathbf R_{ei}+\mathbf R_{ie}=0\)，磁力合为 \(\mathbf j\times\mathbf B/c\)。在所取精度下，左侧归并为质心惯性：</p>
$$\rho_m\frac{D\mathbf U}{Dt}=e(n_i-n_e)\mathbf E+\frac{\mathbf j\times\mathbf B}{c}-\nabla\cdot\mathbf P,\qquad \mathbf P=\mathbf P_e+\mathbf P_i.\tag{L8-24}$$
<p><strong>学习补充：</strong>精确相加还含相对漂移动量通量 \(\sum_s m_sn_s\mathbf w_s\mathbf w_s\)，\(\mathbf w_s=\mathbf U_s-\mathbf U\)。其尺度约为 \(nm_e(j/ne)^2\)，相对 \(\rho_mU^2\) 是 \((m_e/m_i)\epsilon^2\)，此处忽略。</p>
''')
sec('电荷力的量级校核与单流体运动方程','5',r'''
<p>用前面的 \(j\sim\epsilon neV_A\)、\(E\sim V_AB/c\) 和电荷不平衡估计：</p>
$$\frac{|\rho_q\mathbf E|}{|\mathbf j\times\mathbf B|/c}\sim\frac{|n_i-n_e|}{n}\frac1\epsilon\sim\frac{V_A^2}{c^2}\ll1.\tag{L8-25校}$$
<p><strong>原式校注：</strong>原式(25)写为 \(\epsilon |n_i-n_e|/n\sim\epsilon^2V_A^2/c^2\)，但 \(neV_A/j\sim1/\epsilon\)，并不是 \(\epsilon\)。改正后仍可忽略电荷力。此为特征力尺度比较；若局部 \(\mathbf j\parallel\mathbf B\)，不能将实际为零的磁力放在分母。</p>
$$\rho_m\frac{D\mathbf U}{Dt}=\frac{\mathbf j\times\mathbf B}{c}-\nabla\cdot\mathbf P.\tag{L8-26}$$
<p>摩擦是物种间内部力，不出现在总动量方程中；但它把相对流动能转成热，仍会出现在能量方程。</p>
''')
sec('磁压力、磁张力与 Maxwell 应力','5',r'''
$$\frac{\mathbf j\times\mathbf B}{c}=\frac{(\nabla\times\mathbf B)\times\mathbf B}{4\pi}=\frac{(\mathbf B\cdot\nabla)\mathbf B}{4\pi}-\nabla\frac{B^2}{8\pi}.\tag{L8-27}$$
$$\rho_m\frac{D\mathbf U}{Dt}=\frac{(\mathbf B\cdot\nabla)\mathbf B}{4\pi}-\nabla\cdot\left(\frac{B^2}{8\pi}\mathbf I+\mathbf P\right).\tag{L8-28}$$
<p><strong>学习补充：</strong>令 \(\mathbf B=B\mathbf b\)，则 \((\mathbf B\cdot\nabla)\mathbf B=B\partial_\parallel B\,\mathbf b+B^2\boldsymbol\kappa\)，\(\boldsymbol\kappa=(\mathbf b\cdot\nabla)\mathbf b\)。磁压力的平行分量恰好抵消第一项，剩下：</p>
$$\frac{\mathbf j\times\mathbf B}{c}=\frac{B^2}{4\pi}\boldsymbol\kappa-\nabla_\perp\frac{B^2}{8\pi}.$$
<p>前者是曲率张力，后者是磁压力梯度。磁应力张量为 \(\mathbf T_B=\mathbf{BB}/4\pi-(B^2/8\pi)\mathbf I\)，其散度给出磁力。电应力相对小 \(E^2/B^2\sim V_A^2/c^2\)。注意“磁张力”并不意味着磁力能沿磁场加速流体。</p>
''')
sec('闭合是额外假设：CGL、标量压强与单温度','5–6',r'''
<p>动量方程本来包含压强张量。冷等离子体可以忽略它；低 \(\beta\) 对以磁力主导的运动常可作此近似，但不能据此忽略所有平行声学效应。无碰撞、磁化、可忽略热流等适当极限下，CGL 给出双绝热闭合：</p>
$$\frac{D}{Dt}\left(\frac{P_\perp}{nB}\right)=0,\qquad \frac{D}{Dt}\left(\frac{P_\parallel B^2}{n^3}\right)=0.$$
<p>碰撞足够快可促成物种内部近 Maxwell 分布，支持标量压强；电子离子同温还要求更慢的能量交换足够快，即 \((m_e/m_i)\nu_{ei}\gg\omega\)。此处需用真实库仑能量交换率；若前文的 \(\nu_{ei}\) 只是有效摩擦率，应另设温度弛豫率 \(\nu_{T,ei}\gg\omega\)，不能自动推定同温。这些条件互不等价。</p>
$$\frac32 n_p\frac{DT}{Dt}+P\nabla\cdot\mathbf U=S-\nabla\cdot\mathbf Q-2\boldsymbol\Pi:\nabla\mathbf U,\qquad P=n_pT,\quad n_p=n_e+n_i\simeq2n.\tag{L8-29}$$
<p>上式保留原式(29)的 \(2\boldsymbol\Pi\) 记法；若 \(\boldsymbol\pi\) 定义为两物种总非标量应力，标准项是 \(-\boldsymbol\pi:\nabla\mathbf U\)，此处须识别 \(\boldsymbol\pi=2\boldsymbol\Pi\)，不能把两种约定混用。温度无需人为重定义：同温时总压强就是 \(2nT\)。</p>
''')
sec('横向输运小，不等于平行闭合已解决','6',r'''
<p>强磁化限制横向输运；在 \(\nu_{ii}/\Omega_i\ll1\) 下，Braginskii 的横向标度可作定性参考：</p>
$$\frac{\Pi_\times}{P}\sim\frac{U}{\Omega_iL}\sim\epsilon,\qquad \frac{\Pi_\perp}{P}\sim\frac{\nu_{ii}}{\Omega_i}\frac{\Pi_\times}{P}\sim\epsilon\frac{\nu_{ii}}{\Omega_i}.\tag{L8-30}$$
<p><strong>原式校注：</strong>原式(31)排为 \(Q_\times\sim Pv_{Ti}^2/\Omega_i\)、\(Q_\perp\sim\nu_{ii}Pv_{Ti}^2/(m\Omega_i^2)\)，缺失梯度尺度且多出质量因子，按热流量纲不能成立。若温度变化尺度是 \(L\)，与前讲输运相容的量级是：</p>
$$Q_\times\sim\frac{Pv_{Ti}^2}{\Omega_iL},\qquad Q_\perp\sim\frac{\nu_{ii}}{\Omega_i}\frac{Pv_{Ti}^2}{\Omega_iL}.\tag{L8-31校}$$
$$\frac{|\boldsymbol\Pi_\times:\nabla\mathbf U|}{Pv_{Ti}/L}\lesssim\epsilon,\quad \frac{|\boldsymbol\Pi_\perp:\nabla\mathbf U|}{Pv_{Ti}/L}\sim\epsilon\frac{\nu_{ii}}{\Omega_i},\quad \frac{|\nabla\cdot\mathbf Q_\times|}{Pv_{Ti}/L}\lesssim\epsilon,\quad \frac{|\nabla\cdot\mathbf Q_\perp|}{Pv_{Ti}/L}\lesssim\epsilon\frac{\nu_{ii}}{\Omega_i}.\tag{L8-32校}$$
<p>原式(32)最后一个分子印为 \(Q_\perp\)，应比较其散度；这里按一致量纲列出。上界可因几何抵消而更小。对标准 Braginskii 回旋黏性，应力与同一速度梯度的收缩实际为零，属于非耗散项；上式仅列一般幅值上界。这些横向估计<strong>不能消除 \(P_\parallel-P_\perp\) 或证明平行热流很小</strong>。弱碰撞的沿场动力学仍可能需要动理学闭合。</p>
''')
sec('焦耳热：内部摩擦如何成为热源','6',r'''
$$S=S_{ei}+S_{ie}=\mathbf R_{ei}\cdot(\mathbf U_i-\mathbf U_e)=\frac{ne}{\sigma}\mathbf j\cdot\frac{\mathbf j}{ne}=\frac{j^2}{\sigma}\ge0.\tag{L8-33}$$
<p><strong>学习补充：</strong>电子和离子摩擦的总机械功为 \(\mathbf R_{ei}\cdot\mathbf U_e+\mathbf R_{ie}\cdot\mathbf U_i=-S\)。失去的定向动能恰好成为内部热能；能量交换项在物种求和后抵消，摩擦生热不抵消。</p>
$$\frac{S}{Pv_{Ti}/L}\sim\epsilon\frac{m_e}{m_i}\frac{\nu_{ei}}{\Omega_i}\sim\epsilon\sqrt{\frac{m_e}{m_i}}\frac{\nu_{ii}}{\Omega_i}.\tag{L8-34}$$
<p>最后一步使用同温经典碰撞率关系 \(\nu_{ei}\sim\sqrt{m_i/m_e}\,\nu_{ii}\)，不能对任意现象学有效碰撞率直接套用。若省略所有小量，热流、黏性与焦耳热都不保留；若只保留焦耳热，则是在挑选最小耗散模型，而不是严格保留所有同阶项。</p>
''')
sec('绝热状态方程：从温度式到熵守恒','6–7',r'''
$$\frac32\frac{DT}{Dt}+T\nabla\cdot\mathbf U=0,\qquad \frac{D}{Dt}\left(\frac{T}{n^{2/3}}\right)=0.\tag{L8-35}$$
<p>使用连续性方程 \(D\ln n/Dt=-\nabla\cdot\mathbf U\)，得到 \(D\ln T/Dt=(2/3)D\ln n/Dt\)。再由 \(P=2nT\)、\(\rho_m\simeq m_in\)：</p>
$$\frac{D}{Dt}\left(\frac{P}{\rho_m^{5/3}}\right)=0.\tag{L8-36}$$
<p><strong>学习补充：</strong>等价形式为 \(DP/Dt+\gamma P\nabla\cdot\mathbf U=0\)，\(\gamma=5/3\)。它沿流线守恒的是比熵的函数，而不是温度或压强。对弱碰撞聚变等离子体，这通常是各向同性、保守的最小模型，不能无条件声称由碰撞严格推出。</p>
<p>另一种保守选择是不可压缩模型 \(\nabla\cdot\mathbf U=0\)：此时压强由约束决定，是维持不可压缩性的拉格朗日乘子，绝非可以设为零（原脚注5）。</p>
''')
sec('电阻 MHD 的热力学方程','7',r'''
<p>保留焦耳热，仍忽略热流和黏性，得到：</p>
$$2n\left(\frac32\frac{DT}{Dt}+T\nabla\cdot\mathbf U\right)=\frac{j^2}{\sigma}.\tag{L8-37}$$
$$\frac{D}{Dt}\left(\frac{P}{\rho_m^{5/3}}\right)=\frac{2j^2}{3\sigma\rho_m^{5/3}}.\tag{L8-38}$$
<p><strong>学习补充：</strong>对 \(P=n_pT\) 求物质导数，\(DP/Dt=n_pDT/Dt-P\nabla\cdot\mathbf U\)。代入式(37)可得 \(DP/Dt+\gamma P\nabla\cdot\mathbf U=(\gamma-1)j^2/\sigma\)，再乘 \(\rho_m^{-\gamma}\) 即得式(38)。</p>
<p>熵源非负。原文强调，被省略的输运项可能比焦耳热更大；此式适合表达电阻耗散的定性作用，实际温度演化常需更完整的能量闭合。</p>
''')
sec('质量守恒与磁感应方程','7',r'''
$$\partial_t\rho_m+\nabla\cdot(\rho_m\mathbf U)=0.\tag{L8-39}$$
<p>质量密度约为 \(m_in\)，所以离子连续性给出质量守恒。磁场演化由法拉第定律与电阻欧姆定律共同确定：</p>
$$\begin{aligned}\partial_t\mathbf B&=-c\nabla\times\mathbf E\\&=\nabla\times(\mathbf U\times\mathbf B)-\frac{c^2}{4\pi}\nabla\times\left(\frac1\sigma\nabla\times\mathbf B\right)\\&=\nabla\times(\mathbf U\times\mathbf B)+\frac{c^2}{4\pi\sigma}\nabla^2\mathbf B.\end{aligned}\tag{L8-40}$$
<p>最后一步要求 \(\sigma\) 为常数，并使用 \(\nabla\times\nabla\times\mathbf B=\nabla(\nabla\cdot\mathbf B)-\nabla^2\mathbf B\)、\(\nabla\cdot\mathbf B=0\)。若电导率随位置变化，必须保留前一行的旋度形式。</p>
''')
sec('磁扩散率、冻结磁通与时间尺度','7–8',r'''
$$\partial_t\mathbf B=\nabla\times(\mathbf U\times\mathbf B)+\eta\nabla^2\mathbf B,\tag{L8-41}$$
$$\eta\equiv\frac{c^2}{4\pi\sigma}=\nu_{ei}\frac{m_ec^2}{4\pi ne^2}=\nu_{ei}\delta_e^2,\qquad\delta_e=c/\omega_{pe}.\tag{L8-42}$$
$$\partial_t\mathbf B=\nabla\times(\mathbf U\times\mathbf B)\qquad(\eta\to0).\tag{L8-43}$$
<p>\(\eta\) 的量纲是长度平方/时间，是<strong>磁扩散率</strong>，不是 \(1/\sigma\)。SI 制下磁扩散率为 \(1/(\mu_0\sigma)\)，两种单位制都不能混称（原脚注6）。</p>
<p><strong>学习补充：</strong>磁雷诺数 \(R_m=UL/\eta\) 比较对流与扩散，扩散时间 \(\tau_\eta=L^2/\eta\)。无流时傅里叶模按 \(e^{-\eta k^2t}\) 衰减；理想极限的移动曲面满足 \(d\int_{S(t)}\mathbf B\cdot d\mathbf S/dt=-c\oint[\mathbf E+\mathbf U\times\mathbf B/c]\cdot d\boldsymbol\ell=0\)，即磁通冻结。感应方程的旋度形式还保证初始 \(\nabla\cdot\mathbf B=0\) 持续成立。</p>
''')
sec('完整方程组：把动力学与闭合一起记','8',r'''
$$\epsilon=\rho_i/L\sim\omega/\Omega_i\ll1,\quad\beta\sim1,\quad U_{e,i}\sim v_{Ti},\quad V_A\ll c.\tag{L8-44}$$
<p>单温度的经典库仑碰撞依据另需 \((m_e/m_i)\nu_{ei}\gg\omega\)；弱碰撞应用的标量闭合则应明确视作模型选择。对常数电导率：</p>
$$\partial_t\rho_m+\nabla\cdot(\rho_m\mathbf U)=0,\tag{L8-45a}$$
$$\rho_m(\partial_t+\mathbf U\cdot\nabla)\mathbf U=\mathbf j\times\mathbf B/c-\nabla P,\tag{L8-45b}$$
$$\frac{D}{Dt}(P/\rho_m^{5/3})=\frac{2j^2}{3\sigma\rho_m^{5/3}},\tag{L8-45c}$$
$$\partial_t\mathbf B=\nabla\times(\mathbf U\times\mathbf B)+\eta\nabla^2\mathbf B,\tag{L8-45d}$$
$$\mathbf j=\frac c{4\pi}\nabla\times\mathbf B,\tag{L8-45e}$$
$$\nabla\cdot\mathbf B=0,\tag{L8-45f}$$
$$\rho_m\frac{D\mathbf U}{Dt}=\frac{(\mathbf B\cdot\nabla)\mathbf B}{4\pi}-\nabla\left(P+\frac{B^2}{8\pi}\right).\tag{L8-45g}$$
<p>未知量可取 \((\rho_m,\mathbf U,P,\mathbf B)\)，电流由安培定律确定，电场由欧姆定律确定。理想极限删除热源和磁扩散项，采用理想欧姆定律。式(45g)只是(45b)的等价形式，不是额外方程。原文建议记住排序及主要方程，热源系数可不强记。</p>
''')
sec('学习补充：能量收支与静态平衡','8',r'''
<p>令 \(u=P/(\gamma-1)\)、\(K=\rho_mU^2/2\)。动量式点乘速度，加上内能式和 Poynting 定理：</p>
$$\partial_t(K+u)+\nabla\cdot[(K+u+P)\mathbf U]=\mathbf U\cdot(\mathbf j\times\mathbf B/c)+j^2/\sigma,$$
$$\partial_t\frac{B^2}{8\pi}+\nabla\cdot\frac{c\mathbf E\times\mathbf B}{4\pi}=-\mathbf j\cdot\mathbf E,$$
$$\mathbf j\cdot\mathbf E=\mathbf U\cdot(\mathbf j\times\mathbf B/c)+j^2/\sigma.$$
<p>相加后机械功和焦耳热相消，总能量守恒（边界能流除外）；电阻把磁能转热，而非凭空损失总能量。静态、标量压强平衡则为 \(\nabla P=\mathbf j\times\mathbf B/c\)，点乘磁场得 \(\mathbf B\cdot\nabla P=0\)。这正是磁约束平衡计算中“压强沿磁力线常数”的出发点；它不单独保证每条磁力线都形成完整磁面。</p>
''')
sec('Alfvén 波：均匀、冷等离子体的线性化','9–10',r'''
<p>以下另取理想 MHD、低 \(\beta\)（冷等离子体）极限，背景静止且均匀。虽然前面的演示排序取 \(\beta\sim1\)，波动部分采用低 \(\beta\) 的特例，只要低频、磁化与 \(V_A\ll c\) 等近似仍成立。</p>
$$\mathbf U=\widetilde{\mathbf U},\qquad\mathbf B=\mathbf B_0+\widetilde{\mathbf B},\qquad\mathbf B_0=B_0\mathbf b_0.\tag{L8-46}$$
$$\rho_{m0}\partial_t\widetilde{\mathbf U}=\frac{(\mathbf B_0\cdot\nabla)\widetilde{\mathbf B}}{4\pi}-\nabla\frac{\mathbf B_0\cdot\widetilde{\mathbf B}}{4\pi},\qquad \partial_t\widetilde{\mathbf B}=\nabla\times(\widetilde{\mathbf U}\times\mathbf B_0).\tag{L8-47}$$
<p>密度扰动不乘背景加速度，因此不进入这里的一阶动量式，但仍可由连续性方程求出。Alfvén 于1942年预测此类波，1970年因磁流体力学工作获诺贝尔物理学奖；原件图1保留其1942年论文全页。</p>
{{FIG1}}
''')
sec('从线性方程到波动算符','9',r'''
<p>定义无量纲扰动 \(\widetilde{\mathbf b}=\widetilde{\mathbf B}/B_0\)，\(\partial_\parallel=\mathbf b_0\cdot\nabla\)：</p>
$$\partial_t\widetilde{\mathbf U}=V_A^2(\partial_\parallel\widetilde{\mathbf b}-\nabla\widetilde b_\parallel),\qquad\partial_t\widetilde{\mathbf b}=\nabla\times(\widetilde{\mathbf U}\times\mathbf b_0).\tag{L8-48}$$
$$\partial_t^2\widetilde{\mathbf b}=V_A^2\nabla\times[(\partial_\parallel\widetilde{\mathbf b}-\nabla\widetilde b_\parallel)\times\mathbf b_0].\tag{L8-49}$$
<p>代入 \(e^{i\mathbf k\cdot\mathbf x-i\omega t}\)，并使用 \(\mathbf k\cdot\widetilde{\mathbf b}=0\)：</p>
$$\begin{aligned}(\omega/V_A)^2\widetilde{\mathbf b}&=\mathbf k\times[(k_\parallel\widetilde{\mathbf b}-\mathbf k\widetilde b_\parallel)\times\mathbf b_0]\\&=k_\parallel^2\widetilde{\mathbf b}-\mathbf k k_\parallel\widetilde b_\parallel+k^2\mathbf b_0\widetilde b_\parallel\\&=k_\parallel^2\widetilde{\mathbf b}-\mathbf k_\perp k_\parallel\widetilde b_\parallel+k_\perp^2\mathbf b_0\widetilde b_\parallel.\end{aligned}\tag{L8-50}$$
<p><strong>学习补充：</strong>使用 \(\mathbf a\times(\mathbf b\times\mathbf c)=\mathbf b(\mathbf a\cdot\mathbf c)-\mathbf c(\mathbf a\cdot\mathbf b)\)。未使用散度约束前，右侧还有 \(-\mathbf b_0k_\parallel(\mathbf k\cdot\widetilde{\mathbf b})\) 项；这正是下一节两个矩阵写法的差别。</p>
''')
sec('色散矩阵：散度约束与多出来的零根','9',r'''
<p>取 \(\mathbf b_0=\hat{\mathbf z}\)、\(\mathbf k=(k_\perp,0,k_\parallel)\)，记 \(q=(\omega/V_A)^2\)。先施加散度约束的写法是：</p>
$$\begin{pmatrix}q-k_\parallel^2&0&k_\perp k_\parallel\\0&q-k_\parallel^2&0\\0&0&q-k^2\end{pmatrix}\widetilde{\mathbf b}=0.\tag{L8-51}$$
<p>未先代入约束时得到对称矩阵：</p>
$$\begin{pmatrix}q-k_\parallel^2&0&k_\perp k_\parallel\\0&q-k_\parallel^2&0\\k_\perp k_\parallel&0&q-k_\perp^2\end{pmatrix}\widetilde{\mathbf b}=0.\tag{L8-52}$$
<p><strong>学习补充：</strong>对称矩阵的行列式为 \(q(q-k_\parallel^2)(q-k^2)\)。一般 \(\mathbf k\ne0\) 时，额外 \(q=0\) 的纵向磁扰动 \(\widetilde{\mathbf b}\parallel\mathbf k\) 违反 \(\mathbf k\cdot\widetilde{\mathbf b}=0\)，须剔除。故两支传播解是 \(\omega^2=k_\parallel^2V_A^2\) 和 \(\omega^2=k^2V_A^2\)。在垂直传播等退化方向，零频物理解需另查，不能把所有零根一概删除。</p>
''')
sec('剪切 Alfvén 波：磁张力与沿场能量传播','11',r'''
$$\omega^2=k_\parallel^2V_A^2,\qquad\widetilde{\mathbf b}=\widetilde b_y\hat{\mathbf y},\quad\widetilde{\mathbf U}=\widetilde U_y\hat{\mathbf y}.\tag{L8-53}$$
$$\nabla\cdot\widetilde{\mathbf U}=0,\qquad \partial_t\widetilde n=-n_0\nabla\cdot\widetilde{\mathbf U}=0.\tag{L8-54}$$
<p>对非零频率波，密度扰动为零。磁力线横向弯曲，磁张力是回复力，好比拉紧琴弦的横振。\(\mathbf k\) 可以有非零垂直分量；“能量沿场传播”不等于“波矢只能沿场”。</p>
$$\omega=\pm V_Ak_\parallel,\qquad\mathbf v_g=\nabla_{\mathbf k}\omega=\pm V_A\mathbf b_0,\qquad\widetilde U_y=-\frac{\omega}{k_\parallel}\widetilde b_y.$$
<p><strong>退化方向：</strong>在 \(k_\perp=0\) 时，两种横向偏振简并，不能再仅指定 y 方向；在 \(k_\parallel=0\) 时剪切支为零频，以上含 \(1/k_\parallel\) 的表达不适用。</p>
{{FIG2}}
''')
sec('压缩 Alfvén 波：冷等离子体快磁声支','12',r'''
$$\omega^2=k^2V_A^2,\qquad\widetilde b_y=0,\quad k_\perp\widetilde b_x+k_\parallel\widetilde b_z=0.\tag{L8-55}$$
<p>磁扰动在 \(\mathbf k\) 与背景磁场组成的平面内；一般斜传播有 \(\widetilde b_z\ne0\)，磁场强度和密度一起变化。取运动偏振 \(\widetilde{\mathbf U}=\widetilde U_x\hat{\mathbf x}\)，由感应式和连续性式：</p>
$$\widetilde b_x=-\frac{k_\parallel}{\omega}\widetilde U_x,\qquad\widetilde b_z=\frac{k_\perp}{\omega}\widetilde U_x,\qquad\frac{\widetilde n}{n_0}=\frac{k_\perp\widetilde U_x}{\omega}=\widetilde b_z.$$
<p>在垂直传播时 \(\widetilde b_x=0\)，表现为纯磁压缩；在严格平行传播时 \(\widetilde b_z=\widetilde n=0\)，与剪切支简并，不再有压缩性。冷极限的群速度为 \(\mathbf v_g=\pm V_A\mathbf k/k\)。</p>
{{FIG3}}
<p><strong>学习补充：</strong>保留标量压强后，这一支推广为快磁声波，同时出现慢磁声波：\(\omega^2_{f,s}=\tfrac{k^2}{2}[V_A^2+c_s^2\pm\sqrt{(V_A^2+c_s^2)^2-4V_A^2c_s^2\cos^2\theta}]\)，\(c_s^2=\gamma P_0/\rho_{m0}\)。令 \(c_s\to0\)，快支回到 \(k^2V_A^2\)，慢支趋零；剪切支不变。此为补充，不是原讲义本节推导所保留的有限温度效应。</p>
''')
sec('自测：MHD 的模型、假设与欧姆定律','12–13',r'''
<details><summary>1. MHD 大致是什么理论？</summary><p>导电介质的低频长尺度单流体模型，用质量、动量、热力学闭合和感应方程描述流体与磁场耦合。</p></details>
<details><summary>2. 本讲基于哪些假设？</summary><p>非相对论、单价电子离子、\(\rho_i/L\sim\omega/\Omega_i\ll1\)、\(\beta\sim1\)、\(U\sim v_{Ti}\sim V_A\ll c\)，电子惯性小、准中性。标量压强/同温是额外闭合；低β波动另取冷极限。</p></details>
<details><summary>3. 广义欧姆定律是什么？</summary><p>式(20a)：流体系电场等于 Hall 项、电子压强项和电阻项之和；更一般情形还需电子惯性。</p></details>
<details><summary>4. 如何得到广义欧姆定律？</summary><p>从电子动量方程出发，忽略电子惯性，选取摩擦闭合，再用 \(\mathbf U_e\simeq\mathbf U-\mathbf j/(ne)\)。</p></details>
<details><summary>5. 理想欧姆定律是什么？</summary><p>\(\mathbf E+\mathbf U\times\mathbf B/c=0\)；并非实验室系电场为零。</p></details>
<details><summary>6. 什么是电阻 MHD？</summary><p>采用有限电导率的单流体 MHD，保留磁扩散与焦耳热，并说明所选热力学闭合。</p></details>
<details><summary>7. 什么是理想 MHD？</summary><p>电阻 MHD 的无限电导率极限；此处保留绝热标量压强闭合，磁通随光滑流动冻结。</p></details>
<details><summary>8. 什么是磁扩散率？</summary><p>\(\eta=c^2/(4\pi\sigma)=\nu_{ei}\delta_e^2\)，具有面积/时间量纲，勿与电阻率混淆。</p></details>
''')
sec('自测：完整方程组与两支波','12–13',r'''
<details><summary>9. 电阻 MHD 的完整方程有哪些？</summary><p>质量守恒、标量压强动量方程、含焦耳热的热力学方程、含磁扩散的感应方程、安培定律及磁场无散约束；需要电场时再加电阻欧姆定律。见式(45)。</p></details>
<details><summary>10. 理想 MHD 的完整方程有哪些？</summary><p>在式(45)中令 \(1/\sigma\to0\)，去掉热源和扩散，采用理想欧姆定律。不能只删除电阻热而保留有限电阻磁扩散，却称其为完整能量守恒的理想系统。</p></details>
<details><summary>11. 剪切 Alfvén 波的色散和基本物理是什么？</summary><p>\(\omega^2=k_\parallel^2V_A^2\)；非退化时扰动垂直于 \(\mathbf k\)-\(\mathbf B_0\) 平面、不压缩密度，以磁张力为回复力，群速度沿场。</p></details>
<details><summary>12. 压缩 Alfvén 波的色散和基本物理是什么？</summary><p>冷等离子体 \(\omega^2=k^2V_A^2\)；扰动在 \(\mathbf k\)-\(\mathbf B_0\) 平面，通常压缩磁场和密度，是冷极限的快磁声支。严格平行传播时不再压缩，并与剪切支简并。</p></details>
''')
sec('参考文献、原件与校注说明','13',r'''
<p>Alfvén, H. (1942). Existence of electromagnetic-hydrodynamic waves. <em>Nature</em> 150, 405. Freidberg, J. P. (2014). <em>Ideal MHD</em>. Cambridge University Press。</p>
<p>原 PDF 为用户上传的 2026-11-10 版 Lecture08。图1–3来自该原件，原字节及 SHA-256 一并内嵌。校注重点：原式(25)的 \(\epsilon\) 因子、(31)–(32)热流量纲、(29)应力记法、对称色散矩阵的约束零根，以及特殊传播方向的偏振退化。</p>
<p>本讲的“学习补充”是独立展开的教学说明；保留原作者对弱碰撞标量闭合与最小电阻模型的保留意见。疑似原式错误以明确校注呈现，原件可随时对照。</p>
''')
Path(__file__).with_name('lecture08-sections.json').write_text(json.dumps(S,ensure_ascii=False))
print(len(S))
