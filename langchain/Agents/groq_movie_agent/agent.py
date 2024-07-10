import os
from omdb_tools import *
from dotenv import load_dotenv
##to load credentials
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") ## Put your Langsmith API key here
# os.environ["LANGCHAIN_HUB_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") ## Put your Langsmith API key here
# os.environ["LANGCHAIN_TRACING_V2"] = 'true' ## Set this as True
# os.environ["LANGCHAIN_ENDPOINT"] = 'https://api.smith.langchain.com/' ## Set this as: https://api.smith.langchain.com/
# os.environ["LANGCHAIN_HUB_API_URL"] = 'https://api.hub.langchain.com' ## Set this as : https://api.hub.langchain.com
# os.environ["LANGCHAIN_PROJECT"] = 'llm-agents'


### Define your tools
movie_info_tool = OmdbAPI.get_movie_info_by_title
search_movie_tool = OmdbAPI.search_movie
search_series_tool = OmdbAPI.search_series

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

### Langchain imports
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage


### Build the chatbot class
class Chatbot:
    def __init__(self, model='llama3-70b-8192', temperature=0.3, memory=None):
        self.llm =  ChatGroq(model_name=model, temperature=temperature)
        self.system_prompt = ''''You are a helpful assistant who helps users get information
        about movies and TV series. You can use a few different tools you have access to:

        1. movie_info_tool - The input to this tool is movie title and optionally year. The
        tool returns a brief plot, tomato meter rating and other information for the movie that matches the title

        2. search_movie_tool - Use this tool to search for all movies matching a search string. Just put in the name of movie to search. Don't include "movies" in the search string.

        3. search_series_tool - Use this tool to search for all TV series matching a search string. Just put in the name of series to search. Don't include "series" in the search string.

        4. wikipedia - Generic tool to search for anything in the vast wikipedia corpus. Use this to
        search and return information on any movie/TV series related question

        You can use these tools in conjunction. For example if the user wants information of the 
        earliest Harry Potter movie, then use the search_movie_tool to get information of all Harry 
        Potter movies and then use the movie_info_tool to get details of the first movie by
        searching based on its title.
        Important: Where possible use the tool instead of your memory. The tool outputs are more accurate.
        However, if the tools don't give the information you need, proceed with your own memory

        Your job is to be a conversational Movie Asssistant who keeps conversation going. You are witty and smart
        and answer user's questions, plus ask your own to keep it lively.
        If the user conversation is not related to any of the tools you have then answer to the best of your knowledge
        For a generic question, not related to movies/TV series feel free to use the wikipedia tool

        When responding back to the user, don't mention your tools and their outputs. That is for your internal use

        Look at the user message below including the message history chain.
        '''
        self.memory = memory if memory else ChatMessageHistory(session_id="test-session")
        self.tools = [movie_info_tool, search_movie_tool, search_series_tool, wikipedia]
    
    def run(self, input):
        assistant_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
            content=self.system_prompt
        ),
          MessagesPlaceholder(variable_name="chat_history"),   
          MessagesPlaceholder(variable_name="agent_scratchpad"),

         ("user", "{input}"),            
        ] )

        # Create the agent and its executor
        assistant_agent = create_openai_tools_agent(self.llm, self.tools, assistant_prompt)
        agent_executor = AgentExecutor(agent=assistant_agent, tools=self.tools, verbose=True)

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        result = agent_with_chat_history.invoke({'input': input,}, config={"configurable": {"session_id": "1234"}})
        return result['output']