"""Preserve the reviewed source, add explicit inline TeX, and expand L7-A moments.

Only writes beneath this script's directory. Display math in the source is
byte-preserved; prose edits are limited to mathematical typesetting and the
explicit additions documented in README.md.
"""
from pathlib import Path
import re, json

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'derivation-supplements.original.md').read_text()
targets = {
    'L1-A': 'lecture1-s5', 'L2-A': 'lecture2-s11', 'L2-B': 'lecture2-s12',
    'L3-A': 'lecture3-s4', 'L3-B': 'lecture3-s7', 'L4-A': 'lecture4-s9',
    'L4-B': 'lecture4-s10', 'L5-A': 'lecture5-s9', 'L5-B': 'lecture5-s12',
    'L5-C': 'lecture5-s15', 'L5-D': 'lecture5-s16', 'L6-A': 'lecture6-s10',
    'L6-B': 'lecture6-s15', 'L7-A': 'lecture7-s14', 'L7-B': 'lecture7-s12',
    'L7-C': 'lecture7-s10', 'L7-D': 'lecture7-s19',
}

# Longest match wins. Only prose (never the supplied display equations) is
# processed. Each entry is a literal source spelling and its equivalent TeX.
pairs = [
    ('|q_s φ|/T_s≪1', r'|q_s\phi|/T_s\ll1'),
    ('r≪λ_D', r'r\ll\lambda_D'), ('r_nl', r'r_{\rm nl}'),
    ('λ_D⁻²=Σ_s 4πn_sq_s²/T_s', r'\lambda_D^{-2}=\sum_s4\pi n_sq_s^2/T_s'),
    ('λ_D', r'\lambda_D'),
    ('E_ω e⁻ⁱωt', r'\mathbf E_\omega e^{-i\omega t}'),
    ('|ω/Ω|≪1', r'|\omega/\Omega|\ll1'), ('|ω|=|Ω|', r'|\omega|=|\Omega|'),
    ('∂_t', r'\partial_t'), ('E×B', r'\mathbf E\times\mathbf B'),
    ('E_k eⁱᵏ·ˣ', r'\mathbf E_{\mathbf k}e^{i\mathbf k\cdot\mathbf x}'),
    ('k_⊥·ρ=k_⊥ρ_L cosθ', r'\mathbf k_\perp\cdot\boldsymbol\rho=k_\perp\rho_L\cos\theta'),
    ('⟨cos²θ⟩=1/2', r'\langle\cos^2\theta\rangle=1/2'),
    ('⟨cos⁴θ⟩=3/8', r'\langle\cos^4\theta\rangle=3/8'),
    ('cosθ', r'\cos\theta'), ('1−k_⊥²ρ_L²/4', r'1-k_\perp^2\rho_L^2/4'), ('J₀', r'J_0'),
    ('dH/dt=∂H/∂t=mωω̇x²', r'dH/dt=\partial H/\partial t=m\omega\dot\omega x^2'),
    ('x=√[2J/(mω)]sinθ', r'x=\sqrt{2J/(m\omega)}\sin\theta'), ('H=ωJ', r'H=\omega J'),
    ('ε=|ω̇|/ω²≪1', r'\epsilon=|\dot\omega|/\omega^2\ll1'), ('O(ε)', r'O(\epsilon)'),
    ('J_gyro=μmc/|q|', r'J_{\rm gyro}=\mu mc/|q|'),
    ('B(x)ẑ', r'B(x)\hat{\mathbf z}'), ('p_⊥(x)', r'p_\perp(x)'),
    ('n⟨μ⟩=p_⊥/B', r'n\langle\mu\rangle=p_\perp/B'),
    ('M=−(p_⊥/B)b', r'\mathbf M=-(p_\perp/B)\mathbf b'), ('∇B', r'\nabla B'),
    ('x−vt=常数', r'x-vt=\mathrm{const}'), ('v_T²', r'v_T^2'),
    ('Δv∼1/(|k|t)', r'\Delta v\sim1/(|k|t)'),
    ('(x,v)→(x−vt,v)', r'(x,v)\mapsto(x-vt,v)'), ('∫f ln f dx dv', r'\int f\ln f\,dx\,dv'),
    ('h(f)=f ln f', r'h(f)=f\ln f'), ('f̄', r'\bar f'),
    ('𝒱_f', r'\mathcal V_f'), ('V_x', r'V_x'), ('f_G(E_η)=η', r'f_G(E_\eta)=\eta'),
    ('f_G', r'f_G'), ('K_min', r'K_{\min}'),
    ('F(v−U)', r'F(\mathbf v-\mathbf U)'), ('F(v)', r'F(\mathbf v)'),
    ('K_G=NmU²/2', r'K_G=NmU^2/2'),
    ('χ∼|b₀|/b', r'\chi\sim|b_0|/b'), ('|Δv|∼uχ', r'|\Delta\mathbf v|\sim u\chi'),
    ('nu·2πb db', r'nu\,2\pi b\,db'), ('b_min∼|b₀|', r'b_{\min}\sim|b_0|'),
    ('r=2', r'r=2'), ('r>2', r'r>2'), ('u⁻ʳ', r'u^{-r}'),
    ('1/lnΛ', r'1/\ln\Lambda'), ('lnΛ', r'\ln\Lambda'), ('χ²', r'\chi^2'),
    ('Δ_ΩY_ℓm=−ℓ(ℓ+1)Y_ℓm', r'\Delta_\Omega Y_{\ell m}=-\ell(\ell+1)Y_{\ell m}'),
    ('C=(ν(v)/2)Δ_Ωf', r'C=(\nu(v)/2)\Delta_\Omega f'),
    ('ℓ=0', r'\ell=0'), ('ℓ=1', r'\ell=1'), ('ℓ=2', r'\ell=2'),
    ('3ν', r'3\nu'), ('ν(v)', r'\nu(v)'),
    ('4π∫₀ᵛs²f_b(s)ds=n_bF(x)', r'4\pi\int_0^v s^2f_b(s)\,ds=n_bF(x)'),
    ('v²φ_b′=−n_bF(x)', r'v^2\phi_b\prime=-n_bF(x)'),
    ('v=0', r'v=0'), ('φ_b∼n_b/v', r'\phi_b\sim n_b/v'),
    ('(v²ψ_b′)′=2v²φ_b', r'(v^2\psi_b\prime)\prime=2v^2\phi_b'),
    ('G(x)=F(x)/(2x²)', r'G(x)=F(x)/(2x^2)'),
    ('Γ_sb=4πq_s²q_b²lnΛ_sb/m_s²', r'\Gamma_{sb}=4\pi q_s^2q_b^2\ln\Lambda_{sb}/m_s^2'),
    ('C=−∂_i(A_if)+∂_i∂_j(B_ijf)', r'C=-\partial_i(A_if)+\partial_i\partial_j(B_{ij}f)'),
    ('B_⊥', r'B_\perp'), ('v≫σ', r'v\gg\sigma'),
    ('F→1', r'F\to1'), ('G∼σ²/v²', r'G\sim\sigma^2/v^2'),
    ('B_∥∼Γn_bσ²/v³', r'B_\parallel\sim\Gamma n_b\sigma^2/v^3'),
    ('B_⊥∼Γn_b/(2v)', r'B_\perp\sim\Gamma n_b/(2v)'),
    ('v→0', r'v\to0'), ('F∼4x³/(3√π)', r'F\sim4x^3/(3\sqrt\pi)'),
    ('G∼2x/(3√π)', r'G\sim2x/(3\sqrt\pi)'),
    ('v⁻¹', r'v^{-1}'), ('v⁻³', r'v^{-3}'),
    ('∇_v·B=Γ_sb∇_vφ_b', r'\nabla_v\cdot\mathsf B=\Gamma_{sb}\nabla_v\phi_b'),
    ('m_s/m_b', r'm_s/m_b'), ('1+m_s/m_b', r'1+m_s/m_b'),
    ('F=2x²G=v²G/σ²', r'F=2x^2G=v^2G/\sigma^2'), ('T_b', r'T_b'),
    ('V f+B·∇_vf=0', r'\mathbf V f+\mathsf B\cdot\nabla_vf=0'),
    ('v′=v+δv', r'\mathbf v\prime=\mathbf v+\delta\mathbf v'),
    ('δv', r'\delta\mathbf v'), ('∇a_s=λ_s(v)I', r'\nabla\mathbf a_s=\lambda_s(\mathbf v)\mathsf I'),
    ('∇a_s', r'\nabla\mathbf a_s'), ('∇λ_s=0', r'\nabla\lambda_s=0'),
    ('λ_s<0', r'\lambda_s<0'), ('T_s=−1/λ_s', r'T_s=-1/\lambda_s'),
    ('U_s=−c_s/λ_s', r'\mathbf U_s=-\mathbf c_s/\lambda_s'),
    ('λ_s=λ_s′', r'\lambda_s=\lambda_{s\prime}'), ('c_s=c_s′', r'\mathbf c_s=\mathbf c_{s\prime}'),
    ('f₁,φ₁∝eⁱᵏˣ⁻ⁱωᵗ', r'f_1,\phi_1\propto e^{ikx-i\omega t}'), ('Imω>0', r'\operatorname{Im}\omega>0'),
    ('k>0', r'k>0'), ('f₀′=−vf₀/v_T²', r'f_0\prime=-vf_0/v_T^2'),
    ('v/(v−ω/k)=1+(ω/k)/(v−ω/k)', r'v/(v-\omega/k)=1+(\omega/k)/(v-\omega/k)'),
    ('|ζ|≫1', r'|\zeta|\gg1'), ('1/(u−ζ)', r'1/(u-\zeta)'),
    ('⟨u²⟩=1/2', r'\langle u^2\rangle=1/2'), ('⟨u⁴⟩=3/4', r'\langle u^4\rangle=3/4'),
    ('ω²=ω_p²+3k²v_T²+…', r'\omega^2=\omega_p^2+3k^2v_T^2+\cdots'),
    ('|ζ|≪1', r'|\zeta|\ll1'), ('Z(ζ)=i√π−2ζ+…', r'Z(\zeta)=i\sqrt\pi-2\zeta+\cdots'),
    ('v_Ti≪|ω/k|≪v_Te', r'v_{Ti}\ll|\omega/k|\ll v_{Te}'), ('Te≫Ti', r'T_e\gg T_i'),
    ('Δp=p_∥−p_⊥', r'\Delta p=p_\parallel-p_\perp'),
    ('P=p_⊥I+Δp bb', r'\mathsf P=p_\perp\mathsf I+\Delta p\,\mathbf b\mathbf b'),
    ('∇·b=−∂_∥lnB', r'\nabla\cdot\mathbf b=-\partial_\parallel\ln B'),
    ('−∇·P', r'-\nabla\cdot\mathsf P'), ('∇p', r'\nabla p'), ('p_∥', r'p_\parallel'),
    ('a=v_T²=T/m', r'a=v_T^2=T/m'), ('⟨h⟩=n⁻¹∫h g₀d³w', r'\langle h\rangle=n^{-1}\int hg_0\,d^3w'),
    ('A_ij=w_iw_j−δ_ijw²/3', r'A_{ij}=w_iw_j-\delta_{ij}w^2/3'), ('Π_ij', r'\Pi_{ij}'),
    ('Q_i', r'Q_i'), ('⟨w_iw_jF(w²)⟩=δ_ij⟨w²F(w²)⟩/3', r'\langle w_iw_jF(w^2)\rangle=\delta_{ij}\langle w^2F(w^2)\rangle/3'),
    ('⟨w⁴⟩=15a²', r'\langle w^4\rangle=15a^2'), ('⟨w⁶⟩=105a³', r'\langle w^6\rangle=105a^3'),
    ('15a²', r'15a^2'), ('η=P/ν', r'\eta=P/\nu'), ('κ=5P/(2mν)', r'\kappa=5P/(2m\nu)'),
    ('Ĉg̃=源项', r'\widehat C\widetilde g=\text{源项}'),
    ('∫g̃{1,w,w²}=0', r'\int\widetilde g\{1,\mathbf w,w^2\}\,d^3w=0'),
    ('⟨A_ij⟩=0', r'\langle A_{ij}\rangle=0'), ('5/2', r'5/2'),
    ('s=(3/2)lnT−lnn+常数', r's=(3/2)\ln T-\ln n+\mathrm{const}'),
    ('D_tn', r'D_tn'), ('nT D_ts=−∇·Q−Π:∇U', r'nT D_ts=-\nabla\cdot\mathbf Q-\boldsymbol\Pi:\nabla\mathbf U'),
    ('Q=−κ∇T', r'\mathbf Q=-\kappa\nabla T'), ('Π=−ηW', r'\boldsymbol\Pi=-\eta\mathsf W'),
    ('W=∇U+(∇U)ᵀ−(2/3)I∇·U', r'\mathsf W=\nabla\mathbf U+(\nabla\mathbf U)^{\mathsf T}-(2/3)\mathsf I\nabla\cdot\mathbf U'),
    ('W:∇U=W:W/2', r'\mathsf W:\nabla\mathbf U=\mathsf W:\mathsf W/2'),
    ('Q_×∝b×∇T', r'\mathbf Q_\times\propto\mathbf b\times\nabla T'), ('∇T', r'\nabla T'),
    ('E·j_H=0', r'\mathbf E\cdot\mathbf j_H=0'),
    ('v=U_s+w', r'\mathbf v=\mathbf U_s+\mathbf w'), ('U_s·R_s', r'\mathbf U_s\cdot\mathbf R_s'),
    ('a=e', r'a=e'), ('b=i', r'b=i'), ('a,b', r'a,b'),
    ('R_e=α(U_i−U_e)', r'\mathbf R_e=\alpha(\mathbf U_i-\mathbf U_e)'), ('α>0', r'\alpha>0'),
    ('α|U_i−U_e|²', r'\alpha|\mathbf U_i-\mathbf U_e|^2'),
    ('R_e∝−∇T_e', r'\mathbf R_e\propto-\nabla T_e'),
    ('R_e·(U_i−U_e)', r'\mathbf R_e\cdot(\mathbf U_i-\mathbf U_e)'),
    ('n_e=n_i=n', r'n_e=n_i=n'), ('m_i/m_e', r'm_i/m_e'), ('Te=Ti', r'T_e=T_i'), ('ν_ei', r'\nu_{ei}'),
]

