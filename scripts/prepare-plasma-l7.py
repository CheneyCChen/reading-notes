"""Convert the verified Lecture 7 translation to self-study sections.

Requires Pandoc. All original numbered equations and prose are retained. The
added learning notes and answers are explicitly distinguished from the source.
"""
from pathlib import Path
import re, json, subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reports/plasma-lectures/source'
tex = '\n'.join((SOURCE / f'lecture07-part{i}.tex').read_text() for i in (1, 2))
body_start = tex.index(r'\section{基本方程}')
quiz_start = tex.index(r'\section*{自测题}')
body = tex[body_start:quiz_start]

# Split only at paragraph/section boundaries, never inside an equation.
specs = [
    (r'\section{基本方程}', '碰撞矩：守恒方程改变了什么', '1'),
    (r'\section{粗略的有碰撞闭合：弱电离等离子体}', '弱电离 BGK：等温与忽略惯性是两层假设', '1–2'),
    (r'\subsection{密度方程}', '迁移率：反演摩擦与回旋矩阵', '2'),
    ('相应地，通量密度', '从粒子通量到电流：电导率与密度方程', '2–3'),
    (r'\subsection{扩散系数}', '随机游走：平行扩散、垂直扩散与适用尺度', '3–4'),
    (r'\subsection{双极扩散}', '双极扩散：由零电流消去自洽电场', '4'),
    (r'\subsubsection{磁化等离子体}', '磁化几何：局部零电流为什么过强', '5'),
    (r'\section{渐近有碰撞闭合}', '局域 Maxwell 分布与渐近闭合', '5'),
    (r'\subsection{以标量方程替代压强张量方程}', '压力取迹：温度、熵与黏性加热', '5–6'),
    (r'\subsection{Chapman--Enskog 展开}', 'Chapman–Enskog：转到随流速度坐标', '6–7'),
    ('现在只需对算符', '守恒零模：为何反演前要固定三个矩', '7'),
    (r'\subsection{一个简单例子}', '一阶驱动：密度梯度如何抵消', '8'),
    ('再假设 $\\widehat C=-\\nu$', 'BGK 一阶闭合：黏性应力与 Fourier 热流', '8'),
    (r'\sourcepage{7}{9}', 'Knudsen 数：输运展开真正的小参数', '9'),
    (r'\subsection{金标准：Braginskii 方程}', 'Braginskii 排序：强磁化、短自由程与高流速', '9–10'),
    ('因此可将其视为微扰。这给出以下电子方程：', '电子输运：平行、横向热流及摩擦', '10'),
    ('对于离子，有', '离子输运：热流、能量交换与各向异性黏性', '10–11'),
    ('这里的碰撞频率与前面得到的碰撞频率相同', '物理解读与边界：能量交换、焦耳热和边缘模型', '11'),
]
offsets = [body.index(marker) for marker, _, _ in specs]
assert offsets == sorted(offsets) and offsets[0] == 0

