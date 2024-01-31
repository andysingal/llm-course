# gradio_interface.py

import gradio as gr
from core import run_graph

def test_function(input_text):
    return run_graph(input_text)

demo = gr.Interface(
    fn=test_function,
    inputs=gr.Textbox(lines=2, placeholder="Enter your query here..."),
    outputs=gr.Textbox()
)

if __name__ == "__main__":
    demo.launch()
