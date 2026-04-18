[English](./README.md) | **简体中文**

<div align="center">

# 第一性原理.skill

> *“当我们认为自己认识了一件事物的第一原因时，我们才说自己真正知道了它。”*
> — 亚里士多德，[《形而上学》I.3](https://classics.mit.edu/Aristotle/metaphysics.1.i.html)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-0169CC)](https://openai.com/codex)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-CC785C)](https://claude.ai/code)

把复杂问题拆回定义、事实、假设、约束和实验。

[效果示例](#效果示例) · [安装](#安装) · [方法](#方法) · [资料来源](#资料来源) · [维护](#维护) · [致谢](#致谢与许可证)

</div>

用于产品成本分析、系统与流程重构、抽象问题澄清，以及决定下一步验证什么。包含四个心智模型、八条启发式和六种分析路由。

默认使用英文回答。只有用户明确请求时才切换为简体中文；除非请求限定范围或之后更改，选择在当前对话中延续。其他明确指定的语言也会得到遵循。用中文提问或打开中文 README 本身不会切换 Skill 的回答语言。

## 效果示例

以下示例展示推理方式，不用于证明当前价格、工程可行性或预测结果；这些结论需要针对具体问题收集证据。

### 人类如何前往火星？

先定义任务，再推导成本：

- 需要把多少质量送出地球，这对推进系统和能源有什么要求？
- 飞行途中需要怎样的生命支持、辐射防护和冗余？
- 如何完成进入、下降、着陆、地面活动和返程？
- 哪些补给可以原位生产，这又需要多少设备和能源？

在相同任务和可靠性要求下比较不同方案。重复使用和原位制造燃料都是需要评估的假设。下一步可以先建立质量、能量和补给预算，找出其中影响最大、证据最不足的假设。

### 电动车电池为什么可能继续降价？

拆开电芯化学体系、材料用量、加工、制造良率、电池包组件和寿命要求，再用标明日期的价格与一致的单位，例如每千瓦时可用容量的成本，估算各部分贡献。

原材料成本与电池包价格的差距指向了值得研究的问题，但不代表差额都能消除。在安全、性能和寿命要求不变的前提下，验证最有可能带来明显降本的环节。

### AGI 什么时候会到来？

先定义目标，再预测年份。一个用于讨论的定义可以包括任务能力的广度、跨领域迁移、长期自主性、可靠性和可负担的部署成本。

为每个维度指定可观察的评估方式及尚存差距。一个系统在某个维度表现突出，不代表已经满足其他条件。下一步应验证预测所依赖、但证据最薄弱的能力或前提。

### 产品月费 49 美元，利润越来越薄，应该优化什么？

按每个客户或每次成功完成的任务拆开收入与成本：计算、存储、支付手续费、客服、引导上手和获客。区分持续交付成本与获得一个客户所需的成本。

找出哪些功能和流程真正交付了客户愿意付费的结果。在删掉或重做高成本环节前，先检查它对这个结果的贡献。每次测试一项改动，同时观察利润和任务完成率、留存等客户结果指标。

### 现在还有什么创业机会？

从人们已经在努力完成的任务出发。当前路径哪里慢、贵、不可靠或令人厌烦？哪项约束发生了足够大的变化，使另一种做法成为可能？

更短的路径只是候选机会。需要验证人们是否在意到愿意切换或付费：观察现有流程，试做一个小范围替代方案，再把实际行为与原先假设比较。

### 人生的意义是什么？

先区分几个问题：什么让人觉得值得，什么支撑人在困难中继续投入，什么值得超越短期快感而长期付出时间。不同的人可以有不同且合理的答案。

把答案落回真实经验和选择。一个具体的下一步是选择一项小承诺，观察它对日常生活的影响，并在约定时间后重新评估。个人价值需要反思和行动，不必全部化为实验室里的测试。

## 安装

```bash
npx skills add justinhuangai/first-principles-skill
```

使用 Skill 不需要安装 Python 维护工具。安装后可以这样提问：

```text
从第一性原理看，这个产品真正的瓶颈是什么？
如果从零重建这个流程，哪些步骤仍然必不可少？
拆开这个产品的成本结构，并指出我们还需要测量什么。
当我们说这个系统有智能时，默认了哪些前提？
```

需要切换时，可以明确说：`请在当前对话中使用简体中文回答，直到我另行指定语言。`

## 方法

### 四个心智模型

| 模型 | 用途 |
|---|---|
| 质疑继承的价格与做法 | 先拆开现有价格或流程，再判断它是不是不可突破的限制。 |
| 回到物理机制或用户结果 | 找出系统真正需要的材料、操作和交付结果。 |
| 区分约束与路径依赖 | 区分物理、经济、行为、组织、监管约束，以及历史留下的选择。 |
| 用证据缩小不确定性 | 选择一个可能改变决策的小测试或观察。 |

### 八条启发式

1. 围绕目标结果重写问题。
2. 找出已知事实和缺失证据。
3. 揭示每个结论背后的假设。
4. 分类约束，并检查是什么在维持它。
5. 优化之前，先考虑能否删除。
6. 从目标结果重建，不默认保留现有系统。
7. 把大词拆成明确的维度或问题。
8. 以适合该问题的测试、观察或具体选择收尾。

### 六种路由

| 路由 | 适用问题 |
|---|---|
| [假设审计](references/assumption-audit.md) | 找出判断或计划背后的前提。 |
| [概念澄清](references/concept-clarification.md) | 定义 AGI、质量、价值、意义等概念。 |
| [约束拆解](references/constraint-decomposition.md) | 拆分限制，判断哪些可能改变。 |
| [从零重构](references/zero-based-redesign.md) | 围绕必需功能重建产品或流程。 |
| [实验设计](references/experiment-design.md) | 在加大投入前验证不确定的假设。 |
| [经典案例](references/classic-cases.md) | 通过火箭、电池等案例解释方法。 |

[SKILL.md](SKILL.md) 负责选择路由并规定执行规则。先使用对应的主模式，必要时补充有针对性的[操作模块](references/operations/README.md)，需要深入依据时再查阅调研和来源材料。

## 资料来源

仓库将执行指令、背景笔记和来源记录分开：

- [操作模块](references/operations/README.md)：补充问题定义、需求、成本、治理、决策和战略方面的工具。
- [调研笔记](references/research/README.md)：12 篇主题综合笔记，覆盖解释、系统、经济、度量、决策和意义。它们是工作笔记，不代表其中每个论断都已对照原典验证。
- [来源记录](references/sources/README.md)：11 份记录，包含摘录、转录以及目录或索引材料。目录和索引用于查找资料，不能支撑关于相关著作的所有论断。
- [提炼框架](references/extraction-framework.md)：指导如何将材料转化为可用方法，并区分证据与解释。
- [示例](examples/)：一个使用假设数据的产品成本分析示例，以及其他五类问题的回答提纲。

引用材料支持结论前，应检查对应记录的元数据和证据边界。涉及当前成本、技术、市场或监管时，需要为眼前问题收集当前证据。

## 仓库结构

```text
first-principles-skill/
├── README.md                   # 英文说明
├── README.zh-CN.md             # 简体中文说明
├── SKILL.md                    # 路由与执行规则
├── LICENSE
├── requirements.txt            # 来源采集工具的 Python 依赖
├── references/
│   ├── assumption-audit.md
│   ├── concept-clarification.md
│   ├── constraint-decomposition.md
│   ├── zero-based-redesign.md
│   ├── experiment-design.md
│   ├── classic-cases.md
│   ├── extraction-framework.md
│   ├── operations/             # 补充操作模块
│   ├── research/               # 主题调研笔记
│   └── sources/                # 来源记录、摘录与索引
├── examples/                   # 示例分析
├── scripts/                    # 采集、转换与检查工具
└── tests/                      # 工具回归测试
```

## 维护

以下命令在仓库根目录运行，需要 Python 3.10 或更新版本。使用网页来源采集工具前，安装对应的 Python 依赖：

```bash
python3 -m pip install -r requirements.txt
```

- `scripts/capture_web_source.py`：采集网页或 PDF，并记录来源元数据。必填的 `--language` 参数记录来源原文的真实语言，例如 `en`、`zh-CN` 或其他语言标签；无法确定时使用 `und`。该工具不会翻译原文。
- `scripts/download_subtitles.sh`：下载可用字幕，需要额外安装可选的 `yt-dlp` 命令。
- `scripts/srt_to_transcript.py`：把已有的 SRT 或 VTT 字幕整理为可阅读文本。

字幕下载默认选择英文，先尝试人工字幕，再尝试自动字幕。`--language zh-CN` 只选择明确标记为简体中文的字幕（`zh-Hans`、`zh-CN` 及其变体），同样先人工、后自动。两种模式都不会回退到其他语言。下载器忽略 yt-dlp 配置文件，避免外部设置改变语言选择。命令行提示始终使用英文。将 `VIDEO_URL` 替换为视频地址：

```bash
bash scripts/download_subtitles.sh "VIDEO_URL" outputs/subtitles
bash scripts/download_subtitles.sh --language zh-CN "VIDEO_URL" outputs/subtitles
```

检查与核心测试使用 Python 标准库；安装 `beautifulsoup4` 后，还会运行可选的 HTML 采集测试：

```bash
python3 scripts/check_links.py .
python3 scripts/check_sources_inventory.py .
python3 scripts/check_research_repetition.py references/research
python3 -m unittest discover -s tests -v
```

这些检查验证文档结构、来源元数据、重复文本和工具行为，不能证明调研结论真实或生成的回答有效。修改项目说明时应同时检查两种语言版本；更新调研内容时应保留来源局限。

## 使用边界

- Skill 提供推理结构，不能替代缺失的一手证据。
- 更清晰的拆解可以揭示假设，但不等于已经验证假设。
- 简化方案必须保留必要的结果、质量、安全和适用约束。
- 历史案例用于解释方法，不能证明当前的可行性或价格。
- 它不能替代合格的法律、医疗或财务专业意见。

## 致谢与许可证

本仓库由 Jackson Huang 维护，借助 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 搭建。感谢女娲的作者和贡献者提供的工具。

本项目原创内容基于 [MIT License](LICENSE) 开源。引用和摘录的第三方材料仍适用各自的权利与条款，收录到本仓库不代表将其重新许可为 MIT。