notes = [
 r'先固定量纲：$\boldsymbol R$ 是单位体积的力，$S$ 是单位体积、单位时间的随机动能源。由 $\int C\,\mathrm d\boldsymbol v=0$ 得到连续性不变；同种碰撞的总动量、总能量矩为零，不代表每个粒子的动量和能量都不改变。',
 r'本节的 $f_{s0}$ 以静止中性背景为中心；它不是与带电物种同流速的自碰撞 Maxwell 分布。先用足够长时间保证 $T_s\simeq T_n$，再用 $\omega/\nu_s\ll1$ 与 $U_s/(L\nu_s)\ll1$ 删除流体惯性，不能把强角散射直接等同于电子已热化。',
 r'取 $\boldsymbol B=B\boldsymbol e_z$，逐分量写出 $\nu U_x-\Omega U_y=F_x$、$\Omega U_x+\nu U_y=F_y$、$\nu U_z=F_z$。前两式行列式为 $\nu^2+\Omega^2$，所以平行迁移率与垂直迁移率不同。这里 $\Omega_s$ 和 $\mu_s$ 都带电荷符号。',
 r'先乘密度得到粒子通量，再乘 $q_s$ 得电流：$\boldsymbol j_s=q_s\boldsymbol\Gamma_s$。因此 $\boldsymbol\sigma_s=n_sq_s\boldsymbol\mu_s$，而 $\boldsymbol D_s=(T_s/q_s)\boldsymbol\mu_s$；这两式可同时检查电荷符号和量纲。Hall 部分是反对称的，所以 $\boldsymbol E\cdot\boldsymbol\sigma_H\boldsymbol E=0$，不会直接产生焦耳热。',
 r'精确的 BGK 系数是 $D_\parallel=v_T^2/\nu$、$D_\perp=v_T^2\nu/(\nu^2+\Omega^2)$。仅在 $\nu\ll|\Omega|$ 时才用 $D_\perp\simeq\rho^2\nu$。沿场增加碰撞缩短步长；在强磁化极限中，跨场增加碰撞增加换轨次数，所以二者对 $\nu$ 的依赖相反。离开该极限后，$D_\perp$ 在 $\nu=|\Omega|$ 附近达到最大值，再随碰撞率增加而下降。均匀磁场及常系数时，反对称输运部分的散度为零；非均匀情形不能直接把所有横向通量都删掉。',
 r'推导次序是：用准中性令 $n_e=Z_i n_i$，用零净电流令 $\Gamma_e=Z_i\Gamma_i$，再解出 $\boldsymbol E$ 并代回任一通量。准中性并不要求电场为零。对 $Z_i=1$、共同温度且 $|\mu_e|\gg\mu_i$，得到 $D_a\simeq2D_i$，不应误写成电子自由扩散率。',
 r'电荷连续性为 $\partial_t\rho_c+\nabla\cdot\boldsymbol j=0$。准稳态只要求电流无散度，不要求每一点的每个分量都为零；平行与垂直电流可以经端板或壁面闭合。若不说明边界条件，不能直接把未磁化的标量 $D_a$ 套到每个方向。',
 r'这一层不再把流速与温度代数消去，而保留 $n,\boldsymbol U,T$ 的演化。零阶 Maxwell 分布给各向同性压力 $P=nT$；一阶偏离给 $\boldsymbol\Pi$ 与 $\boldsymbol Q$。有碰撞不等于精确 Maxwell 分布，输运恰恰来自小但非零的偏离。',
 r'为免误用原稿系数，实际计算可采用以下经取迹重导的三维式：$\tfrac32 n\,\mathrm dT/\mathrm dt+nT\nabla\cdot\boldsymbol U=S-\nabla\cdot\boldsymbol Q-\boldsymbol\Pi:\nabla\boldsymbol U$。因此 $P\,\mathrm d[\tfrac32\ln(P/n^{5/3})]/\mathrm dt$ 等于同一个右端。这里保留原式和相邻校注，是为了便于核查，不是让两套系数同时进入模型。',
 r'链式法则中的时间导数在固定 $\boldsymbol v$ 下取，而 $g$ 的导数在固定 $\boldsymbol w$ 下取，这正是额外的 $-\partial_t\boldsymbol U\cdot\nabla_wg$ 的来源。用动量方程消去加速度后，电磁体力与随流加速度抵消，留下压力梯度及异种摩擦；磁回旋算符仍作用在非平衡部分上。',
 r'若不加零矩约束，可以把密度、流速或温度的小改变量任意从 $g_0$ 挪进 $\widetilde g$。三个约束固定了这种分解，并不额外要求真实密度、流速或温度为零。求逆只在与守恒模相容的子空间进行。',
 r'把式 (37) 代入后，$\boldsymbol w\cdot\nabla n/n$ 与压力梯度中的对应项抵消；温度项的 $-3/2$ 再减去压力梯度贡献的 $1$，成为 $-5/2$。余下温度梯度驱动关于 $\boldsymbol w$ 为奇函数，速度剪切驱动为偶函数，分别贡献热流与黏性应力。',
 r'积分可用 Maxwell 高斯矩核查：$\langle w_aw_b\rangle=v_T^2\delta_{ab}$，$\langle w_aw_bw_cw_d\rangle=v_T^4(\delta_{ab}\delta_{cd}+\delta_{ac}\delta_{bd}+\delta_{ad}\delta_{bc})$，且 $\langle w^6\rangle=105v_T^6$。由对称性，偶驱动不给热流，奇驱动不给应力。黏性系数 $\eta=P/\nu>0$，导热系数 $\kappa=5P/(2m\nu)>0$；动量方程中还要除以密度 $n$。',
 r'要区别两种时间排序：纯扩散演化速率 $\omega\sim\nu\mathrm{Kn}^2$，一般流体对流速率也可能是 $U/L\sim\nu\mathrm{Kn}$（当 $U\sim v_T$）。两者都要求 $\mathrm{Kn}\ll1$。电子碰撞更快但热速度也更大，在相近温度下这两个质量标度抵消，故平均自由程仍可同阶。',
 r'先检查 $\rho_i\ll\lambda_{ii}\ll L$：第一项保证碰撞前能回旋多次，第二项保证局域输运。再检查 $U_s\sim v_{Ti}$、$Z_i=1$ 和电子离子相对流的排序。这组数值系数不是可任意外推到所有电荷态、弱碰撞核心或强非局域分布的经验公式。',
 r'式 (51c) 包含沿温度梯度的导热及相对流驱动的热流，式 (51f) 同时包含电阻摩擦及热力。二者的 0.71 系数不能独立删取。涉及奇次电子回旋频率的横向项有原稿约定混用问题，必须连同下一节校注使用。',
 r'按结构辨认离子应力：平行黏性按 $P_i/\nu_{ii}$，回旋黏性按 $P_i/\Omega_i$，垂直黏性按 $P_i\nu_{ii}/\Omega_i^2$。回旋黏性是非耗散的有限回旋效应，不应把每个应力项都当成正的标量黏度。原式 (52e) 的离子垂直热流系数另有明确校注。',
 r'可用量纲与能量守恒交叉检查：写 $\boldsymbol Q=-\boldsymbol\kappa\cdot\nabla T$ 后，$\kappa/n$ 的量纲才是扩散率；三维温度演化的热扩散率还含 $2/3$。无温度梯度时，摩擦部分满足 $\boldsymbol R_{ei}\cdot(\boldsymbol U_i-\boldsymbol U_e)\ge0$。有热力时应把热流与摩擦联合分析，不能把每个交叉项单独要求为正。',
]
assert len(notes) == len(specs)

