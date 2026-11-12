# Reading Club

个人论文阅读网站。保留 HTML 精读报告中的公式、原文插图、来源和章节链接，提供标题／作者／关键词搜索、主题筛选、收藏和阅读状态。

## 本地使用

直接打开 `index.html` 即可使用，无需安装依赖。收藏和阅读状态保存在当前浏览器的 localStorage，不上传到 GitHub，不跨设备同步。清理浏览器数据会清除标记。

## 内容

### 2026-11-12 新增七篇精读

- [几何代理的实验检验：负三角形与拉长比](reports/geometric-proxies-2026-reading/report.html)：TCV、跨装置回旋动理学与几何代理：区分相关指标、真实输运和可迁移性的证据。
- [CGYRO 动态优化：在非光滑谱上寻找低输运塑形](reports/dynamic-gyrokinetic-optimization-reading/report.html)：解析 libEnsemble 与流形采样如何处理增长率谱的分支切换，以及线性优化与非线性验证的差距。
- [可微反应堆设计：用计算图拆解 PROCESS](reports/differentiable-reactor-mdao-reading/report.html)：拆解 cottax 的依赖图、耦合环和自动微分，区分模型执行提速与完整设计优化收益。
- [yancc：GPU 上的可微新经典输运](reports/yancc-neoclassical-reading/report.html)：解析漂移动理学离散、求解器和导数，以及 tokamak/stellarator 基准与性能边界。
- [不完美模型如何构成聚变数字孪生](reports/fusion-digital-twins-reading/report.html)：Nature Physics 评论精读：模型与实验的双向更新、多保真和不确定性；区分愿景与已经验证的结果。
- [轴对称偶极线圈阵列：混合托卡马克–仿星器可行性](reports/hybrid-dipole-coil-array-reading/report.html)：逐步解释混合实验的线圈布局、三维场自由度、平衡与工程约束，辨认可行性证据与未验证之处。
- [反向环向场线圈：解耦模块线圈电流与净环向场](reports/reversed-toroidal-field-coils-reading/report.html)：解析 RTF 补偿电流的新自由度、线圈–等离子体间距收益与案例依赖，连接仿星器线圈优化研究。

新增条目沿用原有主题、导航和离线公式；关键原图精选及页码见各报告。输入版本 SHA256 见 `reports/november-2026-sources.json`。不重新发布带个人下载信息的出版商封面。


- [等离子体物理 Lectures 1–7 自学手册](reports/plasma-lectures/index.html)：81 页原讲义、108 个学习单元、63 道带答案自测；新增第七讲迁移率、双极扩散、Chapman–Enskog 展开和 Braginskii 输运，保留 73 个编号公式标签、5 条脚注及原稿校注；七份原 PDF 与离线公式完整内嵌（2026-11-09）。

- cuGMEC / CUDA 回旋动理学–MHD：Liu–Jiang–Fu 2026 CPC 正式版，全部 16 页、16 幅原图、3 张原表；解析压力耦合、δf PIC、电子闭合与 GPU 加速，固定源码版本核查顺序耦合，评估模型局限和可验证研究路线；离线公式与资源静态检查通过，浏览器渲染检查未完成（2026-10-19）。

