# mixtral-inference

Inference code for the Mistral's "mixtral" 8x7B mixture of experts model. Largely based on the [Mistral 7B inference repository](https://github.com/mistralai/mistral-src/tree/main). Requires ~100GB of VRAM.

### Dependencies

PyTorch, SentencePiece, and xformers.

```
pip install -r requirements.txt
```

### Usage

Assumes you have 8 CUDA devices. You can modify this near the bottom of `main.py`.

```
python main.py
```