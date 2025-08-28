[StrandsAgents + Claude](https://acro-engineer.hatenablog.com/entry/2025/08/28/120000)

```py
import asyncio
import os
from textwrap import dedent

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools.mcp import MCPClient

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

websearch = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command='npx',
            args=['-y', 'tavily-mcp@latest'],
            env={'TAVILY_API_KEY': TAVILY_API_KEY},
        )
    )
)

class DeepResearch:
    PROMPT = dedent("""\
    ユーザーから伝えられた調査したいトピックに対して、PDF換算で3枚分の詳細かつ広範なレポートを作成してください。
    レポートはMarkdown形式でフォーマットしてください。
    必ず日本語でレポートを書いてください

    レポートする内容はWeb検索を用いて収集してください。
    収集した内容をよく吟味し、さらに徹底的な調査が必要だと判断した内容は、検索文言を書き換えてさらにWeb検索を行ってください。
    ユーザーが指示したトピックについて包括的な情報を収集することが重要です。

    参照したサイト脚注で示し、脚注には `[脚注番号][タイトル](URL)` 形式で列挙してください。
    """)

    def __init__(self, tools):
        model = BedrockModel(
            model='us.anthropic.claude-sonnet-4-20250514-v1:0',
            streaming=True,
            additional_request_fields={
                'thinking': {'type': 'enabled', 'budget_tokens': 4000},
                'anthropic_beta': ['interleaved-thinking-2025-05-14'],
            },
        )
        self.agent = Agent(
            model=model,
            system_prompt=self.PROMPT,
            tools=tools,
        )

    async def stream(self, prompt):
        async for event in self.agent.stream_async(prompt):
            if text := event.get('event', {}).get('contentBlockDelta', {}).get('delta', {}).get('text', ''):
                yield text
            for content in event.get('message', {}).get('content', []):
                if isinstance(content, dict) and (tool_use := content.get('toolUse', '')):
                    print(tool_use)
```
