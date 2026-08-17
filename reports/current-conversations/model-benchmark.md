# Current Conversations model benchmark

Date: 2026-08-17  
Credential state: absent

The harness checks schema adherence and source-link retention using captured test
responses. It is not a live model comparison and does not establish latency, current
quality or actual cost.

- Captured cases: 1
- All captured outputs schema-valid: True
- Mocked Responses payloads parsed: 1
- Mocked source URLs retained: True
- Responses tool type: web_search
- Strict structured output enabled: True
- Live models tested: 0
- Selected model: operationally unverified
- Paid cost: CAD 0.00

A live benchmark must compare relevance, source-link retention, grouping, summary
fidelity, latency and estimated cost under the CAD 2 run ceiling. The lowest-cost model
that passes every schema and fidelity criterion should then be written to the repository
variable `CURRENT_CONVERSATIONS_OPENAI_MODEL`.
