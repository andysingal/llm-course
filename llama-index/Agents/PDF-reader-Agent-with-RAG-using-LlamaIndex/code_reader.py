from llama_index.core.tools import FunctionTool
import os


def code_reader_func(file_name):
    path = os.path.join("data", file_name)
    try:
        with open(path, "r") as f:
            content = f.read()
            return {"file_content": content}
    except Exception as e:
        return {"error": str(e)}


code_reader = FunctionTool.from_defaults(
    fn=code_reader_func,
    name="code_reader",
    description="""this tool can read the contents of code files and return 
    their results. Use this when you need to read the contents of a file""",
)
