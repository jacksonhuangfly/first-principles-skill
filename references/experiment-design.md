# Experiment Design

Use this mode when a good answer depends on evidence that does not yet exist.

## Goal

Convert uncertainty into the smallest cheap test that changes the decision.

## When This Mode Is Usually Right

- the user wants certainty that does not yet exist
- multiple explanations sound plausible
- the next decision depends on one high-weight assumption
- the team is about to commit major resources without a cheap read

## Output Pattern

1. Critical assumption
2. Evidence that would raise or lower confidence
3. Smallest falsifiable test
4. Success threshold defined in advance
5. Kill / continue / redesign rule
6. An inconclusive outcome and what additional evidence it would require

## Workflow

1. Identify the critical assumption
2. Define what evidence would increase or decrease confidence
3. Design the smallest falsifiable test
4. Set a success threshold before running it
5. Set the comparison, observation window, sample requirement, and guardrails
6. Describe how success, failure, and inconclusive evidence change the decision

## Good Experiment Properties

- low cost
- fast feedback
- one dominant variable
- measurable outcome
- clear kill / continue rule

## Experiment Ladder

1. desk check or data sanity check
2. manual or concierge test
3. smoke test for demand or behavior
4. small-cohort behavioral test
5. production rollout only after the earlier layers teach something

## Mini Example

Assumption:

- "Users need real-time generation here."

Proposed test (illustrative thresholds, to agree on before recruitment):

- Compare batching with the existing real-time path in eligible, consenting workflows.
- Use a measured task-completion baseline; suppose it is 90% in a hypothetical example.
- Require at least a 20% reduction in cost per completed task and a completion-rate difference whose 95% confidence interval stays above -2 percentage points.
- Plan sample size for that tolerance before starting, and observe the primary outcome for at least 14 days. If the available cohort is too small, call this a feasibility pilot rather than an equivalence test.
- Stop for a critical reliability incident; track support burden and delay-sensitive failures as guardrails.
- Review 30-day retention when it becomes observable before deciding on a broader rollout.
- Continue only if the pre-agreed thresholds and guardrails hold. Roll back on harm; treat a confidence interval that crosses the tolerance as inconclusive rather than as proof of no decline.

See the [worked product-cost example](../examples/product-cost-breakdown.md) for
the connection between a cost model, a hypothesis, and a decision rule.

## Failure Modes

- testing too many assumptions at once
- designing a test that mainly produces vanity metrics
- collecting data without a decision threshold

## Boundary

If the problem is still poorly defined, return to assumption audit or concept clarification first. A bad experiment on a bad question is still a bad experiment.
