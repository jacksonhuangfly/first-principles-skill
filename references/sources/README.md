# Source Library

This directory preserves captured source text and discovery records. Research notes link only to the records relevant to their claims. A file's presence or successful schema check does not verify the accuracy of a claim.

## Records And Evidence Status

| Record | What is retained | Use and limitation |
| --- | --- | --- |
| [Aristotle, Metaphysics](books/aristotle-first-causes-source-card.md) | Truncated translation excerpt from Book I | Causes and principles in retained passages; not the complete work |
| [Sunzi, The Art of War](books/sunzi-art-of-war-source-card.md) | Opening chapters of the Giles translation, cut off in Chapter III | Conditions, comparative assessment, and campaign costs |
| [Newton, Opticks catalog](books/newton-opticks-source-card.md) | Gutenberg catalog entry and site-generated summary | Discovery only; no book text retained |
| [Leonardo notebooks catalog](books/leonardo-notebooks-source-card.md) | Gutenberg catalog entry and site-generated summary | Discovery only; no notebook text retained |
| [Feynman, Cargo Cult Science](transcripts/feynman-cargo-cult.md) | Speech transcript | Scientific integrity and anti-self-deception |
| [Feynman Lectures index](transcripts/feynman-lectures-source-card.md) | Website landing page | Discovery only; no lecture chapter retained |
| [Deming Institute, Fourteen Points](articles/deming-quality-source-card.md) | Institutional reproduction of the points | Quality and system responsibility; not a full statistical treatment |
| [Theory of Constraints explainer](articles/goldratt-bottleneck-source-card.md) | Truncated third-party article | Secondary background; not Goldratt's original text |
| [Christensen Institute, Jobs to Be Done](articles/jtbd-source-card.md) | Institutional explainer and reported cases | Demand and customer progress; case outcomes are not independently verified |
| [Meadows, Leverage Points](articles/meadows-systems-source-card.md) | Introduction, ranked list, and partial discussion | Omitted sections' headings do not establish their arguments |
| [SpaceX Mars snapshot](articles/musk-mars-first-principles-source-card.md) | Historical organization page | Stated plans and architecture; not current specifications or independent feasibility evidence |

## Provenance Rules

- Prefer the relevant original text or a clearly attributed institutional reproduction. Label secondary explanations, translations, catalogs, and indexes honestly.
- `author` and `date` describe the retained page or text; work authorship and work dates may be recorded separately for a catalog. Use `Unknown` when the stored material does not establish a value.
- `captured_at` records the existing snapshot date. It is not a publication date or a claim that the source has been checked recently. Stored HTTP and content-type fields describe that original capture.
- Retained source passages remain in their original language. English notes explain selection, evidence limits, cleaning, and truncation; they are editorial content, not quotations from the source.
- `language` records the source text's actual language, not the desired response language. Source capture requires an explicit language tag (such as `en` or `zh-CN`, or `und` when undetermined) and does not translate the text.
- Only retained substantive passages support claims. Catalog descriptions, automatically generated summaries, navigation, and headings of omitted sections cannot replace those passages.
- Distinct files do not imply independent evidence. Keep one canonical record for each captured source URL. Use an edition-specific URL when referring to a different edition.

The [research index](../research/README.md) explains which topics have partial source support and which remain editorial synthesis requiring further verification.
