[How to Build a Team of AI Agents That Work Together](https://x.com/eng_khairallah1/status/2045430911257432225)

- Every effective multi-agent system follows the same fundamental pattern: hub and spoke.
- The hub (coordinator agent) sits at the center. It receives the overall goal from the user. It decomposes the goal into subtasks. It decides which specialist agent handles each subtask. It passes context between specialists. It assembles the final output from all the pieces.
- The spokes (specialist agents) are focused experts. Each one has a defined role, a small set of tools optimized for that role, and a system prompt that constrains it to its specialty.
- All communication flows through the coordinator. Specialists never talk to each other directly. The coordinator is the single point of routing, quality control, and assembly.
This architecture has massive advantages. Each specialist stays focused - reducing errors from context overload. Specialists can be developed and tested independently. You can swap out or upgrade individual specialists without rebuilding the system. The coordinator provides a single point of observability for debugging and monitoring.


Most people assume that because the coordinator knows everything, the specialist must also know everything. It does not. If the coordinator gathered research data and wants the writing specialist to turn it into a report, the coordinator must include all the research data in the writing specialist's prompt. If it just says "write the report based on our research," the writing specialist has no idea what research was done.

```
# WRONG — specialist has no context
writer_prompt = "Write a market analysis report based on the research."

# RIGHT — all context passed explicitly
writer_prompt = f"""You are a professional report writer.

Write a market analysis report using the research findings below.

RESEARCH FINDINGS:
{research_data}

KEY STATISTICS:
{statistics}

COMPETITOR ANALYSIS:
{competitor_data}

FORMAT: Executive summary (3 sentences), then 5 sections with headers, 
each 2-3 paragraphs. Professional tone. Cite specific numbers from 
the research.

AUDIENCE: C-level executives who will read this in under 10 minutes.
"""
```

### Building Your First Multi-Agent Team: The Research and Report System

The team:
- Agent 1: Research Specialist - searches for information, extracts key facts, and compiles raw research data.
- Agent 2: Analyst Specialist - takes raw research data, identifies patterns, draws conclusions, and spots contradictions between sources.
- Agent 3: Writer Specialist - takes analyzed data and produces a polished, structured report in a defined format and voice.
- Agent 4: Reviewer Specialist - reads the finished report, checks for accuracy against the raw research, identifies weak claims, and suggests improvements.

##### Agent 0: Coordinator - manages the entire workflow.

The coordinator's workflow:

```
Step 1: Receive the research question from the user.
Step 2: Decompose the question into 3-5 sub-questions that together 
        fully cover the topic.
Step 3: Send each sub-question to the Research Specialist.
Step 4: Compile all research findings.
Step 5: Send compiled findings to the Analyst Specialist.
Step 6: Send analysis + research to the Writer Specialist.
Step 7: Send the draft report + original research to the 
        Reviewer Specialist.
Step 8: If the Reviewer flags issues: send the flagged sections 
        back to the Writer for revision.
Step 9: Deliver the final report to the user.
```

Each specialist has a focused system prompt:

Research Specialist:

```
You are a research specialist. Your only job is to find accurate, 
current information on the topic you are given.

For each piece of information:
- Note the source
- Rate your confidence (high/medium/low)
- Flag if the information might be outdated

Return your findings as a structured list of facts with sources 
and confidence ratings. Do not analyze. Do not write prose. 
Just find and organize facts.
```

Analyst Specialist:

```
You are a data analyst. Your only job is to analyze research 
findings and extract insights.

Given raw research data:
- Identify the 3-5 most important patterns
- Note contradictions between sources
- Flag claims that lack sufficient evidence
- Draw conclusions supported by the data

Do not write a final report. Return structured analysis that a 
writer can turn into polished prose.
```

Writer Specialist:

```
You are a professional report writer. Your only job is to turn 
analyzed data into a polished, readable report.

Given analysis and supporting data:
- Write in clear, professional prose
- Structure with an executive summary followed by detailed sections
- Cite specific numbers and sources throughout
- Make the report scannable — a reader should grasp key points 
  in under 3 minutes

Do not perform new research. Do not change the conclusions from 
the analysis. Only write.

```

Reviewer Specialist:

```
You are a quality reviewer. Your only job is to check the 
finished report against the original research.

Check for:
- Claims in the report not supported by the research data
- Important findings from the research that the report omits
- Logical inconsistencies or weak reasoning
- Accuracy of all numbers and statistics
- Clarity and readability issues

For each issue found: quote the problem, explain what is wrong, 
and suggest a specific fix. If the report is solid, say so.
```

##### Why this team produces better output than a single agent:

The research agent goes deep on finding information - it is not distracted by having to write a report at the same time. The analyst focuses purely on patterns - not on finding information or writing prose. The writer focuses purely on quality prose - not on doing research or analysis. The reviewer catches mistakes that the writer missed because reviewing is its entire job.


#### Designing Your Own Multi-Agent Teams

The research and report team is just one configuration. You can build multi-agent teams for any complex workflow.
- The Content Team:
Researcher → Outline Architect → Draft Writer → Editor → Formatter
Takes a topic and produces polished, multi-format content.
- The Customer Support Team:
Classifier → Knowledge Base Searcher → Response Drafter → Quality Checker
Handles support tickets with multiple verification layers.
- The Business Analysis Team:
Data Collector → Trend Analyzer → Risk Assessor → Recommendation Writer
Takes raw business data and produces actionable strategic recommendations.

The design principles are always the same:
Each agent has ONE clear responsibility. Each agent has a focused set of tools (3 to 5 maximum). All communication flows through the coordinator. Context is passed explicitly between agents - never assumed. The coordinator validates output at each stage before passing to the next agent.

