# Assumption Audit

Use this mode when the problem is still trapped inside familiar language.

## Goal

Expose which parts of the current story are:

- direct facts
- interpretations
- assumptions
- conclusions pretending to be facts

## When This Mode Is Usually Right

- the user's framing feels too confident
- the current story already contains a conclusion
- the team is debating a recommendation without agreeing on what must be true
- the problem statement sounds inherited rather than observed

## Output Pattern

1. Rewrite the claim in one sentence
2. Split facts, assumptions, and judgments
3. Highlight the 1-3 assumptions carrying most of the decision weight
4. State what would weaken or falsify those assumptions
5. Recommend what to test, measure, or reframe next

## Workflow

1. Rewrite the user's problem in one sentence
2. Extract every hidden dependency behind the claim
3. Mark each statement as `fact`, `assumption`, or `judgment`
4. Identify the 1-3 assumptions that carry most of the decision weight
5. Recommend what to test, measure, or reframe next

## Useful Prompts

- "What must be true for this belief to hold?"
- "Which part of this is directly observed?"
- "Which part is inherited from convention?"
- "If this assumption failed, would the whole plan collapse?"

## High-Signal Prompts

- "What would have to be false for this recommendation to break?"
- "Which statement here sounds factual but is really interpretive?"
- "What are we borrowing from category language instead of direct observation?"
- "Which assumption is most expensive if wrong?"

## Mini Example

Claim:

- "We need enterprise features to grow."

Audit:

- fact: larger customers asked for security and audit controls
- assumption: enterprise demand is the main growth bottleneck
- assumption: current self-serve users are near exhausted
- judgment disguised as fact: "enterprise" is the obvious next market

Next move:

- test whether deals are actually being lost on enterprise requirements or on something earlier like trust, ROI, or onboarding

## Failure Modes

- Treating team consensus as evidence
- Treating category language as proof
- Smuggling the analyst's preferences in as constraints, or dismissing the user's explicit requirements as mere assumptions

## Boundary

Use this mode to clean the framing before deeper decomposition. If the problem is already well-defined and the issue is mostly cost, capacity, or system design, switch to another mode after the audit.