# Standalone mathematical variables, not parts of named methods or prose words.
symbols = {'Q': 'Q', 'T': 'T', 'v': 'v', 'r': 'r', 'a': 'a', 'b': 'b',
           'J': 'J', 'H': 'H', 'B': 'B', 'F': 'F', 'G': 'G', 'f': 'f', 'E': 'E',
           'u': 'u', 'x': 'x', 'n': 'n', 'U': r'\mathbf U',
           'A': r'\mathbf A', 'W': r'\mathsf W',
           'θ': r'\theta', 'μ': r'\mu', 'η': r'\eta', 'ν': r'\nu'}

def inline_math(text):
    tokens = []
    def hold(latex):
        latex = latex.replace(r'\prime', r'^\prime')
        tokens.append(r'\(' + latex + r'\)')
        return '\u0000' + str(len(tokens)-1) + '\u0000'
    # Protect any already explicit math introduced by the additions below.
    text = re.sub(r'\\\((.*?)\\\)', lambda m: hold(m[1]), text, flags=re.S)
    for plain, latex in sorted(pairs, key=lambda p: len(p[0]), reverse=True):
        text = text.replace(plain, hold(latex)) if plain in text else text
    for plain, latex in symbols.items():
        pattern = r'(?<![A-Za-z_0-9])' + re.escape(plain) + r'(?![A-Za-z_0-9])'
        text = re.sub(pattern, lambda m: hold(latex), text)
    return re.sub('\u0000(\\d+)\u0000', lambda m: tokens[int(m[1])], text)

