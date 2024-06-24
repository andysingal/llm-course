```py
import os
import tempfile
import pypandoc

from llama_index.core.tools import FunctionTool

def generate_report(md_text, output_file):
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as temp_md:
        temp_md.write(md_text.encode("utf-8"))
        temp_md_path = temp_md.name
        
    try:
        output = pypandoc.convert_file(temp_md_path, "pdf", outputfile=output_file)
        return "Success"
    
    finally:
        os.remove(temp_md_path)
        
report_generator = FunctionTool.from_defaults(
    fn=generate_report,
    name="report_generator",
    description="This tool can generate a PDF report from markdown text"
)
```
