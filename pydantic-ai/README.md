[Agent Framework / shim to use Pydantic with LLMs](https://ai.pydantic.dev/)

[Example](https://qiita.com/atsukish/items/a1613c77cecd41980467)

[MCP Run Python](https://simonwillison.net/2025/Apr/18/mcp-run-python/)

[Agent2Agent (A2A) Protocol](https://ai.pydantic.dev/a2a/)

[Pydantic AI with Bright Data’s Web MCP for Agents with Data Access](https://brightdata.com/blog/ai/pydantic-ai-with-web-mcp)

<img width="1114" alt="Screenshot 2025-04-24 at 7 27 39 AM" src="https://github.com/user-attachments/assets/0ae0641c-55fa-49b9-b97f-fef0f2540398" />

```py
import pydantic  # pip show pydantic
print(f"Our Pydantic version: {pydantic.VERSION}")

from pprint import pprint
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

class Options(BaseModel):
    """Options object for a multiple-choice question, containing choices A, B, C, and D."""
    A: str = Field(..., description='Option A')
    B: str = Field(..., description='Option B')
    C: str = Field(..., description='Option C')
    D: str = Field(..., description='Option D')

class MCQ(BaseModel):
    """Structure for a multiple-choice question, including question ID, stem, options, and answer."""
    qid: int = Field(..., description='Question ID')
    question: str = Field(..., description='Question stem')
    options: Options = Field(..., description="The four options for this question")
    ans: Optional[str] = Field(default=None, description='Answer')

class Meta(BaseModel):
    """Metadata for the exam, including year, subject, and exam session."""
    year: Optional[int] = Field(default=None, description='Year (e.g., 2023)')
    subject: Optional[str] = Field(default=None, description='Subject name')
    times: Optional[int] = Field(default=None, description='Exam session (e.g., 1st, 2nd)')

class ExtractExam(BaseModel):
    """
    Extracts an entire exam paper.
    - qset: Collection of multiple-choice questions
    - subject: Subject name
    - year: Exam year
    - times: Exam session number
    """
    qset: List[MCQ] = Field(..., description='Multiple-choice questions')
    metadata: Meta = Field(..., description='Exam metadata')

schema = MCQ.model_json_schema()
pprint(schema)

```