def split_align(match):
    value = match.group(1)
    depth = 0; last = 0; rows = []
    for token in re.finditer(r'\\begin\{[^}]+\}|\\end\{[^}]+\}|\\\\(?:\[[^\]]*\])?', value):
        if token.group().startswith(r'\begin'): depth += 1
        elif token.group().startswith(r'\end'): depth -= 1
        elif depth == 0:
            rows.append(value[last:token.start()]); last = token.end()
    rows.append(value[last:])
    result = []
    for row in rows:
        if not row.strip(): continue
        tag = ''.join(re.findall(r'\\(?:tag|label)\{[^}]+\}',row))
        row = re.sub(r'\\(?:tag|label)\{[^}]+\}','',row)
        result.append(r'\begin{equation}\begin{aligned}' + row + r'\end{aligned}' + tag + r'\end{equation}')
    return '\n'.join(result)

footnote_count = 0

def convert(value, prefix):
    global footnote_count
    value = re.sub(r'\\begin\{align\}([\s\S]*?)\\end\{align\}', split_align, value)
    value = re.sub(r'\\(?:chapter|section|subsection|subsubsection)\*?\{[^}]+\}', '', value)
    value = re.sub(r'\\sourcepage\{7\}\{\d+\}', '', value)
    value = re.sub(r'\\Needspace\{[^}]+\}', '', value)
    value = re.sub(r'\\addcontentsline\{[^}]+\}\{[^}]+\}\{[^}]+\}', '', value)
    value = value.replace(r'第~\ref{sec:L7:example}~节（原文第 3.4 节）', '“BGK 一阶闭合”一节（原文第 3.4 节）')
    result = subprocess.run(['pandoc','-f','latex','-t','html5','--mathjax','--id-prefix='+prefix],input=value,text=True,capture_output=True,check=True).stdout
    result = result.replace('id="footnotes"', 'id="'+prefix+'footnotes"')
    found = len(re.findall('class="footnote-ref"',result))
    if found:
        result = re.sub(r'<sup>(\d+)</sup>', lambda m: '<sup>'+str(footnote_count+int(m[1]))+'</sup>',result)
        result = result.replace('<ol>', '<ol start="'+str(footnote_count+1)+'">')
        footnote_count += found
    return result

