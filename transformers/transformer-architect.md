Let’s examine each building block, starting from the encoding part:

- Input embedding->those are the vector representation of tokenized input text;
- Positional encoding-> as the Transformer does not have an inherent sense of word order (unlike RNNs with their sequential nature),positional encodings are added to the input embeddings. These encodings provide information about the positions of words in the input sequence, allowing the model to understand the order of tokens;
- Multi-head attention layer-> a mechanism in which multiple self-attention mechanisms operate in parallel on different parts of the input data, producing multiple representations. This allows the Transformer model to attend to different parts of the input data in parallel and aggregate information from multiple perspectives.
- Add and Norm layer-> it combines element-wise addition and layer normalization. It adds the output of a layer to the original input and then applies layer normalization to stabilize and accelerate training. This technique helps mitigate gradient-related issues and improves the model's performance on sequential data;
Feed-forward layer-> it is responsible for transforming the normalized output of attention layers into a suitable representation for the final output, using non-linear activation function such as the ReLU.
The decoding part of the Transformer starts with a similar process as the encoding part, where the target sequence (output sequence) undergoes input embedding and positional encoding.

- Output embedding (shifted right)-> For the decoder, the target sequence is "shifted right" by one position. This means that at each position, the model tries to predict the token that comes after the token in the original target sequence. This is achieved by removing the last token from the target sequence and padding it with a special start-of-sequence token (start symbol). This way, the decoder learns to generate the correct token based on the preceding context during autoregressive decoding.

Decoders layers->similarly to the encoder block, also here we have positional encoding, multi-head attention, Add&Norm, and feed-forward layers, whose role is the same as above;

- Linear and SoftMax->those layers apply, respectively, a linear and non-linear transformation to the output vector. The non-linear transformation (softmax) convey the output vector into a probability distribution, corresponding to a set of candidate word. The word corresponding to the greatest element of the probability vector will be the output of the whole process.
-
- <img width="448" alt="Screenshot 2024-04-15 at 10 46 11 AM" src="https://github.com/andysingal/llm-course/assets/20493493/4080d8e4-1f3f-462d-b4b5-ec76d162c439">
