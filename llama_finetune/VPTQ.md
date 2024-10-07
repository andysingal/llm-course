Overview of VPTQ:

- Uses vector quantization to achieve high accuracy at extremely low bit-widths (<2-bit)
- Better accuracy at 1-2 bits compared to other methods
- Agile quantization inference with low decode overhead and high throughput
- Leverages vector quantization instead of traditional scalar-based weight quantization
- Compresses vectors into indices using lookup tables
- Achieves better accuracy and higher throughput with lower quantization overhead

📈 Performance Highlights:
- Llama-2 70B model quantized to 2.07 bits:
- Perplexity (W2): 3.93
- Inference speed: 9.7 tokens/second
- Memory usage: 19.54 GB

🛠️ Implementation:
- Open-source code available on GitHub
- Supports PyTorch, TensorFlow, and Hugging Face Transformers
- Provides Python API and command-line interface for easy use


<img width="949" alt="Screenshot 2024-10-06 at 9 04 16 PM" src="https://github.com/user-attachments/assets/07e59032-95a8-4771-9e21-54d68848b4a4">


Resource:

- https://github.com/microsoft/VPTQ
- [Demo](https://huggingface.co/spaces/VPTQ-community/VPTQ-Demo)
