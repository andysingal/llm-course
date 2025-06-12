[ReasoningTools](https://github.com/agno-agi/agno/blob/main/cookbook/reasoning/tools/claude_reasoning_tools.py)

[ Langtrace with Agno](https://docs.langtrace.ai/supported-integrations/llm-frameworks/agno)

[memo-agno](https://github.com/mem0ai/mem0/blob/main/examples/misc/fitness_checker.py)

[sutra_with_agno_agent](https://github.com/sutra-dev/sutra-cookbook/blob/main/agents/sutra_with_agno_agent.ipynb)
SUTRA is a family of large multi-lingual language (LMLMs) models pioneered by Two Platforms. SUTRA’s dual-transformer approach extends the power of both MoE and Dense AI language model architectures, delivering cost-efficient multilingual capabilities for over 50+ languages


- Initialize using session_state
- Modify using tools
- Reference in instructions

```py
from textwrap import dedent
from typing import Dict, List, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from pydantic import BaseModel, Field
from rich.pretty import pprint


class ContentSection(BaseModel):
    """Represents a section of content from the webpage."""

    heading: Optional[str] = Field(None, description="Section heading")
    content: str = Field(..., description="Section content text")


class PageInformation(BaseModel):
    """Structured representation of a webpage."""

    url: str = Field(..., description="URL of the page")
    title: str = Field(..., description="Title of the page")
    description: Optional[str] = Field(
        None, description="Meta description or summary of the page"
    )
    features: Optional[List[str]] = Field(None, description="Key feature list")
    content_sections: Optional[List[ContentSection]] = Field(
        None, description="Main content sections of the page"
    )
    links: Optional[Dict[str, str]] = Field(
        None, description="Important links found on the page with description"
    )
    contact_info: Optional[Dict[str, str]] = Field(
        None, description="Contact information if available"
    )
    metadata: Optional[Dict[str, str]] = Field(
        None, description="Important metadata from the page"
    )


agent = Agent(
    model=OpenAIChat(id="gpt-4.1"),
    tools=[FirecrawlTools(scrape=True, crawl=True)],
    instructions=dedent("""
        You are an expert web researcher and content extractor. Extract comprehensive, structured information
        from the provided webpage. Focus on:

        1. Accurately capturing the page title, description, and key features
        2. Identifying and extracting main content sections with their headings
        3. Finding important links to related pages or resources
        4. Locating contact information if available
        5. Extracting relevant metadata that provides context about the site

        Be thorough but concise. If the page has extensive content, prioritize the most important information.
    """).strip(),
    response_model=PageInformation,
)

result = agent.run("Extract all information from https://www.agno.com")
pprint(result.content)
```

[Define tools to manage our shopping list](https://github.com/agno-agi/agno/blob/main/cookbook/agent_concepts/state/session_state.py)

[zep_integration](https://github.com/agno-agi/agno/blob/main/cookbook/agent_concepts/memory/integrations/zep_integration.py)

<img width="399" alt="Screenshot 2025-04-23 at 1 56 06 PM" src="https://github.com/user-attachments/assets/534abd44-aab4-46b2-86b8-bf3b8b6b70c4" />

<img width="729" alt="Screenshot 2025-05-11 at 9 57 28 PM" src="https://github.com/user-attachments/assets/3e4955e4-e474-4989-bde7-504ad56047a4" />




## ARTICLE

[Building a MCP-Powered Task Manager Agent with Agno and Supabase: A Step-by-Step Guide](https://codingthesmartway.com/building-a-mcp-powered-task-manager-agent-with-agno-and-supabase-a-step-by-step-guide/)

[Building a Research Agent using Agno](https://github.com/rajshah4/LLM-Evaluation/blob/main/ResearchAgent_Agno_LangFuse.ipynb)

## projects

[GenAI_AgenticRAG_PDF_WebSearch](https://github.com/simranjeet97/AgenticAI_AIAgents_Course/blob/main/GenAI_AgenticRAG_PDF_WebSearch/agentic_rag.py)



