```py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "KbsdJames/Omni-Judge", 
    device_map="auto", 
    torch_dtype=torch.bfloat16, 
)
tokenizer = AutoTokenizer.from_pretrained(
    "KbsdJames/Omni-Judge", 
    trust_remote_code=True
)

# set terminators for decoding
terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

question = "Compute the smallest positive integer $n$ for which $\\sqrt{100+\\sqrt{n}}+\\sqrt{100-\\sqrt{n}}$ is an integer."
reference_answer = "6156"
student_solution = "Let's approach this step-by-step:\n\n1) Let's denote $\\sqrt{100+\\sqrt{n}}+\\sqrt{100-\\sqrt{n}} = k$, where k is an integer.\n\n2) Square both sides:\n   $(\\sqrt{100+\\sqrt{n}}+\\sqrt{100-\\sqrt{n}})^2 = k^2$\n\n3) Expand the left side:\n   $100+\\sqrt{n} + 100-\\sqrt{n} + 2\\sqrt{(100+\\sqrt{n})(100-\\sqrt{n})} = k^2$\n\n4) Simplify:\n   $200 + 2\\sqrt{10000-n} = k^2$\n\n5) Rearrange:\n   $\\sqrt{10000-n} = \\frac{k^2-200}{2}$\n\n6) For this to be true, $\\frac{k^2-200}{2}$ must be a perfect square. Let's call it $m^2$:\n   $\\frac{k^2-200}{2} = m^2$\n\n7) Multiply both sides by 2:\n   $k^2-200 = 2m^2$\n\n8) Rearrange:\n   $k^2 = 2m^2 + 200$\n\n9) For the smallest positive n, we need the smallest k > 14 (since $\\sqrt{100+\\sqrt{n}}+\\sqrt{100-\\sqrt{n}} > 2\\sqrt{100} = 20$) that makes this equation true.\n\n10) Testing values:\n    For k = 15: $15^2 = 225 = 2m^2 + 200$\n                $25 = 2m^2$\n                $m^2 = 12.5$ (not an integer)\n\n    For k = 16: $16^2 = 256 = 2m^2 + 200$\n                $56 = 2m^2$\n                $m^2 = 28$ (integer)\n\n11) So, the smallest valid k is 16, and m = $\\sqrt{28}$\n\n12) Now, going back to step 5:\n    $\\sqrt{10000-n} = \\frac{16^2-200}{2} = 28$\n\n13) Solve for n:\n    $10000-n = 28^2 = 784$\n    $n = 10000 - 784 = 9216$\n\nTherefore, the smallest positive integer n for which $\\sqrt{100+\\sqrt{n}}+\\sqrt{100-\\sqrt{n}}$ is an integer is 9216."

# pre-process
formatted_context = tokenizer.get_context(
    question,
    reference_answer,
    student_solution,
)
model_inputs = tokenizer(formatted_context, return_tensors="pt")
input_ids = model_inputs["input_ids"]
attention_mask = model_inputs["attention_mask"]

# do inference
pred = model.generate(
    input_ids=input_ids.to(model.device),
    attention_mask=attention_mask.to(model.device),
    do_sample = False,
    num_return_sequences = 1,
    max_new_tokens = 300,
)[0].cpu().tolist()

# post-process
pred = pred[len(input_ids[0].cpu().tolist()):]
for terminator in terminators:
    if terminator in pred:
        pred = pred[:pred.index(terminator)]
response = tokenizer.decode(pred, skip_special_tokens=True)
pred_truth = tokenizer.parse_response(response)

# if response parsing fails, the answer/judgement/justification will be None,
# which we consider as errors in prediction. 
# in this case, using multiple sampling may help.

print("answer:", pred_truth["answer"])
# >>> answer: 9216
print("judgement:", pred_truth["judgement"])
# >>> judgement: FALSE
print("justification:", pred_truth["justification"])
```