sections = [{
    'title':'阅读路线：把碰撞率变成闭合的小参数', 'pages':'1–12',
    'html': convert(r'''本讲接续 Lecture 5 的碰撞算子与 Lecture 6 的矩方程。中心问题是：什么时候可以用局域的迁移率、黏度和导热率替代完整分布函数？

先读弱电离模型：从摩擦平衡反演流速，得到电导率、扩散和双极电场；再读完全电离模型：保留密度、流速和温度，通过 Chapman--Enskog 展开计算一阶应力与热流；最后检查 Braginskii 方程的排序及系数约定。

沿用高斯单位制与能量单位的温度，$v_{Ts}=\sqrt{T_s/m_s}$。原讲义的 $\Omega_s=q_sB/(m_sc)$ 有符号，回旋半径用于尺度估计时取 $\rho_s=v_{Ts}/|\Omega_s|$。本讲有 12 页原文、73 个编号公式标签、5 条脚注和 14 道原自测题，没有原始插图。原式、中文译文与译者校注完整保留；标为“学习补充”的段落和自测答案是自学辅助，不属于原作者正文。''','l7-roadmap-')
}]
for i, ((_,title,pages), start, note) in enumerate(zip(specs,offsets,notes)):
    raw = body[start: offsets[i+1] if i+1<len(offsets) else len(body)]
    html = convert(raw, f'l7-s{i+2}-')
    html += '<div class="learning-note"><h4>学习补充</h4>' + convert(note, f'l7-note{i+2}-') + '</div>'
    sections.append({'title':title,'pages':pages,'html':html})

