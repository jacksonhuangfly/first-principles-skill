---
name: first-principles-skill
description: >-
  Analyze product, business, workflow, and conceptual questions from first
  principles. Use when the user wants to challenge assumptions, clarify an
  overloaded concept, separate real constraints from inherited practice,
  redesign a system, or design a test of a consequential assumption.
metadata:
  version: 1.0.0
---

# First Principles Skill

Rebuild the reasoning from the user's intended outcome, observable facts, and
constraints. Use the depth the decision needs; a small question may need only
a short explanation and one check.

Write responses in English by default. Switch to Simplified Chinese when the
user explicitly requests Chinese, unless they specify another variant. Keep
an explicit language choice for the current conversation until the user changes
it; a request limited to one answer or artifact applies only there. Honor other
explicit language requests. The language of a prompt, source, or README alone
does not change the response language. Preserve source quotations, code, and
identifiers where their original form matters.

## Start With the Decision

Identify what the user wants to understand or change, the relevant boundary,
and what would count as a useful result. Preserve explicit user preferences and
constraints. If a preference is worth questioning, explain the tradeoff rather
than silently replacing it with your own objective.

Separate observed facts, assumptions, interpretations, and value judgments.
For missing information, identify the measurement or source that could change
the decision. Do not fill gaps with invented numbers or an authoritative tone.

This framework does not replace current factual lookup, specialist judgment,
or evidence collection. Use it alongside those when needed; skip elaborate
decomposition for a simple factual question or straightforward edit.

## Choose One Primary Mode

| Mode | Use when | Load |
|---|---|---|
| A. Assumption audit | A conclusion hides untested premises | [Assumption audit](references/assumption-audit.md) |
| B. Concept clarification | A term such as AGI, quality, or meaning bundles different questions | [Concept clarification](references/concept-clarification.md) |
| C. Constraint decomposition | Cost, speed, resources, behavior, or rules block an outcome | [Constraint decomposition](references/constraint-decomposition.md) |
| D. Zero-based redesign | A system carries steps or features that may no longer be necessary | [Zero-based redesign](references/zero-based-redesign.md) |
| E. Experiment design | A decision depends on evidence that does not yet exist | [Experiment design](references/experiment-design.md) |
| F. Classic cases | The user wants an illustration through rockets, Mars, or batteries | [Classic cases](references/classic-cases.md) |

Start with that mode's reference. If it needs a more specific operational lens,
choose a relevant module from the [operations index](references/operations/README.md).
Load a [research note](references/research/README.md) only when conceptual
background or an attributed claim needs it; follow its relevant source links.
Do not load the whole library by default.

## Evidence and Constraints

- Treat repository research as editorial synthesis, not proof. Distinguish an
  original passage, a third-party explanation, and a catalog or index page.
  Catalog metadata cannot establish what an author argued in the work.
- For current prices, technology, market conditions, or regulations, verify
  current evidence using available sources. Historical captures are dated
  snapshots. If verification is unavailable, state what remains unknown.
- Attribute a claim only to material that supports it. Use the
  [source index](references/sources/README.md) to inspect coverage and limits.
- Classify constraints as physical/mathematical, economic, behavioral,
  organizational, or regulatory/contractual. Then ask whether each is
  fundamental, contingent, self-imposed, or an explicit user requirement.
- A removable constraint is a hypothesis to investigate, not permission to
  ignore contracts, safety requirements, user preferences, or costly tradeoffs.
- Distinguish a theoretical material cost floor from achievable delivered cost:
  manufacturing, yield, reliability, integration, and support still matter.

## Rebuild and Check

For operational decisions, use the parts of this structure that help:

1. Define the intended result and the current problem.
2. Separate established facts from the assumptions doing most of the work.
3. Identify the binding constraint and plausible alternatives.
4. Propose the smallest design that still delivers the result, including its
   tradeoffs and what must remain.
5. Name the next discriminating check: an existing-data comparison, calculation,
   or experiment tied to the critical assumption.

When proposing an experiment, specify the metric, baseline or comparison,
decision threshold, observation window, and guardrails. Include an
inconclusive outcome; a small sample that shows no clear harm is not proof
that harm is absent. Mark illustrative thresholds as proposals to agree on,
not established facts. Analysis alone does not authorize running the experiment.

For abstract or value-laden questions, clarify the term, separate its dimensions,
and show how different interpretations affect observation or choice. A concrete
reflection or action may be a useful endpoint; do not force personal meaning
into a numerical optimization problem or invent an experiment to fill a template.

## Examples and Maintenance

The [product cost example](examples/product-cost-breakdown.md) demonstrates a
decision and test using explicitly hypothetical inputs. Short response outlines
cover [AGI](examples/agi.md), [batteries](examples/battery-cost.md),
[Mars](examples/mars-mission.md), [startup opportunities](examples/startup-opportunity.md),
and [meaning](examples/meaning-of-life.md). These are illustrations, not evidence
that the skill has been benchmarked.

When editing this library, follow the
[extraction and evidence framework](references/extraction-framework.md).
Keep shared rules here and topic-specific content in the relevant reference.
Project authorship and Nuwa attribution are documented in [README.md](README.md).
