# Extraction and Evidence Framework

Use this file when maintaining the library. The product is a topic skill: its
purpose is to improve reasoning, not to imitate a particular person's voice.

## From Source to Reusable Method

For a proposed model or heuristic, record:

1. The problem it addresses and the mechanism it claims explains the result.
2. A specific supporting passage, with author or publisher, work, location,
   source URL, and capture date where available.
3. What is the source's claim and what is the maintainer's interpretation.
4. A concrete application and a counterexample or condition under which the
   method stops being useful.
5. What decision, observation, or experiment changes when the method is applied.

Repeated use across domains can support transferability, but does not prove a
universal rule. A plausible idea with thin evidence can remain an explicitly
labeled heuristic; do not invent citations to promote it to a proven model.

## Evidence Types

| Material | Appropriate use | Limit |
|---|---|---|
| Original text or transcript | Support a claim actually present in the passage | Context, translation, and date still matter |
| Institutional or third-party explanation | Explain how that publisher describes a theory | Do not attribute its wording directly to the original thinker |
| Catalog or index | Locate a work and establish bibliographic metadata | Does not count as captured substantive evidence |
| Editorial synthesis | Connect ideas and propose applications | Label the interpretation and its unverified parts |
| Illustrative example | Demonstrate a reasoning procedure | Invented inputs and thresholds must be explicit |

Prefer primary materials for attributed claims. Use secondary explanations when
appropriate and identify them as such. If publication date or authorship is
unknown, write "Unknown" rather than using the card creation date or a label
such as "public concept card" as the author.

## Capture Integrity

- Keep source language, publisher, work, and capture date traceable.
- Label catalog/index captures accurately. A successful HTTP response is not
  evidence that the requested book or lecture was captured.
- Mark omissions and truncation. Do not label a truncated excerpt as full text.
- Remove navigation controls and failed dynamic counters from evidence, and
  record meaningful cleaning decisions in an editorial note.
- Preserve source rights notices. A publicly accessible page is not necessarily
  licensed under this repository's MIT license.
- Keep one canonical capture per source URL; link multiple research topics to
  it rather than duplicating a passage to increase file counts.

## Handling Gaps and Disagreement

Missing evidence should result in a narrower claim, an explicit uncertainty, or
a useful next lookup. A bibliography of famous names is not a substitute for a
passage that supports the argument.

When sources disagree, state whether the difference concerns facts, definitions,
values, dates, or scope. Preserve the disagreement rather than manufacturing a
consensus. Present-day costs, capabilities, and rules require present-day checks;
an archived page only supports what the publisher said at the time captured.

## Review Before Publishing

- Does each attributed claim have a relevant source and location?
- Are editorial deductions distinguishable from source statements?
- Do examples state their assumptions, limits, and a decision-relevant outcome?
- Are user preferences and task scope preserved by the workflow?
- Does each reference add information instead of repeating shared instructions?
- Do link, source-inventory, and repetition checks pass, and have their limits
  been acknowledged? Passing a structural check does not verify factual truth.

Use the maintenance commands in [README.md](../README.md). For substantial
instruction changes, also try representative user requests and inspect whether
the resulting answer follows the intended route without inventing evidence.
