# RunThePaper README 设计参考

> 调研时间：2026-07-13（Asia/Shanghai）  
> 范围：只查看仓库自己的 GitHub 首页、README 与 GitHub API，不采用第三方榜单或解读文章。Stars 只是流行度快照，不代表 README 质量排名。

## 先给结论

RunThePaper 不应照搬某一个热门仓库，而应组合三种成熟模式：

- 排版学 [OpenAI Codex](https://github.com/openai/codex) 和 [MLX](https://github.com/ml-explore/mlx) 的克制：一句话定位、少量入口、短路径；
- 可信度学 [Transformers](https://github.com/huggingface/transformers) 的可验证徽章、明确边界和最小可运行示例；
- 目录与社区模型学 [Papers We Love](https://github.com/papers-we-love/papers-we-love) 和 [Public APIs](https://github.com/public-apis/public-apis)：先让读者找到目标，再逐层进入详情；
- 内容叙事可以参考 [LangChain](https://github.com/langchain-ai/langchain) 的“是什么 → 立刻试用 → 为什么值得用 → 资源与参与”，但不要引入它的产品生态复杂度。

RunThePaper 首页最重要的不是展示 Agent 技术，而是让读者在十几秒内回答四个问题：

1. 这是什么项目？
2. 已经复现了哪些论文？
3. 每篇复现可信到什么程度、可以拿到什么？
4. 我怎样运行、提需求或参与？

## 数据快照与一手来源

| 仓库 | Stars（快照） | 为什么纳入 | 一手来源 |
| --- | ---: | --- | --- |
| openai/codex | 97,516 | AI Agent 工具，首屏和 Quickstart 极简 | [README](https://github.com/openai/codex/blob/main/README.md) · [GitHub API](https://api.github.com/repos/openai/codex) |
| huggingface/transformers | 162,558 | AI / 科研基础设施，可信度与边界表达成熟 | [README](https://github.com/huggingface/transformers/blob/main/README.md) · [GitHub API](https://api.github.com/repos/huggingface/transformers) |
| langchain-ai/langchain | 141,630 | Agent 平台，内容顺序和行动路径清晰 | [README](https://github.com/langchain-ai/langchain/blob/master/README.md) · [GitHub API](https://api.github.com/repos/langchain-ai/langchain) |
| papers-we-love/papers-we-love | 107,783 | 论文社区与资料目录，和 RunThePaper 的对象最接近 | [README](https://github.com/papers-we-love/papers-we-love/blob/main/README.md) · [GitHub API](https://api.github.com/repos/papers-we-love/papers-we-love) |
| public-apis/public-apis | 449,495 | 大型目录型项目，可观察索引和表格的规模化方式 | [README](https://github.com/public-apis/public-apis/blob/master/README.md) · [GitHub API](https://api.github.com/repos/public-apis/public-apis) |
| ml-explore/mlx | 27,530 | 面向科研人员的技术项目，导航与信息密度控制好 | [README](https://github.com/ml-explore/mlx/blob/main/README.md) · [GitHub API](https://api.github.com/repos/ml-explore/mlx) |

## 逐个仓库观察

### 1. OpenAI Codex：把主路径压到最短

[Codex README](https://github.com/openai/codex/blob/main/README.md) 的首屏是一句直接定义产品的话，再配一张居中的产品图。没有徽章墙，也没有长篇愿景。内容顺序是：定位和使用入口 → Quickstart → 登录方式 → 文档 → License。

它的 Quickstart 很有效：安装之后立刻告诉用户运行什么命令。README 还主动区分 CLI、IDE、App 和 Web，先消除产品定位混淆。

适合 RunThePaper：

- 首屏只用一句话讲清“开放、可运行、可检查的论文复现目录”；
- 紧接三个主入口：`浏览论文复现`、`提交复现需求`、`参与项目`；
- README 只保留读者主路径，维护脚本和发布流程放在 `CONTRIBUTING.md`；
- 技术愿景只需一小段，不要在目录前展开 Agent 架构。

不适合照搬：

- 80% 宽的大型 splash 图会把论文目录挤出首屏；RunThePaper 的核心视觉证据应该是复现结果，而非品牌海报；
- 过度精简也不可取，因为复现状态、证据和边界本身就是产品的一部分。

### 2. Hugging Face Transformers：所有“可信”信息都可点击验证

[Transformers README](https://github.com/huggingface/transformers/blob/main/README.md) 用品牌 Logo、构建状态、License、文档、Release、贡献公约和 DOI 形成可信度层级；这些徽章都指向实际页面，不是装饰。随后给出一句定位、规模证据、安装、Quickstart、适用理由、明确的不适用场景、社区和引用方式。

它的 Quickstart 不只给安装命令，还给最小代码和预期结果；较长的多模态示例用 `<details>` 折叠，避免主路径被淹没。它同时写“为什么使用”和“什么时候不该使用”，这是很成熟的边界表达。

适合 RunThePaper：

- 只放能够验证的徽章，例如 License、公开 case 数、检查状态；没有 CI 时不要做 CI 徽章；
- 中英文入口应在首屏可见，但保持为一行，不复制超长语言导航；
- 增加一个最小 case 运行示例，至少包括进入目录、安装依赖、运行脚本和产物位置；
- 把“我们提供什么 / 不保证什么”并列说明：分数是证据覆盖度，不是物理正确率；
- 将来增加 `CITATION.cff` 后，可像 Transformers 一样提供标准引用入口。

不适合照搬：

- 大图、徽章和语言入口全部堆在首屏会制造噪声；
- RunThePaper 首要动作是浏览论文，不是安装一个通用软件包，不能让安装说明压过目录。

### 3. LangChain：先让读者成功，再解释完整价值

[LangChain README](https://github.com/langchain-ai/langchain/blob/master/README.md) 的顺序很清楚：Logo 与一句定位 → 少量徽章 → 一段产品定义 → Quickstart → 生态入口 → Why use → Resources。读者在看到长篇优势之前，已经能用一条安装命令和几行代码跑出结果。

资源区也处理得很规整：文档、API reference、讨论区、课程、贡献指南和行为准则分别承担不同任务。

适合 RunThePaper：

- 目录后尽快给出“运行一个 case”的成功路径，然后再解释复现质量体系；
- 把读者资源分成互不混淆的入口：案例、方法、需求、贡献、Roadmap；
- “Why RunThePaper”只保留两三个与读者有关的结果：更快 follow 工作、可检查的研究 baseline、为科研 Agent 提供更详细的训练和评测资产。

不适合照搬：

- LangChain 的多个关联产品需要生态导航，RunThePaper 目前没有这个问题；
- 不要把 Agent、Note、公众号和 GitHub case 写成四个并列产品。核心对象只有“公开复现 case”，其他都是生产方式或传播渠道。

### 4. Papers We Love：先讲社区与目录，再讲如何加入

[Papers We Love README](https://github.com/papers-we-love/papers-we-love/blob/main/README.md) 用一段话同时说明社区是什么、仓库是什么。版权边界放得很早：无权托管论文时只提供外部链接。根目录按领域组织，例如 [Physics](https://github.com/papers-we-love/papers-we-love/tree/main/physics) 和 [Quantum Computing](https://github.com/papers-we-love/papers-we-love/tree/main/quantum_computing)，再由领域 README 列论文，形成“领域 → 论文”的两级导航。

参与方式是动作化的：推荐论文、改进组织、加入讨论、启动分会；不是泛泛说“欢迎贡献”。

适合 RunThePaper：

- 项目定位同时表达“开放社区”和“公开复现目录”；
- 版权边界要清晰：不重新分发论文 PDF、源文件或原始图片，原图只在合法范围内做必要引用和对照；
- 参与阶梯写成明确动作：提交论文 → 运行并报告问题 → 审核结果 → 扩展 case；
- 当案例明显增多时，可采用“物理领域 → case”的两级目录。

不适合照搬：

- Papers We Love 主要依赖文件树发现论文，根 README 没有统一的完整论文表；RunThePaper 当前只有 10 个 case，应保留首页完整目录；
- 它的论文条目没有状态、Note、代码、图和 checks 等统一字段，不能满足复现项目的可信度要求；
- 批量下载 PDF 的 Quickstart 与 RunThePaper 的版权边界不一致。

### 5. Public APIs：目录项目需要索引，但首屏不能被次要内容占领

[Public APIs README](https://github.com/public-apis/public-apis/blob/master/README.md) 的核心优点是规模化检索：先给分类 Index，再使用固定字段表格列条目，每个分类结束提供回到索引的链接。这个结构在数百条内容下仍然能导航。

但它当前的首屏被 APILayer 品牌图、产品表和社区广告占据，真正的公共 API 索引要向下滚动较远才能看到。这说明“热门目录仓库”的排版也可能偏离普通读者的第一需求。

适合 RunThePaper：

- case 增多后增加领域索引，并让领域名链接到表格锚点或独立目录页；
- 每个条目使用稳定字段，而不是临时写一段说明；
- 在完整目录中保留直接资源链接，减少读者来回寻找。

不适合照搬：

- 任何赞助、项目背景或 Agent 愿景都不应出现在论文目录之前；
- 过宽表格在移动端难读。RunThePaper 不宜把标题、期刊、领域、状态、分数、Note、代码、图、checks 全塞进一张表；
- “回到目录”链接只有在 README 很长时才有价值，目前不必增加。

### 6. Apple MLX：科研工具也可以非常克制

[MLX README](https://github.com/ml-explore/mlx/blob/main/README.md) 开头直接给 `Quickstart | Installation | Documentation | Examples` 四个链接，只放一个 CI 徽章。随后用一句话定位项目，再列核心特性、设计目标、示例、Quickstart、安装、贡献和引用。

MLX 把“为机器学习研究者设计”的定位与具体设计特性相连，没有用空泛愿景代替证据；同时在末尾提供 Citation，符合科研用户习惯。

适合 RunThePaper：

- 顶部导航控制在 4–5 个入口；
- 愿景必须连接到具体资产：Note、代码、数据、图和 checks；
- 增加 Citation 与可复用引用格式，会让项目更像科研基础设施而非内容合集；
- 贡献与引用放在后半段，不打断读者寻找论文的主路径。

不适合照搬：

- MLX 是软件框架，特性列表是核心；RunThePaper 是 case 目录，不需要在首页列一长串 Agent 能力；
- Quickstart 不能只链接外部文档，应让读者直接在 README 看到最短命令。

## 对 RunThePaper 的具体内容编排

建议首页严格采用下面的顺序：

### 1. 首屏：一句定位 + 三个动作

首屏只承担“认知”和“行动”，建议控制在约 8–12 行 Markdown：

1. `RunThePaper` 项目名；
2. 一句中文或中英双语定位；
3. 一句可验证的项目规模，例如“10 个公开复现 case”；
4. 两到三个真实徽章；
5. 三个入口：浏览复现、提交需求、参与项目。

不要在首屏展开：Agent 架构、审计分数算法、完整愿景、维护命令、版权长说明。

### 2. 论文复现目录：README 的主产品

当前约 10 篇论文，完整目录应继续留在首页。为了移动端可读，建议将表格压缩为四列：

| 论文 | 期刊 / 年份 | 复现状态 | 资源 |
| --- | --- | --- | --- |
| 标题链接到 case | DOI 或 arXiv | 统一状态标签 | 中文 · English · Code · Figures |

“研究主题”可放进 case 页面，或作为论文标题下的一行短描述；审计分数放进详细索引和 case 页面，不应成为首页横向比较数字。状态标签必须紧邻一个简短图例，避免读者自行猜测 complete、feature-level、reduced-scale 的区别。

当 case 超过约 20–30 个时，再升级为：

- 首页展示 Featured / Latest cases；
- 按 Non-Hermitian、Quantum Computing、Many-body、Quantum Simulation 等领域提供二级入口；
- `CASES.md` 或专门目录页承载完整可筛选清单。

### 3. Quickstart：让一个 case 真正跑起来

Quickstart 的目标不是展示所有脚本，而是证明“runnable”。建议只选择一个 paper-parameter complete 的代表 case，提供：

1. clone 仓库；
2. 安装该 case 所需依赖；
3. 运行一张代表图；
4. 告诉读者生成文件的位置；
5. 链接到该 case 的完整命令。

命令必须在 CI 或发布检查中实际执行；如果仓库还没有一条跨环境可靠的最短命令，宁可暂时不给徽章，也不要展示未经验证的“Quickstart”。

### 4. 复现可信度：短规则 + 深链接

首页只保留三条最重要的规则：

- 最终公开复现优先使用论文原参数；无法做到时明确标注 reduced-scale、subset、proxy 或 blocked；
- audit score 衡量证据覆盖程度，不代表物理正确率或论文间排名；
- 每个 case 都公开 Note、运行代码、生成产物、checks 和限制说明。

评分公式、容差、验证层级和完整边界放到独立方法页，并从这里链接过去。这样既建立信任，也不让 README 变成审计规范全文。

### 5. 参与：按门槛从低到高排列

建议避免一大段“欢迎大家参与”，而改为四个动作：

1. **Request**：提交标题、DOI/arXiv 和最关心的图或结论；
2. **Run**：运行已有 case，报告环境或数值问题；
3. **Review**：检查公式、参数、图和限制声明；
4. **Extend**：补充新图、更多尺度或完整 case。

每个动作只给一个明确链接。对普通读者，Issue 是主入口；对贡献者，再进入 `CONTRIBUTING.md`。

### 6. 项目愿景、Citation、License

Agent4Science 愿景适合放在后半段，用两三句话说明：自研 Agent 是生产和检查复现 case 的方法，公开 case 才是项目交付物。随后提供 Roadmap、Citation、License 和第三方版权边界。

## 排版规则

- 顶部导航不超过 5 项；同类入口不要重复出现在三处。
- 徽章控制在 2–4 个，且每个徽章都必须指向可验证页面。
- 一屏只出现一个主要视觉焦点；项目初期不需要大型品牌图。
- 表格优先服务扫描，不承担解释；长说明放在 case 或方法页。
- 中英文入口统一命名并保持同一位置，不在每段重复双语。
- README 主体使用英文或中英对照均可，但标题、状态和资源词汇要全仓一致。
- 使用 `<details>` 只折叠真正的次要内容，不把关键限制隐藏起来。
- 重要链接使用动作词：Browse、Run、Request、Review，而不是笼统的 More。

## 明确不建议采用的模式

- 徽章墙：GitHub 本身已显示 Stars/Forks，不需要重复做流行度装饰；
- 首屏长愿景：会推迟读者看到论文目录；
- 大幅封面：公众号需要封面，GitHub README 不一定需要同一张视觉资产；
- 全字段巨表：移动端不可读，且会把不同维度压成横向评分；
- 把所有 10 个 case 都叫“完整复现”：状态必须真实反映 paper-parameter、feature-level 或 reduced-scale；
- 重复入口：README、`CASES.md`、case README 各自承担不同层级，不应复制同一段长说明；
- 广告或生态前置：Agent、公众号和未来产品都不能抢在公开 case 目录之前。

## 推荐的信息架构

```text
README
├── 项目定位与主入口
├── 全部论文目录（当前阶段）
├── 运行一个代表 case
├── 复现质量的三条规则
├── 参与路径
└── 愿景 / Citation / License

CASES.md
├── 完整元数据
├── audit score
├── limitation
└── 领域与状态索引

cases/<paper-id>/README.md
├── 论文与复现结论
├── 关键结果 / 图
├── 运行说明
├── checks
└── 复现边界

CONTRIBUTING.md
├── 新增 case 流程
├── 目录生成与校验
├── 测试要求
└── 提交流程
```

核心原则是：README 负责让读者发现和进入，`CASES.md` 负责完整索引，单篇 case 负责证据，`CONTRIBUTING.md` 负责维护流程。这样既借鉴热门仓库的成熟排版，又不会丢掉 RunThePaper 最有辨识度的“可运行、可检查、边界明确”的复现模型。
