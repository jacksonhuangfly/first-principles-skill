# Example: Product Cost Breakdown

## User Prompt

Our product charges $49 per month, but margins keep shrinking. Use first
principles to analyze it.

## Worked Response With Hypothetical Inputs

The price alone does not identify the problem. Ask for costs and usage by
customer cohort, then separate delivery costs from acquisition and fixed
company expenses. The numbers below are invented to illustrate the calculation;
they are not estimates for the user's business.

### Define the Unit

Use one paying customer per month. Suppose the monthly delivery costs are:

| Item | Hypothetical cost |
|---|---:|
| Model/API computation | $18 |
| Support delivery | $9 |
| Hosting and storage | $3 |
| Payment fees | $2 |
| Onboarding delivery allocated over the expected paid lifetime | $4 |
| Total | $36 |

At $49 revenue, this leaves $13 per customer, or about 26.5%, before acquisition,
fixed payroll, taxes, and other excluded costs. This is a contribution estimate,
not a claim about accounting profit. State and test the paid-lifetime assumption
behind the onboarding allocation separately.

### Find the Decision-Bearing Assumption

Computation is the largest listed cost, but that does not prove it is waste.
Break it into cost per successful task, task frequency, retries, and idle work.
An initial hypothesis might be: some scheduled reports do not need real-time
model calls. Check actual report deadlines and customer expectations first.

Distinguish requirements from design choices:

- A promised delivery deadline is a constraint to preserve or explicitly renegotiate.
- Generating every intermediate result immediately may be a design choice.
- High support cost may reflect onboarding failures rather than excessive staffing.

### Compare the Smallest Useful Change

Test batching only for eligible reports, keeping the output and promised
completion deadline. Keep a real-time fallback for failures or urgent requests.
If measured compute cost fell from $18 to $11 with other costs unchanged, the
contribution would rise from $13 to $20, about 40.8% of revenue. That is a
conditional scenario, not a predicted saving.

### Propose a Test and a Decision Rule

Agree on these illustrative limits before starting; the user has requested
analysis, not authorized a production change.

- **Comparison:** randomly assign eligible customers to batching or the existing
  path, using customer-level metrics to avoid treating repeated tasks as
  independent customers.
- **Cost metric:** mean compute cost per successfully completed report, with a
  target reduction of at least 20%.
- **Outcome guardrail:** suppose measured completion is 90%; choose a maximum
  tolerated decline of 2 percentage points. Require the 95% confidence interval
  for the treatment-minus-control difference to stay above -2 percentage points.
- **Window and sample:** collect at least 14 days of task outcomes and plan the
  required sample size for the chosen tolerance before recruitment. If traffic
  cannot support that sample, use a feasibility pilot and label the inference
  limited. Check 30-day retention after it becomes observable.
- **Operational guardrails:** stop on a critical reliability incident, preserve
  agreed delivery deadlines, and investigate support contacts above a
  pre-agreed per-customer limit.
- **Decision:** continue only if cost and outcome criteria pass and guardrails
  hold; roll back on harm. An interval crossing the tolerance, insufficient
  traffic, or immature retention data means the result is inconclusive.

Before running this test, the next minimum action is to inspect a recent sample
of report usage and compute invoices. If almost every report needs real-time
completion, reject the batching hypothesis and investigate retries or support
causes instead.
