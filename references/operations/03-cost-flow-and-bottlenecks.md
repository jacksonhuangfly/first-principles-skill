# Cost, Flow, And Bottlenecks

## Why This File Exists

This file merges unit economics, queues, bottlenecks, quality variation, reliability, learning curves, and standardization tradeoffs into one operational module for systems that are slow, expensive, or unstable.

## When This Lens Is Usually Right

- the user asks why something is expensive, slow, or operationally messy
- margins keep shrinking and no one can name the cost floor
- support load or rework is growing without one dramatic bug
- throughput collapses after one more approval, handoff, or dependency

## Core Questions

- Which costs are irreducible and which are artifacts of current design?
- Where is work waiting rather than flowing?
- Which bottleneck governs throughput right now?
- How much quality cost is actually rework, variance, or recovery?
- What should become standard because the pattern is now repeatable?

## Default Workflow

1. define the cost or flow unit that actually matters to the decision
2. separate irreducible spend from costs created by current process shape
3. locate the queue, gate, or defect class that governs total throughput
4. translate reliability drift and rework into economic terms
5. propose one subtraction, redesign, or standardization move that changes the cost surface

## Common Patterns

- gross margin story looks fine until support and churn recovery are counted
- local speed improvement just moves the queue downstream
- one more review step catches defects but creates waiting and workarounds
- the system keeps blaming people for common-cause variation
- the process repeats often enough to standardize, but nobody has extracted the stable pattern

## Good Moves

- model cost in units, not in slogans
- treat waiting time as cost
- look for rework hiding inside “service” or “support” categories
- prefer upstream control to late inspection
- differentiate early learning from permanent inefficiency

## Failure Modes

- optimizing price before understanding the cost stack
- treating throughput as a local team problem when the queue is system-level
- assuming more quality control means better quality
- standardizing too early or not standardizing after the pattern is obvious

## Natural Deliverables

- a cost stack by category
- the current bottleneck and queue map
- the main rework or reliability drivers
- the first subtraction or standardization move worth testing

## Example Translation

Question: "Our product charges $49 per month, but margins keep shrinking. How should we optimize it?"

The best move is not to optimize features yet. First separate compute, storage, payment fees, servicing labor, support, acquisition, and churn recovery. Then ask which costs are intrinsic and which are artifacts of product shape, queueing, or avoidable rework.

## Related References

- [constraint-decomposition.md](../constraint-decomposition.md)
- [experiment-design.md](../experiment-design.md)

## Included Subthemes

- unit economics and contribution analysis
- queues and throughput
- quality variation and rework
- learning curves and process maturity
- standardization versus flexibility

## High-Signal Heuristics

- Waiting is cost even when it is not booked as cost.
- A queue is a signal to investigate; check whether it limits end-to-end throughput before calling it the governing bottleneck.
- Support and rework often hide inside stories about margin pressure.
- A stable repeating pattern should eventually leave people’s heads and enter the process.

## Mini Cases

- A subscription business looks healthy until support labor and churn recovery are counted at unit level.
- A team adds approvals to improve quality and accidentally turns the real cost center into waiting.
- A service remains artisanal far longer than needed because no one extracts the repeatable pattern from expert behavior.

## Quick Checks

- Which cost bucket is truly irreducible?
- Where is work stacking rather than flowing?
- Is the current pain a maturity problem, a bottleneck problem, or a reliability problem?

## Useful Prompts

- "What is the real unit here: per user, per job, per month, per transaction, or per incident?"
- "Which cost bucket would survive even after a full redesign?"
- "Where is work waiting rather than progressing?"
- "How much of this margin pressure is really rework, recovery, or support load?"
- "What bottleneck would still govern throughput after two small local optimizations?"
- "Which activity feels expensive only because it is being done at the wrong time or cadence?"
- "What should become standard because it repeats often enough to stop improvising?"
- "What is the cheapest test that tells us whether the cost floor is structural or self-inflicted?"

## Observation Checklist

- Choose one operating unit before discussing gross economics.
- Turn waiting and retry loops into explicit cost categories.
- Check whether the queue is upstream, downstream, or hidden in support.
- Separate one-off learning costs from recurring mature-process costs.
- Look for handoffs that create variance more than insight.
- Count defect prevention and defect recovery separately.
- Ask whether throughput is limited by policy, tooling, or capacity.
- Propose a change that improves the user's target outcome while preserving required speed, cost, and quality limits; state any tradeoffs.

## Red Flags

- The team speaks about margin without naming unit-level costs.
- Quality is being “protected” by adding reviews that only move the queue.
- The bottleneck changes every week because no one defined the actual unit of flow.
- Support, churn recovery, or exception handling are treated as background noise.
- A local team reports speed gains while end-to-end lead time worsens.
- Everyone feels overloaded but no governing constraint is named.
- Process maturity is discussed as culture instead of design.

## Misreadings To Avoid

- Do not treat all cost as equally compressible.
- Do not assume the visible queue is the governing queue.
- Do not confuse inspection volume with reliability.
- Do not standardize a process whose core variation still teaches you something.
- Do not blame individuals for common-cause variation baked into the system.
- Do not cut cost in a way that quietly transfers it to recovery or support.

## Modern Questions This Helps With

- Why does an AI product stay gross-margin fragile even as model prices fall?
- Where is a service team paying hidden cost through exception handling and retries?
- What part of a logistics or approval workflow is truly throughput-limiting?
- Why does a support org grow faster than paying users?
- Which operations should be standardized now that the learning curve is flattening?
- What recurring latency or rework pattern is pretending to be “normal complexity”?
