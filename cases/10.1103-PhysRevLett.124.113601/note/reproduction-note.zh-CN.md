# 局域化驱动超辐射不稳定性：像素配准数值复现

## 论文与问题

本公开包复现 Yin 等人在 *Physical Review Letters* **124**, 113601
(2020) 中研究的局域化驱动超辐射不稳定性。核心问题是：准周期势使原子波函数局域化后，
为什么腔散射响应反而会增强，并把超辐射阈值压低到零？

## 独立计算

代码独立实现有限链 Aubry–André / generalized Aubry–André 哈密顿量、态分辨 IPR、
腔散射易感性、线性临界泵浦，以及原子轨道与腔场的自洽平均场迭代。所有公开曲线由包内
CSV 数值重新绘制；论文图像只出现在有限的对照板中，不参与模型计算或图像生成。

## 主要结果

- Fig. 2：移动边界出现在 `alpha=233`、`epsilon_c/J=0.4396`；377 个 IPR
  矢量点的相关系数为 `0.99999999997`。激发态阈值归一化没有公开，因此该目标保持
  exploratory。
- Fig. 3：五个 panel 全部生成。`eta_c(chi=0)/J=0.27681`，Fig. 3(a) 的阈值
  曲线与 PDF 矢量路径相关系数为 `0.99999695`。这是本 case 唯一达到
  `complete_reproduction` 的目标。
- Fig. 4：非线性光子数起点和腔波矢阈值 landscape 均复现；由于 published/arXiv
  detuning convention 分裂，证据等级保持 paper subset。
- Fig. S1：五组 normal/superradiant 密度曲线均生成，十条可见 PDF 矢量路径全部通过
  点对点合同；原文没有给泵浦样本与迭代细节。

完整画布 SSIM 分别为 Fig. 3 `0.8602`、Fig. 4 `0.7921`、Fig. S1 `0.7856`。
这些数字来自独立数值图与论文几何配准后的比较，不是复制原图得到的。

## 运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1103-PhysRevLett.124.113601/code
python scripts/run_linear_targets.py
python scripts/run_nonlinear_targets.py
python scripts/render_pixel_registered.py
```

前两个脚本在 Apple M4 上最近一次完整重跑约为 22.65 秒；渲染与公开检查另需数秒。
数据、图片与 JSON 检查分别写入 `../outputs/data`、`../outputs/figures` 和
`../outputs/checks`。如需隔离验证输出，可设置 `LDSI_OUTPUT_ROOT=/tmp/ldsi-run`。

## 复现边界

Harness 总分为 `88.56/100`，全案等级为 `numerical_feature_reproduction`。
Fig. 2 缺失阈值归一化，Fig. 4 存在版本间公式约定分裂，S1 缺失泵浦样本和迭代元数据。
因此视觉接近不会把这些目标自动升级为完整复现。公开包不包含论文 PDF、原始图、矢量采样
点或内部过程日志。
