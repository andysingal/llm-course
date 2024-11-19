<img width="1417" alt="Screenshot 2024-08-22 at 10 58 17 PM" src="https://github.com/user-attachments/assets/8d7345cb-b0d1-408a-85f8-0a6de6a56335">

Resource: https://arxiv.org/abs/2408.08274 


What is a Mixture of Experts (MoE), and why are they successful? Maarten just published a new visual guide on the Mixture of Experts (MoE) to explain the two main components of MoE: Experts and the Router. 👀

TL;DR:
- 🧠 MoE consists of multiple "expert" neural networks and a router that directs inputs to the most suitable experts
- 🔄 Experts aren't domain specialists, but rather learn to handle specific tokens in specific contexts
- ⚖️ Load balancing is crucial to ensure all experts are utilized effectively during training
- 🚂 The router uses probability distributions to select which experts process which tokens
- 📊 MoE allows models to have more parameters overall while using fewer during actual inference
- 🖼️ MoE isn't limited to language models - it's also being adapted for vision models
- 🔢 Mixtral 8x7B demonstrates the power of MoE, loading 46.7B parameters but only using 12.8B during inference
![Screenshot 2024-10-07 145408](https://github.com/user-attachments/assets/4f894179-4504-40cd-a34f-1c5d4540b385)


Resoures:
- [A Visual Guide to Mixture of Experts (MoE)](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mixture-of-experts)
