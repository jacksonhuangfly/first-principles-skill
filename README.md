**English** | [简体中文](./README.zh-CN.md)

<div align="center">

# First Principles.skill

> *“We say we know each thing only when we think we recognize its first cause.”*
> — Aristotle, [*Metaphysics* I.3](https://classics.mit.edu/Aristotle/metaphysics.1.i.html)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-0169CC)](https://openai.com/codex)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-CC785C)](https://claude.ai/code)

Reduce complex problems to definitions, facts, assumptions, constraints, and experiments.

[Examples](#examples) · [Installation](#installation) · [Method](#method) · [Sources](#sources) · [Maintenance](#maintenance) · [Credits](#credits-and-license)

</div>

A skill for analyzing product costs, redesigning systems and workflows, clarifying abstract questions, and deciding what to test next. It uses four mental models, eight heuristics, and six routes.

Responses default to English. Switch to Simplified Chinese with an explicit request; that choice continues in the current conversation unless you limit its scope or change it. Other explicitly requested languages are also honored. Writing a prompt in Chinese or opening the Chinese README does not switch the skill's response language.

## Examples

These examples illustrate the reasoning pattern. They do not establish current prices, engineering feasibility, or forecasts; those require evidence for the specific case.

### How would humans get to Mars?

Start with the mission, then derive its costs:

- What mass must leave Earth, and what propulsion and energy does that require?
- What life support, radiation protection, and redundancy are needed during transit?
- How will entry, descent, landing, surface operations, and the return journey work?
- Which supplies could be produced locally, and what equipment and energy would that take?

Compare architectures under the same mission and reliability requirements. Reusability and local fuel production are hypotheses to evaluate. A useful next step is a mass, energy, and logistics budget that exposes the largest uncertain assumption.

### Why might EV batteries become cheaper?

Separate cell chemistry, material quantities, processing, manufacturing yield, pack components, and lifetime requirements. Then estimate each contribution using dated prices and a consistent unit, such as cost per usable kWh.

A gap between material costs and pack prices identifies questions to investigate; it does not prove that the gap is removable. Test the largest plausible cost lever while holding safety, performance, and lifetime requirements constant.

### When will AGI arrive?

Define the target before predicting a year. A working definition might include breadth of task performance, transfer across domains, long-horizon autonomy, reliability, and affordable deployment.

For each dimension, name an observable evaluation and the remaining gap. A system that performs well on one dimension has not necessarily satisfied the others. The next useful step is to test the least-supported capability or dependency behind the forecast.

### Our product charges $49 per month, but margins keep shrinking. What should we optimize?

Break down revenue and costs per customer or successfully completed task: computation, storage, payment fees, support, onboarding, and acquisition. Separate recurring delivery costs from costs incurred to acquire a customer.

Identify which features and process steps deliver the result customers pay for. Remove or redesign a costly step only after checking its contribution to that result. Test one change against both margin and a customer outcome, such as task completion or retention.

### What startup opportunities still exist?

Start with a job people already try to complete. Where is its current path slow, expensive, unreliable, or frustrating? Which constraint has changed enough to make a different approach possible?

A shorter path is a candidate opportunity. Validate that people care enough to switch or pay: observe the existing workflow, test a small alternative, and compare actual behavior with the original assumption.

### What is the meaning of life?

Separate several questions: what feels worthwhile, what sustains commitment through difficulty, and what deserves time beyond short-term pleasure. Different people can reasonably answer them differently.

Connect the answer to lived experience and choices. One concrete next step is to choose a small commitment, observe its effect on daily life, and reconsider it after a defined period. Personal values need reflection and action; they do not all reduce to laboratory tests.

## Installation

```bash
npx skills add justinhuangai/first-principles-skill
```

Using the skill does not require the Python maintenance tools. After installation, try:

```text
From first principles, what is the real bottleneck in this product?
If we rebuilt this workflow from zero, which steps would still be necessary?
Break down this product's cost structure and identify what we need to measure.
What are we assuming when we say this system is intelligent?
```

To switch explicitly, say: `Please answer in Simplified Chinese for the rest of this conversation, unless I ask to change languages.`

## Method

### Four mental models

| Model | Application |
|---|---|
| Question inherited prices and practices | Decompose the current price or process before treating it as a limit. |
| Work from physical mechanisms or user outcomes | Identify the materials, operations, or results the system actually requires. |
| Separate constraints from path dependence | Distinguish physical, economic, behavioral, organizational, and regulatory constraints from inherited choices. |
| Use evidence to resolve uncertainty | Choose a small test or observation that could change the decision. |

### Eight heuristics

1. Rewrite the problem around the desired outcome.
2. Identify established facts and missing evidence.
3. Surface the assumptions behind each conclusion.
4. Classify constraints and check what enforces them.
5. Consider deletion before optimization.
6. Rebuild from the outcome instead of preserving the current system.
7. Split broad concepts into explicit dimensions or questions.
8. End with a test, observation, or concrete choice suited to the problem.

### Six routes

| Route | Use it for |
|---|---|
| [Assumption audit](references/assumption-audit.md) | Finding the premises behind a claim or plan. |
| [Concept clarification](references/concept-clarification.md) | Defining terms such as AGI, quality, value, or meaning. |
| [Constraint decomposition](references/constraint-decomposition.md) | Separating limits and identifying which could change. |
| [Zero-based redesign](references/zero-based-redesign.md) | Rebuilding a product or workflow around its necessary functions. |
| [Experiment design](references/experiment-design.md) | Testing an uncertain assumption before a larger commitment. |
| [Classic cases](references/classic-cases.md) | Explaining the method through cases such as rockets and batteries. |

[SKILL.md](SKILL.md) selects the route and defines the execution rules. Start with the relevant route, add a targeted [operational module](references/operations/README.md) if needed, and consult research and sources when deeper grounding is useful.

## Sources

The repository separates working instructions from background notes and source records:

- [Operational modules](references/operations/README.md): supplemental tools for framing, demand, costs, governance, decisions, and strategy.
- [Research notes](references/research/README.md): 12 thematic syntheses covering explanation, systems, economics, measurement, decisions, and meaning. These are working notes, not a claim that every statement has been verified against an original text.
- [Source records](references/sources/README.md): 11 records containing excerpts, transcripts, and catalog or index material. A catalog or index is a discovery aid, not evidence for every claim about the associated work.
- [Extraction framework](references/extraction-framework.md): guidance for turning source material into usable methods while keeping evidence and interpretation distinct.
- [Examples](examples/): a worked product-cost example with hypothetical inputs and response outlines for the other five questions.

Check each source record's metadata and evidence boundaries before using it to support a claim. For current costs, technology, markets, or regulations, obtain current evidence for the problem at hand.

## Repository layout

```text
first-principles-skill/
├── README.md                   # English overview
├── README.zh-CN.md             # Simplified Chinese overview
├── SKILL.md                    # Routing and execution rules
├── LICENSE
├── requirements.txt            # Python dependencies for source capture
├── references/
│   ├── assumption-audit.md
│   ├── concept-clarification.md
│   ├── constraint-decomposition.md
│   ├── zero-based-redesign.md
│   ├── experiment-design.md
│   ├── classic-cases.md
│   ├── extraction-framework.md
│   ├── operations/             # Supplemental operational modules
│   ├── research/               # Thematic research notes
│   └── sources/                # Source records, excerpts, and indexes
├── examples/                   # Example analyses
├── scripts/                    # Capture, conversion, and validation tools
└── tests/                      # Tool regression tests
```

## Maintenance

Run these commands from the repository root with Python 3.10 or later. To use the web source capture tool, install its Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

- `scripts/capture_web_source.py` captures a web page or PDF with source metadata. Its required `--language` argument records the source's actual language, such as `en`, `zh-CN`, or another language tag; use `und` when undetermined. It does not translate the source.
- `scripts/download_subtitles.sh` downloads available subtitles; it requires the optional `yt-dlp` command.
- `scripts/srt_to_transcript.py` cleans an existing SRT or VTT file into readable text.

Subtitle downloads default to English, trying manual subtitles before automatic ones. `--language zh-CN` selects only explicitly labeled Simplified Chinese tracks (`zh-Hans`, `zh-CN`, and their variants), with the same manual-then-automatic order. Neither mode falls back to another language. The downloader ignores yt-dlp configuration files to keep external settings from changing this selection. Command-line messages remain in English. Replace `VIDEO_URL` with the video's URL:

```bash
bash scripts/download_subtitles.sh "VIDEO_URL" outputs/subtitles
bash scripts/download_subtitles.sh --language zh-CN "VIDEO_URL" outputs/subtitles
```

The checks and core tests use Python's standard library. Optional HTML capture tests also run when `beautifulsoup4` is installed:

```bash
python3 scripts/check_links.py .
python3 scripts/check_sources_inventory.py .
python3 scripts/check_research_repetition.py references/research
python3 -m unittest discover -s tests -v
```

These checks verify document structure, source metadata, repeated text, and tool behavior. They do not establish the truth of a research claim or the quality of a generated answer. Review both language versions when changing the overview, and keep source limitations visible when updating research.

## Boundaries

- The skill structures reasoning; it cannot supply missing first-hand evidence.
- A clearer decomposition can reveal assumptions without proving them true.
- Simplification must preserve required outcomes, quality, safety, and applicable constraints.
- Historical examples explain a method; they do not establish present-day feasibility or prices.
- It is not a substitute for qualified legal, medical, or financial advice.

## Credits and license

This repository is maintained by Jackson Huang and was assembled with [Nuwa.skill](https://github.com/alchaincyf/nuwa-skill). Thanks to Nuwa's authors and contributors for the tooling.

Original project content is released under the [MIT License](LICENSE). Referenced and excerpted third-party materials retain their respective rights and terms; inclusion in this repository does not relicense them under MIT.
