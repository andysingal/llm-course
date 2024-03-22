from credentials import openai_api_key, model_name
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import YouTubeSearchTool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from tools import ImageDescriberTool


#tools 
tools = [YouTubeSearchTool(), ImageDescriberTool()]

#memory
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=1,
    return_messages=True,
    input_key="human_input"
)

prompt = PromptTemplate(
    input_variables=[
        "user_question",
        "image_path",
        "chat_history",
        "human_input",
        "agent_scratchpad"

    ],
    template=(
        '''
        Previous conversation:
        {chat_history}

        Begin!

        User Question: {user_question}
        Image Path: {image_path}
        Thought: {agent_scratchpad}
        Human Input: {human_input}
        '''
    )
)

#initialize llm
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=0,
    model_name=model_name
)

#create the agent
openai_agent = create_openai_tools_agent(llm, tools, prompt)
agent = AgentExecutor(agent=openai_agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True,
                                           max_iterations=2)
