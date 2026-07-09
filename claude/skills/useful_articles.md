[Do LLM-Generated Skills Make Better AI Data Scientists? A Component Ablation Across Data-Science Workflows](https://arxiv.org/pdf/2607.07504)

This yields four
skill conditions plus a No-Skill baseline:
- (1) No-Skill: task prompt only
- (2) Core-Only: Routing + Core Procedure
- (3) Core+Examples: Routing + Core Procedure + Worked Ex
amples
- (4) Core+Refs: Routing + Core Procedure + Reference Notes
- (5) Full: all four sections

Each skill contains four sections:
- • Routing (∼50 tokens): activation triggers specifying when to
apply the skill
- • CoreProcedure (∼190 tokens): step-by-step workflow instruc
tions
- • Worked Examples (∼225 tokens): concrete input→output
demonstrations
- • Reference Notes (∼225 tokens): supplementary heuristics and
conventions
