# Decisions, Metrics, And Experiments

## Why This File Exists

This file brings together probability, calibration, scenario ranges, decision briefs, data gaps, metrics, guardrails, and minimum viable experiments into one operational module for acting under uncertainty.

## When This Lens Is Usually Right

- the user cannot know the answer immediately and needs a testable path
- the system is using overconfident forecasts or thin evidence
- the debate is really about measurement and decision thresholds
- the decision-maker needs a compact frame with next actions

## Core Questions

- What is known, what is assumed, and what is worth measuring next?
- What base rates or outside-view anchors should discipline the forecast?
- Which metrics matter, and what guardrails keep them honest?
- What scenario range is broad enough to be useful but narrow enough to act on?
- What is the smallest discriminating experiment or data check?

## Default Workflow

1. name the decision that actually needs to be made and by when
2. separate directional uncertainty from measurement uncertainty
3. choose the metric, guardrail, and base rate that should discipline the answer
4. design the smallest test that changes the decision, not just the conversation
5. state what action threshold will count as enough evidence

## Common Patterns

- single-number forecast with no range -> false precision
- one metric improving while downside metrics rot -> proxy distortion
- long discussion with no discriminating next measurement -> analysis theater
- leaders want commitment before the cheapest useful experiment is run
- too much data exists but none of it is tied to a decision threshold

## Good Moves

- convert certainty language into ranges or conditions
- name the missing measurement rather than pretending to know
- use guardrails to keep a winning metric from corrupting the system
- keep experiments tied to one critical assumption
- end with a decision frame, not just a commentary stream

## Failure Modes

- using metrics without behavior logic
- running experiments that change too many variables at once
- mistaking dashboard volume for evidence quality
- forcing commitment before cheap learning has happened

## Natural Deliverables

- a short uncertainty map
- the key metrics and guardrails
- a scenario range or decision brief
- the next smallest experiment or data check

## Example Translation

Question: "When will AGI arrive?"

The better move is to stop pretending a year is the primitive. Define the dimensions, use ranges, name the bottlenecks, then specify what evidence would cause the forecast to move.

## Related References

- [experiment-design.md](../experiment-design.md)
- [research index](../research/README.md)

## Included Subthemes

- probability and outside-view reasoning
- scenario ranges and decision thresholds
- metrics, guardrails, and proxy risk
- decision briefs under uncertainty
- minimum viable experiments

## High-Signal Heuristics

- Ranges are often more honest and more useful than precise single-point claims.
- A metric without a guardrail invites local optimization against the system.
- A good experiment kills a bad belief quickly or upgrades a plausible one cheaply.
- If the decision brief cannot state the key unknown, the team is pretending to know too much.

## Mini Cases

- A forecast debate collapses once participants are forced to anchor on base rates and state what evidence would move the range.
- A growth metric rises while trust falls because no one named the guardrail that should have constrained optimization.
- A team keeps discussing an idea because the smallest discriminating test was never designed.

## Quick Checks

- What would change our mind?
- Which metric matters and which metric keeps that metric honest?
- What is the smallest test that could falsify the central claim?

## Useful Prompts

- "What decision are we really trying to unblock?"
- "Which metric matters, and which metric only flatters us?"
- "What base rate or outside-view check should constrain this forecast?"
- "What would we have to observe to change course honestly?"
- "Which experiment is cheap enough to run now but strong enough to kill a bad idea?"
- "What guardrail keeps a local gain from damaging the whole system?"
- "Where are we pretending to measure learning while only measuring motion?"
- "What threshold would make the next step obvious instead of debatable?"

## Observation Checklist

- Tie the analysis to a real upcoming decision.
- Separate directional confidence from numeric precision.
- Choose one primary metric and at least one guardrail.
- Check whether the metric can be gamed cheaply.
- Use an outside-view anchor before trusting a detailed forecast.
- Prefer experiments that change the posterior meaningfully.
- Define a stop rule before running the test.
- Leave with a threshold or trigger, not just an interesting insight.

## Red Flags

- The team is measuring what is easy, not what would change the decision.
- A forecast carries false precision with no base-rate anchor.
- An experiment exists, but no one has defined what result would matter.
- A local KPI is eating the system while everyone celebrates the dashboard.
- The answer optimizes optics rather than information value.
- Evidence keeps arriving without updating the decision logic.
- People want certainty from a test that can only provide directionality.

## Misreadings To Avoid

- Do not confuse an experiment with a demo.
- Do not let one metric stand in for the whole objective unguarded.
- Do not treat small samples as permission to tell a dramatic story.
- Do not delay cheap experiments because they feel less prestigious than planning.
- Do not collect data without precommitting to what would count as signal.
- Do not use “we need more information” when the real issue is decision avoidance.

## Modern Questions This Helps With

- Which metric should govern an AI product where response quality and cost trade off directly?
- How should we test a new onboarding flow without being fooled by vanity conversion?
- What base rates should temper a startup forecast or TAM story?
- How do we decide whether an LLM automation deserves more investment?
- Which guardrails matter when optimizing content, growth, or marketplace engagement?
- What is the minimum experiment that would actually falsify this strategy belief?
