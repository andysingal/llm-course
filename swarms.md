```py
import os

from swarm_models import OpenAIChat

from swarms import Agent

company = "NVDA"

# Get the OpenAI API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Model
model = OpenAIChat(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=api_key,
    model_name="llama-3.1-70b-versatile",
    temperature=0.1,
)


# Initialize the Managing Director agent
managing_director = Agent(
    agent_name="Managing-Director",
    system_prompt=f"""
    As the Managing Director at Blackstone, your role is to oversee the entire investment analysis process for potential acquisitions. 
    Your responsibilities include:
    1. Setting the overall strategy and direction for the analysis
    2. Coordinating the efforts of the various team members and ensuring a comprehensive evaluation
    3. Reviewing the findings and recommendations from each team member
    4. Making the final decision on whether to proceed with the acquisition

    For the current potential acquisition of {company}, direct the tasks for the team to thoroughly analyze all aspects of the company, including its financials, industry position, technology, market potential, and regulatory compliance. Provide guidance and feedback as needed to ensure a rigorous and unbiased assessment.
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    streaming_on=True,
    verbose=True,
    stopping_token="<DONE>",
    state_save_file_type="json",
    saved_state_path="managing-director.json",
)
```

- [Interactive GroupChat](https://docs.swarms.world/en/latest/swarms/examples/igc_example/)
- [swarmclaw](https://github.com/swarmclawai/swarmclaw)

The self-hosted AI agent runtime and multi-agent framework for autonomous agents. Open-source agent swarms with durable agent memory, MCP tools, skills, delegation, schedules, and 23+ LLM providers — a practical Claude Code and LangChain alternative.


[A Swarm of Agents for Multi-Angle Analysis: Building a Team of Experts from LLMs](https://x.com/h100envy/status/2077371640690672001)

1. The Basic Client
Start with a simple client to the model. I use an OpenAI-compatible message format, it works with most providers and local Ollama.

```
import requests
import json
from concurrent.futures import ThreadPoolExecutor

API = "http://localhost:11434/api/chat"   # Ollama, or a provider endpoint
MODEL = "qwen2.5:32b"

def ask(system, user, temperature=0.7):
    resp = requests.post(API, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "stream": False,
    }, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"]
```

### The Orchestrator Assigns Roles
The orchestrator gets the task and decides which experts are needed. Do not hardcode roles in advance, let the model pick them for the specific task, this makes the swarm general. Ask for strict JSON to parse.

```
ORCHESTRATOR_SYSTEM = """You are the orchestrator of an analytical swarm.
For the task, define 3-5 expert roles that will give maximally DIFFERENT
and conflicting views on the decision. The roles must conflict in their
interests, not complement each other.

For each role give: name, focus (what it fixates on), bias (what it is
biased toward, what it tends to overrate).

Reply ONLY with a JSON array, no explanations:
[{"name": "...", "focus": "...", "bias": "..."}, ...]
"""

def plan_roles(task):
    raw = ask(ORCHESTRATOR_SYSTEM, f"Task to analyze:\n{task}",
              temperature=0.9)   # higher temperature for role diversity
    # cut out the JSON in case the model added text around it
    start, end = raw.find("["), raw.rfind("]") + 1
    return json.loads(raw[start:end])
```

### The Experts Analyze in Parallel and Independently
Each expert gets its role and the same decision. Critically: they run in parallel and do not see each other's conclusions. Parallelism here is not only for speed, it guarantees independence, an expert physically cannot adjust to another's opinion.

```
EXPERT_SYSTEM = """You are an expert with the role: {name}.
Your focus: {focus}.
Your bias: {bias}. Do not fight it, it is your value to the analysis.

Analyze the decision STRICTLY from your position. Do not be balanced,
do not try to account for other viewpoints, other experts will do that.
Your job is to push your angle to the limit.

Give:
- a verdict from your position (for / against / conditional)
- 2-3 main arguments from your angle specifically
- 1 risk that is most visible from your position and others will miss
Short and hard, no fluff."""

def run_expert(role, task):
    system = EXPERT_SYSTEM.format(**role)
    opinion = ask(system, f"Decision to analyze:\n{task}", temperature=0.7)
    return {"role": role["name"], "opinion": opinion}

def run_swarm(roles, task):
    # parallel launch: independence plus speed
    with ThreadPoolExecutor(max_workers=len(roles)) as pool:
        futures = [pool.submit(run_expert, role, task) for role in roles]
        return [f.result() for f in futures]
```

### The Merge Reconciles the Conclusions
Now we have several sharp, one-sided opinions. The merge collects them into one verdict, but not by averaging. It looks for where the experts agree (a strong signal), where they contradict (a risk zone requiring a decision), and what outweighs what.

```
MERGE_SYSTEM = """You are the synthesizer of an analytical swarm. You are
given the opinions of several experts with different biases on one decision.

Your job is NOT to average them. Your job is:
1. Agreement: what the experts agreed on despite different positions.
   This is the most reliable signal, highlight it.
2. Conflict: where the experts directly contradict. Do not smooth it over,
   name the conflict explicitly and say what each side costs.
3. Blind spots: a risk only one expert named, but it matters.
4. Final verdict across everything: for / against / conditional, and under
   what conditions it changes.

Write densely. Keep disagreement as information, do not hide it."""

def merge_opinions(task, opinions):
    block = "\n\n".join(
        f"### Expert: {o['role']}\n{o['opinion']}" for o in opinions
    )
    user = f"Decision:\n{task}\n\nExpert opinions:\n{block}"
    return ask(MERGE_SYSTEM, user, temperature=0.4)   # lower temperature for sober synthesis
```
### A Devil's Advocate Against Fake Agreement
There is a quiet danger: sometimes the experts agree not because the decision is good, but because everyone is looking the same way out of inertia. This is fake agreement, and it is more dangerous than open conflict, because it looks like confidence.
Against this we add one special agent, the devil's advocate. Its only job is to attack the consensus. It sees all the experts' opinions and is obligated to find why they might all be wrong at once. If the swarm unanimously voted "for," the advocate looks for a scenario where it is a catastrophe.

```
DEVIL_SYSTEM = """You are the devil's advocate in an analytical swarm. You
are given the experts' opinions. Your only job: attack their agreement.

If the experts converged on something, find why they might ALL be wrong AT
ONCE. Look for a shared blind spot: an assumption everyone accepted without
checking, a scenario no one considered because it is inconvenient.

Do not be polite. Your value is that you say what the group does not want
to hear. Give:
- which shared assumption of the experts is the most dangerous
- a scenario in which the swarm's unanimous opinion turns out fatally wrong
- one question the group carefully avoided
If there is no agreement and the experts genuinely disagree, say so plainly
and point to the sharpest unresolved conflict."""

def run_devil(task, opinions):
    block = "\n\n".join(
        f"### {o['role']}\n{o['opinion']}" for o in opinions
    )
    user = f"Decision:\n{task}\n\nSwarm opinions:\n{block}"
    return ask(DEVIL_SYSTEM, user, temperature=0.8)
```
#### Putting It All Together
```
def analyze(task, debate=True):
    print("Orchestrator is picking roles...")
    roles = plan_roles(task)
    for r in roles:
        print(f"  - {r['name']}: {r['focus']}")

    print(f"\nLaunching {len(roles)} experts in parallel...")
    opinions = run_swarm(roles, task)
    for o in opinions:
        print(f"\n[{o['role']}]\n{o['opinion']}")

    # optional debate round: experts react to each other
    if debate:
        print("\nDebate round, experts rebut each other...")
        opinions = debate_round(roles, task, opinions)

    # devil's advocate attacks the swarm's agreement
    print("\nDevil's advocate looks for a crack in the agreement...")
    devil = run_devil(task, opinions)
    print(f"\n[Devil's advocate]\n{devil}")

    # merge reconciles the conclusions plus the advocate's attack
    print("\nMerge is reconciling the conclusions...")
    opinions_plus = opinions + [{"role": "Devil's advocate", "opinion": devil}]
    verdict = merge_opinions(task, opinions_plus)
    print(f"\n=== FINAL VERDICT ===\n{verdict}")
    return verdict

if __name__ == "__main__":
    analyze(
        "We want to remove the free tier and make the product fully paid "
        "with a 14-day trial. Should we do it?"
    )
```