def normalize_math(text):
    segments = re.split(r'(\\\[.*?\\\])', text, flags=re.S)
    return ''.join(s if s.startswith(r'\[') else inline_math(s) for s in segments)

moment_addition = r'''
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

'''

modules = []
for match in re.finditer(r'^## (L\d-[A-Z])｜(.+?)\n(.*?)(?=^## |\Z)', source, flags=re.M|re.S):
    ident, title, body = match.groups()
    location, body = body.strip().split('\n\n', 1)
    body = body.replace('由于 U 只消去', r'由于 \(\mathsf U\) 只消去')
    body = body.replace('忽略 b 的空间变化', r'忽略 \(\mathbf b\) 的空间变化')
    body = body.replace('扩散的 1/2 约定', r'扩散的 \(1/2\) 约定')
    if ident == 'L7-A':
        body = body.replace('**先求应力。**', moment_addition + '**先求应力。**')
    modules.append({
        'id': 'supplement-' + ident.lower(), 'source_id': ident,
        'lecture': int(ident[1]), 'target_section': targets[ident],
        'title': normalize_math(title), 'title_plain': title, 'body': normalize_math(body),
        'source_insertion_note': location,
        'collapsed': ident in ['L4-B','L5-C','L6-A'],
        'insertion': 'append_to_existing_prose',
    })
assert len(modules) == 17
original_math = re.findall(r'\\\[(.*?)\\\]', source, flags=re.S)
normalized_math = [m for obj in modules for m in re.findall(r'\\\[(.*?)\\\]', obj['body'], flags=re.S)]
cursor = iter(normalized_math)
for formula in original_math:
    assert any(formula == candidate for candidate in cursor), 'Source display formula lost/reordered'
(ROOT/'modules.json').write_text(json.dumps(modules,ensure_ascii=False,indent=2)+'\n')
render_source = '# 排版与计算展开版（17 个补充模块）\n\n'
render_source += '原始稿原样保存为 derivation-supplements.original.md；数学转写与显式新增说明见 README.md。\n\n'
render_source += '\n\n'.join('## '+m['source_id']+'｜'+m['title']+'\n\n'+m['body'] for m in modules)
(ROOT/'derivation-supplements.render.md').write_text(render_source+'\n')
print(json.dumps({'modules':len(modules),'original_display_equations':len(original_math),
                  'rendered_display_equations':len(normalized_math)},ensure_ascii=False))
