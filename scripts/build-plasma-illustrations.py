"""Generate additive static SVG teaching diagrams, no JavaScript or dependencies.
Run from any directory. Illustration blocks reverse byte-for-byte to c8a831f.
"""
from pathlib import Path
import math,re,json
from html import escape
R=Path(__file__).resolve().parents[1]; D=R/'reports/plasma-lectures/illustrations';D.mkdir(exist_ok=True)
def txt(x,y,s,size=19,anchor='middle'):
 return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{escape(s)}</text>'
def line(x,y,X,Y,arrow=False,dash=False):
 return f'<path d="M{x},{y} L{X},{Y}" fill="none" stroke="currentColor" stroke-width="2"'+(' marker-end="url(#ARROW)"' if arrow else '')+(' stroke-dasharray="6 5"' if dash else '')+'/>'
def path(d,arrow=False):return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2.5"'+(' marker-end="url(#ARROW)"' if arrow else '')+'/>'
def poly(points,fill='none'):
 return '<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+'" fill="'+fill+'" stroke="currentColor" stroke-width="2"/>'
def curve(points):return path('M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in points))
def circle(x,y,r,fill='none'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="2"/>'
figs=[]
def add(key,section,title,desc,body,caption):
 ident='pi-'+key
 body=body.replace('ARROW',ident+'-arrow')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 330" role="img" aria-labelledby="{ident}-title {ident}-desc" class="plasma-figure-svg"><title id="{ident}-title">{title}</title><desc id="{ident}-desc">{desc}</desc><defs><marker id="{ident}-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="currentColor"/></marker></defs><g font-family="Georgia, Songti SC, serif" fill="currentColor">{body}</g></svg>'
 (D/f'{key}.svg').write_text(svg)
 figs.append(dict(key=key,section=section,title=title,description=desc,caption=caption,svg=svg))
# 1. Screened/unshielded point source normalized at each radius.
b=line(80,250,550,250,True)+line(80,250,80,45,True)+txt(550,280,'r / λD')+txt(82,30,'r φ / Q')
b+=line(80,65,530,65,False,True)+txt(380,53,'无屏蔽：1')
b+=curve([(80+100*x,250-185*math.exp(-x)) for x in [i/30 for i in range(136)]])+txt(300,173,'屏蔽：exp(−r / λD)')
b+=line(180,250,180,182,False,True)+txt(180,280,'1')+txt(50,72,'1')+txt(50,255,'0')+txt(300,314,'三维点源 · 线性响应区；不描述源附近非线性核心',17)
add('debye-screening','lecture1-s5','德拜屏蔽：比较剥去 1/r 因子后的电势','横轴为距点源距离除以德拜长度，纵轴为 rφ/Q，采用讲义高斯单位。无屏蔽值为1，线性屏蔽结果按指数下降。',b,'图 1 · 采用讲义的高斯单位，三维 Yukawa 势为 φ = Q exp(−r/λD)/r。画 rφ/Q 是为了单独显示屏蔽因子；原点仅表示线性解的形式极限，不能据此把线性化外推到强扰动核心。')
# 2 gyration cross section sign explicit positive q B out.
b=circle(300,155,92)+circle(300,155,4,'currentColor')+txt(300,172,'导心',17)+circle(392,155,7,'currentColor')+line(392,155,392,225,True)+txt(436,211,'v⊥')+line(392,155,326,155,True)+txt(354,135,'洛伦兹力',17)+line(300,155,300,63,False,True)+txt(276,105,'ρ')
b+=circle(90,80,17)+circle(90,80,3,'currentColor')+txt(90,118,'B 出纸面',17)+txt(300,30,'垂直磁场平面：q > 0，顺时针回旋')+txt(300,282,'沿 B 的 v∥ 与回旋叠加，形成螺旋轨道')+txt(300,312,'q < 0 时回旋方向反转；ρ = v⊥ / |Ω|',17)
add('gyromotion','lecture2-s3','回旋运动中的速度与洛伦兹力','正电荷在出纸面均匀磁场中顺时针回旋。轨道右端速度向下，洛伦兹力指向圆心。',b,'图 2 · 圆周图是垂直于 B 的截面，不是完整三维轨道。无电场、均匀静磁场下，洛伦兹力不做功；横向导心固定，完整导心沿 B 以不变的平行速度移动。')
# 3 loss cone in meridional velocity plane
b=poly([(300,165),(525,60),(525,270)],'var(--soft, #e8e4d9)')+poly([(300,165),(75,60),(75,270)],'var(--soft, #e8e4d9)')
b+=line(45,165,560,165,True)+line(300,290,300,40,True)+txt(562,193,'v∥')+txt(300,24,'v⊥（有符号截面）',17)+txt(455,153,'逃逸')+txt(140,153,'逃逸')+txt(300,75,'俘获')+txt(300,260,'俘获')
b+=path('M354,165 A54,54 0 0 0 349,142')+txt(388,157,'αLC',17)+txt(300,315,'sin² αLC = Bmin / Bmax',21)
add('loss-cone','lecture3-s8','磁镜中面速度空间中的双向损失锥','在磁场最弱处画速度空间截面。靠近平行轴的双锥为可逃逸区域，锥外为反射俘获区域；没有电势或碰撞。',b,'图 3 · 在 Bmin 处定义俯仰角 α。无电势、无碰撞且磁矩近似守恒时，sin²α < Bmin/Bmax 的粒子可越过镜喉；等号为临界轨道。阴影是三维双锥的一个二维截面，纵轴有正负号仅用于显示该截面。')
# 4 free particle canonical shear exact determinant1
b=line(40,240,260,240,True)+line(55,255,55,50,True)+txt(260,267,'q')+txt(35,48,'p')+poly([(90,190),(170,190),(170,100),(90,100)],'var(--soft, #e8e4d9)')+txt(132,153,'S')
b+=line(330,240,575,240,True)+line(345,255,345,50,True)+txt(575,267,'q')+txt(325,48,'p')+poly([(400,190),(480,190),(516,100),(436,100)],'var(--soft, #e8e4d9)')+txt(460,153,'S')+line(245,140,320,140,True)+txt(283,113,'时间 t',16)
b+=txt(300,30,'自由粒子 Hamilton 流：平移 + 剪切')+txt(300,296,'q(t) = q(0) + p(0)t/m，p(t) = p(0)',19)+txt(300,321,'相空间面积守恒；形状不必保持',17)
add('liouville-shear','lecture4-s2','Liouville 定理：相空间剪切保持面积','自由粒子的正则相空间小矩形随时间剪切成平行四边形。两形状底边和高度相同，因此面积相等。',b,'图 4 · 对 H = p²/(2m)，相空间映射的 Jacobian 行列式等于 1。这里两块阴影面积相等而形状不同，说明 Liouville 不可压缩性指相空间体积，并不要求真实空间密度不变。')
# 5 small-angle scattering speed sphere
O=(100,240);u=300;theta=.42;x=O[0]+u*math.cos(theta);y=O[1]-u*math.sin(theta)
b=line(75,240,490,240,True)+txt(510,220,'平行方向',17)+line(100,265,100,45,True)+txt(100,30,'横向')+line(100,240,400,240,True)+line(100,240,round(x,2),round(y,2),True)+txt(290,218,'u')+txt(260,150,'u′')+line(400,240,x,y,True)+txt(432,170,'Δu')+line(x,240,x,y,False,True)+path('M160,240 A60,60 0 0 0 155,216')+txt(183,221,'θ')+txt(300,290,'|u′| = |u|：仅相对速度方向改变',19)+txt(300,319,'Δu⊥ ~ uθ；Δu∥ ~ −uθ²/2',19)
add('small-angle-collision','lecture5-s11','小角散射的横向与纵向速度增量','两体弹性碰撞的相对速度在碰撞前后模长不变。横向增量为一阶角度，纵向增量为负的二阶角度。',b,'图 5 · u 是两粒子的相对速度，不是一般实验室系中某一物种的速度。小角极限下，横向扩散与二阶纵向漂移必须配合；沿初速度方向的平均分量减小，不等于相对动能损失。')
# 6 CGL two separate compressions rectangular flux tubes
b=txt(150,30,'横向压缩')+txt(450,30,'平行压缩')
for x,y,w,h in [(45,65,210,70),(45,200,210,35),(345,65,210,70),(390,200,120,70)]:
 b+=poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)])
 for yy in [y+h*.3,y+h*.7]: b+=line(x+8,yy,x+w-8,yy,True)
