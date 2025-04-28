[agent_dev_kit](https://github.com/rajib76/agent_dev_kit/blob/main/looping_agent/agent.py)

```py
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
model = "openai/gpt-4o"
model_abstraction = LiteLlm(model=model)

research_agent = LlmAgent(
    name="research_agent",
    instruction="You will research on a provided topic and share the output of research",
    model=model_abstraction,
    output_key="research_content"
)

reviewer_agent = LlmAgent(
    name="reviewer_agent",
    instruction="""You are an expert reviewer.
    You will review the below provided content and make changes to make 
    the content more engaging and impactful

    **Content to review**
    {research_content}

    """,
    model=model_abstraction,
    output_key="reviewed_content"
)

review_loop = LoopAgent(
    name="ReviewLoop",
    sub_agents=[
        research_agent,
        reviewer_agent,
    ],
    max_iterations=3  # Limit loops
)

linkedin_poster = LlmAgent(
    name="linkedin_agent",
    instruction="""You are an expert writer of articles in LinkedIn.
    You will be provided with a research content. You will need to create 
    an impactful title for the content. You will also format the content 
    aligning it to LinkedIn article format. The final title and content output 
    muat be ready to be posted in LinkedIn 

    **Content to review**
    {reviewed_content}

    """,
    model=model_abstraction,
    output_key="linkedin_content"
)

research_pipeline_agent = SequentialAgent(
    name="LinkedInPostPipelineAgent",
    sub_agents=[review_loop, linkedin_poster],
    description="Executes a sequence of research and research review activity.",
    # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
)

root_agent = research_pipeline_agent
```
