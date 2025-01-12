[Langchain-AgentExecutor-Memory](https://qiita.com/R61/questions/9e738d57c080262e7af6)

[Ai-Agents](https://github.com/NisaarAgharia/AI-Agents)

```py
import boto3
import json
import os
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain.agents import AgentExecutor

# AWS クライアントの設定
session = boto3.Session(region_name='ap-northeast-1')
secrets_client = session.client('secretsmanager')
bedrock_client = session.client(
    service_name='bedrock-runtime',
    region_name='ap-northeast-1',
    endpoint_url='https://bedrock-runtime.ap-northeast-1.amazonaws.com'
)

# LangChain API キーの取得
def get_langchain_api_key(secret_name):
    response = secrets_client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict['LANGCHAIN_API_KEY']

api_key = get_langchain_api_key('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_API_KEY"] = api_key

# セッション ID の設定
session_id = 'unique_session_id_20240827'

# DynamoDB テーブルの設定
table_name = 'ChatHistoryTable'
history = DynamoDBChatMessageHistory(table_name="chat-history-dynamodb",
        session_id=session_id,)

# Bedrock のモデル設定
chat_model = ChatBedrock(model_id='anthropic.claude-3-5-sonnet-20240620-v1:0', client=bedrock_client)

# 必要な変数を含むプロンプトテンプレートの設定
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template=(
        "You are a helpful assistant. Use the following tools to answer the user's questions:\n"
        "{tools}\n"
        "Tool names available: {tool_names}\n"
        "Keep track of your conversation using this scratchpad: {agent_scratchpad}\n"
        "User input: {input}\n"
        "Your response should be in the form of 'Action: <action>', followed by 'Action Input: <input>', "
        "and finally 'Response: <response>'.\n"
        "For example, if using a tool, say 'Action: use_tool' followed by 'Action Input: tool_name'."
    )
)

# メモリ設定
memory = ConversationBufferMemory(chat_memory=history)

# ツールのロード
tools = load_tools(["ddg-search", "wikipedia"], llm=chat_model)

# エージェントの初期化
agent = create_react_agent(
    llm=chat_model,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# エージェントを実行する関数
def send_message(user_message):
    # メモリにユーザーの入力を追加
    memory.save_context({"input": user_message}, {"output": ""})

    # エージェントの応答を取得
    try:
        # 必要な引数を辞書形式で渡す
        response = agent_executor.invoke({
            "input": user_message,
            "tools": tools,
            "tool_names": [tool.name for tool in tools],
            "agent_scratchpad": memory.load_memory_variables({}).get("agent_scratchpad", ""),
            "chat_history": memory.load_memory_variables({}).get("chat_history", "")
        })
        
        # 応答が AgentAction オブジェクトの場合、その属性を使って応答を処理
        if hasattr(response, 'output'):
            output_text = response.output
        else:
            output_text = str(response)
        
        # 会話履歴にエージェントの応答を追加
        memory.save_context({"input": user_message}, {"output": output_text})
        
        return output_text

    except OutputParserException as e:
        # パースエラーをハンドル
        print(f"Output parsing error: {e}")
    except AttributeError:
        # invoke メソッドがない場合はエラーハンドリング
        print("Error: The agent object is not callable. Check the agent creation method.")
    except Exception as e:
        # その他のエラーをハンドル
        print(f"An unexpected error occurred: {e}")

    return None

# サンプルの対話
user_message = '私の名前を覚えていますか？'
# user_message = 'こんにちは、私の名前は'
response = send_message(user_message)
if response:
    print(response)
else:
    print("Failed to get a response from the agent.")

```
