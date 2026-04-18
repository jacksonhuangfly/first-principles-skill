# Classic First-Principles Cases

Use this file when the user asks for canonical examples of first-principles reasoning rather than a direct decomposition of their own problem.

## Why These Cases Matter

These are illustrative decompositions, not verified accounts of a particular
person's decision process or evidence of current technical feasibility. For the
historical SpaceX proposal, see the [Mars source capture](sources/articles/musk-mars-first-principles-source-card.md)
and its limitations. This repository has no primary battery-cost study.

The cases illustrate how to:

- start below inherited price or convention
- separate physical limits from industry structure
- ask what must be true in atoms, energy, materials, or process
- rebuild the system from those lower-level constraints

## Case 1: Going To Mars

Why it matters:

- shows the difference between "industry says impossible" and "physics says impossible"
- reframes cost from legacy aerospace pricing to material cost plus system design
- illustrates how reusability changes the cost equation

Core move:

1. Ignore current launch pricing as the base truth
2. Ask what a rocket is made of
3. Ask what the material cost floor looks like
4. Ask which part of current cost comes from one-time use and institutional process
5. Compare architectures involving reusability and local fuel production, including their reliability, mass, energy, and logistics requirements

## Case 2: Battery Cost

Why it matters:

- moves from auto-industry pricing assumptions to chemistry and manufacturing realities
- shows how first principles can attack "permanent" cost beliefs

Core move:

1. Ignore the inherited price of finished battery packs
2. Break the pack into raw materials and process steps
3. Ask which costs are truly material-bound and which are process-bound
4. Compare manufacturing alternatives using a dated, chemistry-specific bill of materials and measured yield, processing, integration, and warranty costs

A material floor is a lower bound, not a forecast of an achievable pack price.
Do not assume all battery chemistries use the same materials or that current
market prices can be inferred from this example.

## Transfer Pattern

When moving from these classic cases to a modern product or workflow problem:

1. replace "rocket" or "battery" with the system under discussion
2. ask what the bill-of-materials or bill-of-process looks like
3. separate irreducible cost from path-dependent cost
4. ask what changes if the dominant expensive step becomes reusable, batchable, cacheable, or removable

## When To Use These Cases

Use them to:

- explain what first-principles reasoning feels like
- teach the difference between accepted industry structure and physical reality
- anchor a user's abstract question in a concrete canonical example

## Failure Modes

- using the cases as mythology instead of method
- copying the conclusion instead of the decomposition pattern
- treating every problem like physics when the real blocker is incentives or definitions
