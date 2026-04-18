# Zero-Based Redesign

Use this mode when the current system has too much history inside it.

## Goal

Rebuild the smallest system that still delivers the desired result.

## When This Mode Is Usually Right

- the current flow feels bloated, slow, or hard to explain
- many steps exist only because of other bad steps
- the system has accumulated features, approvals, or tools over time
- local optimization is no longer improving total outcome

## Output Pattern

1. Define the result in user terms
2. List the minimum necessary components
3. Identify deletions and postponements
4. Propose the shortest viable path from intent to outcome
5. Name the main risk and the smallest check against it

## Workflow

1. Define the result in user terms
2. Ignore the current implementation temporarily
3. Ask what the minimum necessary components are
4. Remove steps, roles, tools, and features that are not essential
5. Reintroduce only what earns its place

## Core Question Set

- If we started today, would we build it this way?
- What is the shortest path from intent to outcome?
- Which steps exist only to support other bad steps?
- Which features defend complexity rather than create value?

## Deletion Tests

- If we remove this step, what user outcome breaks?
- Is this step preserving value or preserving familiarity?
- Is this feature needed by the user or by the current org chart?
- Are we optimizing around a dependency that should itself be removed?

## Mini Example

System:

- a seven-step approval process for publishing a small product update

Redesign move:

1. define the real result: safe release with clear ownership
2. keep only version control, automated checks, and one accountable approver
3. delete review steps that mainly exist to diffuse responsibility
4. reintroduce only what earns its place after the simple path exists

## Design Bias

Prefer:

- deletion before optimization
- manual proof before automation
- one clear path before many optional branches

## Failure Modes

- rebuilding around the current org chart instead of the user outcome
- preserving legacy exceptions in the first draft of the redesign
- adding optionality before proving a simple core path
