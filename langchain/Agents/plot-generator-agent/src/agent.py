import logging
from typing import List

from dotenv import find_dotenv, load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent

from src.tools import get_tools, Tool
from src.models import get_chat_model

# Load the environment variables from my .env file
load_dotenv(find_dotenv())

# Set up logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def get_react_agent_executor(
    llm: BaseChatModel,
    tools: List[Tool],
    model_provider: str) -> AgentExecutor:
    """
    Returns an agent executor that can execute a multi-hop react agent.
    If the model_provider is 'cohere', the agent will be created using the Cohere API.

    Args:
        llm (BaseChatModel): The chat-based LLM model to use.
        tools (List[Tool]): A list of tools that can be used by the agent.
        model_provider (str): The provider of the chat-based LLM model.

    Returns:
        AgentExecutor: An agent executor that can execute a multi-hop react agent.
    """
    if model_provider == 'cohere':
        prompt = ChatPromptTemplate.from_template("{input}")
        agent = create_cohere_react_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )
    else:
        prompt = hub.pull('hwchase17/react')
        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    
    )
    return agent_executor


def run(
    model_provider: str,
    model_name: str,
    input: str
):
    """
    Creates an agent executor that can execute a multi-hop react agent, using the
    specified model, and runs the agent with the given input.

    Args:
        model_name (str): The name of the chat-based LLM model to use.
        input (str): The input to the agent.
    """
    llm = get_chat_model(model_provider, model_name)
    tools = get_tools()

    agent_executor = get_react_agent_executor(llm, tools, model_provider)

    # breakpoint()

    agent_executor.invoke(
        {
            'input': input,
        }
    )


if __name__ == '__main__':
    from fire import Fire
    Fire(run)