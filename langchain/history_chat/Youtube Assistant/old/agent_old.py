from credentials import openai_api_key, model_name
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import YouTubeSearchTool
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from tools import ImageDescriberTool


#tools 
tools = [ImageDescriberTool(), YouTubeSearchTool()]

#memory
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
    input_key="human_input"
)

#prompt
# template = '''Answer the following questions as best you can. You have access to the following tools:
        # {tools}
    
        # Previous conversation:
        # {chat_history}

        # Use the following format:

        # User Question: the input question you must answer
        # Image Path: the path to the image you need to describe based on User Question (can be optional)
        # Action: the action to take, should be one of [{tool_names}]
        # Final Answer: the final answer to the original input question

        # Begin!

        # User Question: {user_question}
        # Image Path: {image_path}
        # Thought:{agent_scratchpad}
        # Human Input: {human_input}
        # '''
        


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
        Thought:{agent_scratchpad}
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
openai_agent = create_openai_functions_agent(llm, tools, prompt)
agent = AgentExecutor.from_agent_and_tools(agent=openai_agent, tools=tools, memory=memory, verbose=True, handle_parsing_errors=True,
                                           max_iterations=2)
agent.invoke(
    {
        "user_question": "Hello?",
        'image_path': '',
        'human_input':'',
        "chat_history": [
            HumanMessage(content="Hi! how are you?"),
            AIMessage(content="Hello! I am fine today. Thank you for asking."),
        ],
    }
)
