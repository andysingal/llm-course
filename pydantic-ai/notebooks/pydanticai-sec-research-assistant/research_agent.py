from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from tavily import TavilyClient
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

@dataclass
class SearchDataclass:
    max_results: int
    todays_date: str

@dataclass
class SearchDependencies:
    todays_date: str

class ResearchOutput(BaseModel):
    title: str = Field(description="Title of the research article. This will be markdown heading 2")
    description: str = Field(description="Description of the research article. This will be markdown paragraph")
    links: List[str] = Field(description="List of links that are sources for the research article. This will be markdown bullet points")

class AllResearchOutputs(BaseModel):
    research_outputs: List[ResearchOutput]


research_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=SearchDependencies,
    result_type=AllResearchOutputs,
    system_prompt = (
        "You are an expert security research assistant"
        "You are tasked with identifying all the major application security news for the previous week."
        "You need to collate that news and come up with a research report with multiple articles."
        "Each article should have a title, description and links to the sources."
        "Each article must be news and not generic information about Application Security"
        "You need to write a maximum of 5 articles"
    )
)

@research_agent.tool
def search_in_tavily(search_data: RunContext[SearchDataclass], query: str, query_number: int) -> dict[str, Any]:
    """
    This tool searches for the latest Application security using the Tavily API. 
    This needs to be provided with a query and a max_results parameter.
    """
    search_client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    max_results = search_data.deps.max_results
    results = search_client.get_search_context(query=query, max_results=max_results)

    return results

@research_agent.tool
def write_to_md_file(ctx: RunContext[SearchDependencies], research_report: AllResearchOutputs) -> dict[str, Any]:
    """
    This tool writes the research outputs to a markdown file.
    """
    todays_date = ctx.deps.todays_date
    file_name = f"research_report_{todays_date}.md"
    with open(file_name, "w") as f:
        for research_output in research_report.research_outputs:
            f.write(f"## {research_output.title}\n")
            f.write(f"{research_output.description}\n")
            f.write("### Links\n")
            for link in research_output.links:
                f.write(f"* {link}\n")
            f.write("\n")

    return {"file_name": file_name}


if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    search_deps = SearchDataclass(max_results=5, todays_date=current_date)
    result = research_agent.run_sync(
        "get me the latest application security news from all over the world",
        deps=search_deps
    )
    # print(result)