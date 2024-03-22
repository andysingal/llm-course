from credentials import openai_api_key, model_name
from tools import ImageDescriberTool
import os
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent, create_structured_chat_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import YouTubeSearchTool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

tools = [YouTubeSearchTool(), ImageDescriberTool()]  #, ImageDescriberTool()

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


memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
    input_key="human_input"
)


llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=0,
    model_name=model_name
)

# Construct the OpenAI Tools agent
openai_agent = create_openai_tools_agent(llm, tools, prompt)

agent = AgentExecutor(agent=openai_agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True,
                                           max_iterations=2)

while True:
    promp = input("Ask questions: ")
    response = agent.invoke({"user_question": promp,
                                    "image_path": '',
                                    'human_input': ''})

    print("Response", response['output'])



