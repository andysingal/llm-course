[QuantFactory/prem-1B-SQL-GGUF](https://huggingface.co/QuantFactory/prem-1B-SQL-GGUF)

```py
from premsql.pipelines import SimpleText2SQLAgent
from premsql.generators import Text2SQLGeneratorHF
from premsql.executors import SQLiteExecutor

# Provide a SQLite file here or see documentation for more customization
dsn_or_db_path = "./data/db/california_schools.sqlite"

agent = SimpleText2SQLAgent(
    dsn_or_db_path=dsn_or_db_path,
    generator=Text2SQLGeneratorHF(
        model_or_name_or_path="premai-io/prem-1B-SQL",
        experiment_name="simple_pipeline",
        device="cuda:0",
        type="test"
    ),
)

question = "please list the phone numbers of the direct charter-funded schools that are opened after 2000/1/1"

response = agent.query(question)
response["table"]
```
<img width="700" alt="Screenshot 2024-09-14 at 6 57 37 AM" src="https://github.com/user-attachments/assets/deafb75a-71cf-425a-b6d2-c471f1480d12">
