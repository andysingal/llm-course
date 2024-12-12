- https://stackoverflow.com/questions/75962909/convert-llama-to-onnx
- [optimum-neuron](https://pypi.org/project/optimum-neuron/)

```py
# Export the Model to ONNX Format
from transformers import AutoModelForSequenceClassification
import torch

# Load a pre-trained model
model_name = "bert-base-uncased"
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Dummy input for tracing
dummy_input = torch.ones(1, 16, dtype=torch.int64)

# Export to ONNX
torch.onnx.export(
    model, 
    dummy_input, 
    "bert_model.onnx", 
    input_names=["input_ids"], 
    output_names=["output"],
    dynamic_axes={"input_ids": {0: "batch_size", 1: "sequence_length"}}
)
```
## Optimize the ONNX Model
```py
## Optimize the ONNX Model
## Optimize the model for faster inference using ONNX Runtime’s optimization tools.
python -m onnxruntime.transformers.optimizer --input bert_model.onnx --output optimized_bert.onnx

```
## Serve with ONNX Runtime
```py
import onnxruntime as ort
import numpy as np

# Load the optimized model
session = ort.InferenceSession("optimized_bert.onnx")

# Prepare input
input_ids = np.ones((1, 16), dtype=np.int64)

# Run inference
outputs = session.run(None, {"input_ids": input_ids})
print("Model Output:", outputs)
```

Source: https://dev.to/nareshnishad/day-49-serving-llms-with-onnx-runtime-3828
