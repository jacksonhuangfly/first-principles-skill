# Constraint Decomposition

Use this mode when the user feels blocked by cost, time, complexity, scale, or resources.

## Goal

Break constraints into separate buckets so the user stops treating every limit as equally real.

## When This Mode Is Usually Right

- the user keeps saying "we can't" without distinguishing why
- cost, speed, complexity, regulation, or headcount are mixed together
- the team is over-respecting inherited limits
- the next step depends on finding the highest-leverage removable bottleneck

## Constraint Types

1. Physical/mathematical: computation, materials, latency, bandwidth, energy
2. Economic: margin, CAC, payroll, capital intensity, pricing power
3. Behavioral: user attention, trust, habit, switching cost
4. Organizational: approvals, handoffs, ownership gaps, incentives
5. Regulatory/contractual: compliance, contracts, and legal obligations

## Workflow

1. List all stated constraints
2. Classify each one
3. Ask whether it is fundamental, contingent, self-imposed, or an explicit user requirement
4. Find the highest-leverage change within the user's requirements; identify evidence needed before treating a constraint as removable
5. Translate the rest into design rules rather than excuses

## Output Pattern

1. Stated constraints
2. Constraint classification
3. Fundamental vs contingent vs self-imposed, with user requirements kept explicit
4. Highest-leverage removable constraint
5. Design implications for the next version of the system

## Constraint Tests

- What law of nature, user behavior, contract, or budget actually enforces this?
- Does the system break if this constraint is removed, or just become unfamiliar?
- Is this a one-time artifact of current architecture?
- Are we protecting customer value or internal convenience?

## Useful Prompts

- "What law of nature or market behavior enforces this?"
- "What happens if we remove this step?"
- "Who decided this was required?"
- "Is this a real limit or a coordination artifact?"

## Mini Example

Claim:

- "We cannot ship faster because quality will collapse."

Decomposition:

- physical constraint: test runtime
- organizational constraint: serial approvals
- behavioral constraint: low trust between teams
- self-imposed constraint: release policy optimized for legacy risk

Next move:

- attack the approval bottleneck before assuming quality requires the whole current structure