quiz = tex[quiz_start:tex.index(r'\section*{参考文献}')]
questions = re.findall(r'\\item\s+([^\n]+)',quiz)
answers = [
 r'迁移率是电场到平均流速的线性响应：$\boldsymbol\mu_s=(q_s/m_s)\boldsymbol N_s^{-1}$。无磁场时为 $\mu_s=q_s/(m_s\nu_s)$；本讲电子迁移率为负。单位可由 $\boldsymbol U=\boldsymbol\mu\boldsymbol E$ 检查，且不要与磁矩混淆。',
 r'忽略惯性后解 $\boldsymbol N_s\boldsymbol U_s=q_s\boldsymbol E/m_s$，再乘 $n_sq_s$，得到 $\boldsymbol\sigma_s=n_sq_s^2\boldsymbol N_s^{-1}/m_s$。平行分量为 $n_sq_s^2/(m_s\nu_s)$，Pedersen 分量为 $n_sq_s^2\nu_s/[m_s(\nu_s^2+\Omega_s^2)]$，Hall 的 $yx$ 分量为 $-n_sq_s^2\Omega_s/[m_s(\nu_s^2+\Omega_s^2)]$。',
 r'Fick 通量是密度梯度驱动的粒子通量 $\boldsymbol\Gamma_{F,s}=-\boldsymbol D_s\nabla n_s$。它与电流不同，还要乘 $q_s$ 才成为该部分电流。张量反对称部分可以产生侧向通量，但不等同于沿梯度的耗散扩散。',
 r'先得 $\boldsymbol\Gamma_s=q_s^{-1}\boldsymbol\sigma_s\boldsymbol E-\boldsymbol D_s\nabla n_s$，代入 $\partial_tn_s+\nabla\cdot\boldsymbol\Gamma_s=0$，得到式 (11)。只有系数均匀且没有电场驱动时，才进一步简化成常系数扩散方程。',
 r'沿场步长为 $\lambda=v_T/\nu$，步频为 $\nu$，所以 $D_\parallel\sim\lambda^2\nu=v_T^2/\nu$。强磁化时跨场步长为 $\rho=v_T/|\Omega|$，故 $D_\perp\sim\rho^2\nu=v_T^2\nu/\Omega^2$。有限磁化的 BGK 结果是 $D_\perp=v_T^2\nu/(\nu^2+\Omega^2)$。',
 r'电子、离子扩散差异引起少量电荷分离，自洽电场随之建立；在未磁化、准中性、零总电流模型中，$\boldsymbol E_a=(D_i-D_e)\nabla\ln n/(\mu_i-\mu_e)$。它减慢快物种、加快慢物种，而不是把所有扩散停止。',
 r'双极扩散是电场耦合后电子与离子共同以一个密度扩散系数演化；一般电荷态满足 $\Gamma_e=Z_i\Gamma_i$。磁化有壁面回路时，整体电荷守恒不意味着每个方向分别具有相同的局部双极通量。',
 r'用 $n_e=Z_in_i$、$\Gamma_e=Z_i\Gamma_i$ 解出上题的电场，再代回离子通量：$\boldsymbol\Gamma_i=-D_a\nabla n_i$，$D_a=(\mu_iD_e-\mu_eD_i)/(\mu_i-\mu_e)$。共同温度且 $|\mu_e|\gg\mu_i$ 时，$D_a\simeq(Z_i+1)D_i$。',
 r'在相近温度、近似同阶且与速度无关的中性碰撞截面下，$\nu_s\propto v_{Ts}\propto m_s^{-1/2}$，所以 $|\mu_e|/\mu_i\sim Z_i^{-1}\sqrt{m_i/m_e}$；若截面不同，还要乘 $\sigma_{in}/\sigma_{en}$。对单电荷离子，常用估计是质量比平方根。',
 r'取 $g=g_0+\widetilde g$，$g_0$ 是由真实 $n,\boldsymbol U,T$ 定义的局域 Maxwell 分布。将小梯度驱动在零阶分布上求值，在线性碰撞加回旋算符下解出 $\widetilde g$；用零密度、零动量、零能量矩约束排除守恒零模，再计算应力、热流等矩。',
 r'$\mathrm{Kn}=\lambda_{\mathrm{mfp}}/L$ 比较微观平均自由程与宏观梯度尺度。$\mathrm{Kn}\ll1$ 是局域渐近输运的条件；它不等同于强磁化的 $\rho/L\ll1$，两者都需检查。',
 r'在完全电离、温度同阶且电荷态及库仑对数同阶时，$\nu_{ee}\sim\nu_{ei}\propto m_e^{-1/2}$、$\nu_{ii}\propto m_i^{-1/2}$，同时 $v_{Ts}\propto m_s^{-1/2}$，因此 $\lambda_{ee}\sim\lambda_{ei}\sim\lambda_{ii}$。原式 (45) 的热速度正指数是笔误。',
 r'适用于满足短平均自由程、强磁化、分布接近局域 Maxwell 状态及所用流速排序的完全电离等离子体。讲义列举较冷、较密的聚变边缘作为常见应用；不能仅凭位置就判断有效性，仍需逐项检查 Knudsen 数、磁化与梯度尺度。高温弱碰撞核心通常不满足这套局域闭合。',
 r'忽略热电交叉项的量级估计为 $Q_{s\parallel}\sim n_sv_{Ts}\lambda_s|\nabla_\parallel T_s|$，$Q_{s\perp}\sim n_s\rho_s^2\nu_s|\nabla_\perp T_s|$，横向非耗散热流 $Q_{s\times}\sim n_sv_{Ts}\rho_s|\nabla_\perp T_s|$。电子热流需联合考虑 e–e 与 e–i 碰撞，二者频率同阶，不能把它们当成两个独立热流简单相加；离子导热主要由 i–i 碰撞决定。相近温度与梯度下，电子沿场热流较强，离子经典跨场导热可较强；数值系数与符号见式 (51)、(52) 及校注。',
]
assert len(questions)==len(answers)==14
references = tex[tex.index(r'\section*{参考文献}'):]
data = {
    'title':'Lecture 7 · 有碰撞流体、输运与闭合',
    'summary':'从中性碰撞的摩擦平衡出发，推导迁移率、各向异性扩散与双极电场；再用 Chapman–Enskog 展开建立黏性和热传导，辨清 Braginskii 方程的排序、守恒与适用边界。',
    'objectives':['迁移率与电导率','双极扩散','Knudsen 数','Chapman–Enskog 展开','Braginskii 输运'],
    'sections':sections,
    'questions':[{'q':convert(q,f'l7-q{i+1}-'),'a':convert(a,f'l7-a{i+1}-')} for i,(q,a) in enumerate(zip(questions,answers))],
    'references':convert(references,'l7-ref-'),
    'cautions':convert(r'''本讲保留原稿公式，不将勘误无提示地改写进去。实际计算前，优先检查三组问题：碰撞力密度 $\boldsymbol R$ 到每粒子方程的 $1/n$；标量压力方程中的黏性系数、内能和熵符号；Braginskii 电子回旋频率的正负约定及离子垂直热流系数。其余 Hall 下标、抗磁流、扩散时间与热速度标度问题均在对应原式后列出。

对同一模型一致保留质量、动量与能量守恒，不要从不同排序中拼接单独的输运系数。弱电离密度模型、无磁场自碰撞 BGK 模型与 Braginskii 模型具有不同的背景、适用条件及保留项。''','l7-caution-'),
}
(SOURCE/'lecture07-content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sections':len(sections),'quiz':len(questions),'original_equation_tags':len(re.findall(r'\\tag\{',tex))},ensure_ascii=False))
