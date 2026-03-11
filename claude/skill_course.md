[I want to learn how to use Claude Skills](https://x.com/hooeem/status/2031755971265974632)

```
I want you to help me identify whether I need a Claude Skill.

Here's how this works:

1. Ask me to describe the 3-5 tasks I repeat most often when
   using AI assistants. For each one, ask me:
   - What instructions do I typically give at the start?
   - How often do I repeat this task per week?
   - Does the output need to follow a specific format, tone,
     or structure every time?

2. After I describe each task, score it on a "Skill Readiness"
   scale of 1-10 based on:
   - Repetition frequency (higher = more ready)
   - Instruction complexity (more specific instructions =
     more ready)
   - Output consistency requirements (stricter format needs =
     more ready)

3. Rank my tasks from highest to lowest Skill Readiness score.

4. For my top-scoring task, tell me:
   - Why this is the best candidate for my first Skill
   - What the Skill would need to contain
   - An estimate of time saved per week if I automate it
   - Whether this is better suited for Claude Code or
     Claude Desktop (CoWork)

Start by asking me about my first repeated task.
```

#####PROMPT: THE SKILL INSTRUCTION ARCHITECT:

```
You are a Claude Skill instruction writer. Your job is to 
generate the complete instruction body for a SKILL.md file 
that is clear, sequential, and under 500 lines.

Here is my Skill definition:
[PASTE YOUR SKILL DEFINITION BRIEF FROM STEP 1]

Here is the YAML frontmatter already written:
[PASTE YOUR YAML BLOCK FROM STEP 2]

Now generate the full instruction body that goes BELOW the 
closing --- of the YAML block. Follow these rules precisely:

STRUCTURE RULES:
1. Start with a one-paragraph "Overview" that states what 
   this skill does and when it activates, written for Claude 
   (not for a human reader).
2. Break the workflow into numbered steps under a 
   "## Workflow" heading. Each step must be:
   - One clear action
   - Written as an imperative command ("Read the file..." 
     not "The file should be read...")
   - Specific enough that there is only ONE way to 
     interpret it
3. Include a "## Output Format" section that specifies 
   exactly how the final output should be structured 
   (file type, formatting, sections, tone, etc.)
4. Include a "## Edge Cases" section that tells Claude 
   how to handle:
   - Missing or incomplete input
   - Ambiguous requests
   - Conflicting instructions
   - Unexpected file formats or data types

EXAMPLE RULES:
5. Include at least 2 concrete examples under a 
   "## Examples" heading:
   - Example 1: A straightforward "happy path" showing 
     normal input → expected output
   - Example 2: An edge case showing unusual input → 
     how Claude should handle it
   Each example must show ACTUAL input and ACTUAL expected 
   output, not abstract descriptions.

QUALITY RULES:
6. Total length: aim for 100-300 lines. Cut anything 
   that doesn't directly instruct Claude on how to 
   execute the task.
7. Never use vague language like "handle appropriately" 
   or "format nicely." Every instruction must be specific 
   and testable.
8. If the skill requires referencing external files 
   (brand guides, templates), add a "## References" 
   section with the instruction: "Read [filename] from 
   the references/ directory before beginning the task."

Output the complete instruction body as markdown, ready to 
paste directly below the YAML frontmatter in a SKILL.md file.

After the instructions, provide a "Quality Checklist" that 
confirms:
- [ ] Every step is a single, unambiguous action
- [ ] At least 2 concrete examples included
- [ ] Edge cases are covered
- [ ] Output format is explicitly defined
- [ ] Total length is under 500 lines
- [ ] No vague or interpretable language remains

```

```
your-skill-name/
├── SKILL.md          (YAML header + instructions from Steps 2-3)
└── references/       (optional, from Step 4)
    └── your-ref.md
```

But wait. Before you deploy, you want to make sure the whole thing is airtight. This prompt does a final quality assurance pass on your complete SKILL.md file:

### PROMPT: THE SKILL QA AUDITOR

```
You are a Claude Skill Quality Assurance Auditor. I have 
built a complete SKILL.md file and I need you to audit it 
before I deploy it.

Here is my complete SKILL.md file:
[PASTE YOUR ENTIRE SKILL.MD FILE HERE]

Run the following audit checks and report results:

## 1. YAML FRONTMATTER AUDIT
- [ ] name field exists and is valid kebab-case
- [ ] description field exists and is over 50 words
- [ ] description is written in third person
- [ ] At least 5 trigger phrases are listed
- [ ] Negative boundaries are defined (when NOT to activate)
- [ ] Description is "pushy" enough (would Claude actually 
      fire this skill on a relevant request?)
SCORE: X/10

## 2. INSTRUCTION CLARITY AUDIT
- [ ] Every step is a single, unambiguous action
- [ ] No vague language ("handle appropriately", 
      "format nicely", "as needed")
- [ ] Instructions are in imperative voice ("Read the 
      file" not "The file should be read")
- [ ] Sequential logic is correct (no step depends on 
      information from a later step)
- [ ] Total instruction length is under 500 lines
SCORE: X/10

## 3. EXAMPLE QUALITY AUDIT
- [ ] At least 2 examples are included
- [ ] Examples show ACTUAL input and ACTUAL output 
      (not abstract descriptions)
- [ ] At least one edge case example is included
- [ ] Examples are realistic (represent real-world usage)
SCORE: X/10

## 4. EDGE CASE COVERAGE AUDIT
- [ ] Missing/incomplete input is handled
- [ ] Ambiguous requests are handled
- [ ] Unexpected file types or data formats are handled
- [ ] The skill knows when to ask for clarification 
      vs. make a reasonable assumption
SCORE: X/10

## 5. REFERENCE FILE AUDIT (if applicable)
- [ ] All referenced files are at one level deep only
- [ ] No circular references
- [ ] Reference instructions in SKILL.md are clear 
      ("Read X before beginning")
SCORE: X/10

## OVERALL DEPLOYMENT READINESS: X/50

If any section scores below 7/10, provide SPECIFIC 
rewrites for the failing sections. Output the corrected 
text ready to paste directly into the file.

If overall score is 40+/50, confirm: "READY TO DEPLOY."
If below 40, list the critical fixes needed before 
deployment, in priority order.
```