b+=txt(150,54,'B →（沿管轴）',16)+txt(450,54,'B →（沿管轴）',16)+line(150,145,150,187,True)+line(450,145,450,187,True)+txt(150,262,'长度固定：n ∝ B',17)+txt(150,292,'T⊥ ∝ B；T∥ 不变',18)+txt(450,292,'T∥ ∝ n²；T⊥ 不变',18)+txt(450,320,'截面积固定：B 不变',17)
add('cgl-compression','lecture6-s18','CGL 双绝热的两种压缩检验','磁场沿磁通管长轴。横向压缩固定长度，使密度与磁场同增、垂直温度升高；平行压缩固定截面，使平行温度随密度平方增长。',b,'图 6 · 两个独立思想实验，均假设强磁化、缓慢演化、磁通冻结、粒子数守恒、无碰撞且热流可忽略。p⊥/(nB) 与 p∥B²/n³ 守恒给出图中温度标度；这些是流体元演化，不是任意等离子体都适用的闭合。')
#7 diffusion displacement scale emphasize schematic not seeded random implied sample
b=txt(150,32,'沿场随机游走')+txt(450,32,'强磁化横向导心游走')
b+=line(45,110,260,110,True)+txt(150,85,'B',18)+line(60,135,210,135,True)+line(210,170,110,170,True)+line(110,205,250,205,True)+txt(35,141,'①',16)+txt(35,176,'②',16)+txt(35,211,'③',16)+txt(150,250,'步长 ~ vT / ν',20)
b+=circle(450,155,64)+circle(482,173,64)+circle(450,155,3,'currentColor')+circle(482,173,3,'currentColor')+line(450,155,482,173,True)+txt(450,250,'导心步长 ~ ρ = vT / |Ω|',17)+txt(450,75,'B 垂直此平面',17)
b+=txt(150,294,'D∥ ~ vT² / ν',20)+txt(450,294,'D⊥ ~ νρ²',20)+txt(300,323,'适用：ν ≪ |Ω|，且观察时间远大于碰撞时间',17)
add('magnetized-diffusion','lecture7-s6','碰撞与强磁场如何改变扩散步长','沿磁场方向每次碰撞之间移动约一个自由程。垂直方向碰撞改变回旋导心约一个回旋半径。两方向扩散系数对碰撞频率依赖相反。',b,'图 7 · 左侧三行依次表示三个时间段的沿场位移，错层仅为看清返回步，不是横向运动。图示用于量级估计，不代表一次特定粒子轨迹。沿场步长约为自由程，横场导心跳跃约为回旋半径，步时均约为 1/ν。这里 ν 是有效偏转／去相关频率，不是单次微小库仑散射的发生频率。数值系数依赖碰撞模型；弱磁化时不能继续使用 D⊥ ~ νρ²。')
#8 shear wave k along B simplest shear bent field displacement
b=txt(300,30,'沿场传播的剪切 Alfvén 波（k ∥ B₀）')+line(65,170,550,170,True,True)+txt(550,203,'z')+txt(493,154,'B₀，k',18)
b+=curve([(65+i*1.2,170-42*math.sin(2*math.pi*i/240)) for i in range(361)])+line(137,170,137,128,True)+txt(110,110,'ξ⊥',19)+line(180,134,180,163,True)+txt(208,146,'F张力',17)+txt(220,77,'磁张力提供恢复力',19)+txt(300,268,'扰动横向，沿 B₀ 传播；一阶无密度压缩',19)+txt(300,302,'ω² = k∥² vA²',23)
add('shear-alfven','lecture8-s24','剪切 Alfvén 波：横向位移与磁张力','虚线为均匀背景磁场方向，实线为某一时刻弯曲的磁力线。位移垂直背景磁场，磁张力指向平衡位置。此图取波矢平行背景磁场。',b,'图 8 · 实线是某一时刻的磁力线形状，不是粒子沿正弦曲线前进的轨迹。理想、均匀背景下，剪切 Alfvén 波满足 ω² = k∥²vA²；图取 k ∥ B₀，避免把一般斜传播的三维偏振混成二维压缩波。')
style='''<style id="plasma-illustration-style">.plasma-illustration{margin:30px 0;padding:20px 0;border-block:1px solid var(--line);break-inside:avoid}.plasma-illustration .diagram-scroll{overflow-x:auto;overscroll-behavior-x:contain}.plasma-figure-svg{display:block;width:100%;min-width:480px;height:auto;max-height:none;color:var(--ink)}.plasma-illustration figcaption{margin-top:14px;font-size:.9em;line-height:1.8;color:var(--muted)}.plasma-illustration figcaption strong{color:var(--ink)}.plasma-illustration .diagram-hint{font-size:.8em;color:var(--muted);margin:8px 0 0}.diagram-scroll:focus-visible{outline:2px solid var(--ink);outline-offset:3px}@media(min-width:650px){.plasma-illustration .diagram-hint{display:none}}@media print{.plasma-figure-svg{min-width:0}.plasma-illustration .diagram-hint{display:none}}</style>'''
p=R/'reports/plasma-lectures/index.html';s=p.read_text();s=re.sub(r'<!-- PLASMA-ILLUSTRATION:[^>]*:start -->[\s\S]*?<!-- PLASMA-ILLUSTRATION:[^>]*:end -->','',s)
s=s.replace('</head>','<!-- PLASMA-ILLUSTRATION:style:start -->'+style+'<!-- PLASMA-ILLUSTRATION:style:end --></head>')
for f in figs:
 pattern=r'(<section\b[^>]*id="'+f['section']+r'"[^>]*>[\s\S]*?<div class="prose">)'
 fig=f'<!-- PLASMA-ILLUSTRATION:{f["key"]}:start --><figure class="plasma-illustration" id="fig-{f["key"]}"><div class="diagram-scroll" tabindex="0" role="region" aria-label="{f["title"]}；窄屏可横向滚动">{f["svg"]}</div><p class="diagram-hint">窄屏可横向滑动查看完整标注。</p><figcaption>{f["caption"]}</figcaption></figure><!-- PLASMA-ILLUSTRATION:{f["key"]}:end -->'
 s,n=re.subn(pattern,lambda m:m[1]+fig,s,count=1);assert n==1,f['section']
p.write_text(s)
(D/'manifest.json').write_text(json.dumps([{k:v for k,v in f.items() if k!='svg'} for f in figs],ensure_ascii=False,indent=2)+'\n')
print('Generated',len(figs),'static, accessible diagrams')