- 仿星器边界表示 / 极向角规范：Henneberg–Helander–Drevlak 2021 JPP 正式版，全部 16 页、15 幅原图；解析旋转截面投影、显式 Fourier 转换与优化冗余，核查浅局部极小、W7-X 重建、三维目标收益及中间公式疑点；公式离线预渲染，按要求未使用浏览器检验（2026-10-13）。
- 扩展 Nemov 磁坐标 / BoRiS：Bonnin 等 2005 Nuclear Fusion，正式版全部 8 页、11 幅原图；解析 W7-X 核心、磁岛与层流 SOL 的多区域坐标和梯度输运，核查 VMEC 基准、磁通归一化、磁剪切及图文疑点；完成离线桌面、窄屏和打印检查（2026-10-10）。
- 约束优化磁面拟合 / MEGPy：Snoep 等 2023 Physics of Plasmas，10 幅原图、1 张完整参数表；解析 Turnbull–Miller、Fourier 与 MXH 的鲁棒拟合、角度对应和自洽径向导数，核查四个 GENE 算例的非一致收益与当前代码残差差异；按要求未使用浏览器检验（2026-10-05）。
- 角度谐波磁面参数化 / MXH：Arbon–Candy–Belli 2021 PPCF，上传 Accepted Manuscript 共 6 页、5 幅原图；解析拟合流程、径向导数、Miller 退化、Fourier 收敛与 NEO/CGYRO 输运比较，核查六阶参照和误差数字的证据边界（2026-10-05）。
- 守恒与多阶段训练 / CM-PINN：Deng–Han 2026 Chinese Physics B，6 幅原图、3 张原表及训练算法；解析 Zakharov 耦合系统与 NLS 的守恒约束，静态核查印刷公式与公开代码差异、精度收益和效率结论的证据边界（2026-10-03）。
- 辛神经算子 / SNO：Makara 等 2026 arXiv v1，25 个编号原图（24 幅去重内容）、10 张原表；解析自伴 Fourier 算子与梯度剪切，核查长时定理条件、无限维可微性反例、四类 PDE 实验和公开代码差异（2026-10-01）。
- 神经算子分裂 / DISCO：Serrano 等 ICML 2026 arXiv v2，17 幅原图、9 张原表、2 个算法；解析冻结权重下的测试时搜索、算子组合与参数外推，核查目标观测条件、计算开销、参数辨识及图文差异（2026-09-30）。
- Poincaré 截面约束 / DESC：Elmacioglu 等 2026 arXiv v1，6 幅原图、1 张原表；解析全截面约束、初猜与力残差归一化，核查冷暖重求解和 QH 优化对比。
- AI–GX / DESC / T3D：Churchill 等 2026 arXiv v1，12 幅原图，临界梯度优化、输运加速与代理失效分析。
- GKI/ITEF：Kawazura–Barnes 2018 arXiv v2，7 幅原图，164 处离线数学表达。
- MXH–Chebyshev / VEQ / VEQ-R：三文对照，25 幅原图、12 张原表；补入环向旋转模型、基准验证与图文核查（2026-09-28）。
- MEGA 与 M3D-C1-K：混合模型专题比较。
- 热离子与鱼骨模：Liu 等 2022 arXiv v1，16 幅原图。
- LHD 高 beta 维持：Sato–Todo 2021，9 幅原图。

共十五份主报告与一份课程自学手册，180 幅去重原图（含多论文对照报告与课程原图）。专题目录保留 M3D-C1-K 附录副本以兼容原有内部链接；主页不重复收录。

## 新增报告

1. 将 HTML 报告及其完整资源目录放到 `reports/<主题>/`。
2. 在 `assets/library.js` 的 `reports` 数组中添加标题、作者、年份、标签、摘要与相对链接。`id` 应唯一且稳定。
3. 首页数量随报告列表自动更新。
4. 检查图片、公式和内部跳转后提交。

## GitHub Pages

当前 GitHub 仓库为公开仓库，已启用 GitHub Pages；仓库内容与网页均可公开访问。网站地址：[Reading Club](https://cheneycchen.github.io/reading-notes/)。

网站随 `main` 分支更新，通过 GitHub Pages 构建与部署。报告与资源使用相对路径，兼容 `/reading-notes/` 项目地址，也可直接本地打开。更改仓库可见性或访问权限应单独决定。

原文插图及论文内容的权利归原作者／出版方所有；阅读分析以各报告声明的原文版本与证据边界为准。

## 阅读样式与检查

首页采用暖米白底、Newsreader 衬线与窄栏文字目录，保留搜索、主题筛选、排序、收藏和阅读状态。右上角开关可切换深浅色，选择保存在当前浏览器并在报告间沿用。Newsreader 字体随站点提供，许可见 `assets/fonts/OFL-Newsreader.txt`；中文采用设备上的宋体或衬线字体。

- 共享样式与主题逻辑：`assets/editorial.css`、`assets/theme.js`。
- 修改后运行 `python3 scripts/sync-editorial.py`，将主题内嵌到全部报告。报告仍可单独离线阅读，缺少站点字体时使用系统衬线字体。
- 内容完整性回归：`npm run test:content`。
- 浏览器回归：`npm ci`、`npx playwright install chromium`，启动 `python3 -m http.server 8766` 后运行 `npm run test:browser`。
- GitHub Actions 检查桌面与 390/320 像素布局、筛选收藏、主题切换、原图公式、课程导航、自测、阅读进度与原 PDF；确认已移除交互可视化及其专用资源。

### Plasma scientific illustrations

Eight static, accessible SVG diagrams supplement Lectures 1–8: Debye shielding,
gyromotion, loss cone, Liouville shear, small-angle scattering, CGL compression,
magnetized diffusion, and shear Alfvén polarization. They match the existing
light/dark reading theme and scroll locally on narrow screens. Each caption
states the physical assumptions and distinguishes schematic geometry from an
actual trajectory.

Regenerate inline and standalone diagrams with
`python3 scripts/build-plasma-illustrations.py`. Sources and editable SVG files
are kept in the repository; no TeX installation or external image service is
required. Original lecture prose, equations, figures, PDFs and interactions are
unchanged. `npm run test:content` verifies reversible byte preservation against
commit `c8a831f`; `npm run test:browser` covers the new diagrams at 1440, 390 and
320 pixels in both themes. Set `QA_DIR` to choose a screenshot directory.
