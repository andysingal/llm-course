## The Copilot System
The Copilot system is a new category of software that serves as an expert helper to users trying to accomplish complex tasks. This concept was coined by Microsoft and already introduce into its applications, such as M365 Copilot or the new Bing, now powered by GPT-4. With the same framework and orchestration, developers can now build their own copilots to embed within their applications.But what exactly is a copilot?As the name suggests, copilots are meant to be AI assistant that work side-by-side with users and support them in various activities, from information retrieval to blog writing and posting, from ideas brainstorming to code review and generation.Below some peculiar features of copilots:

A copilot is powered by LLMs or, more generally, LFMs, meaning that these re the reasoning engines that make the copilot “intelligent”. This reasoning engine is one of its components, but not the only one. A copilot also relies on other technologies, such as apps, data sources, and user interfaces, to provide a useful and engaging experience for users.

<img width="470" alt="Screenshot 2024-04-16 at 10 26 02 AM" src="https://github.com/andysingal/llm-course/assets/20493493/606c4ea8-5804-4f55-b229-15545a347091">

A copilot is designed to have a conversational user interface, allowing users to interact with it using natural language. This reduces or even eliminates the knowledge gap between complex systems which need domain-specific taxonomy (for example, querying tabular data needs the knowledge of programming languages such as T-SQL) and users.



<img width="562" alt="Screenshot 2024-04-16 at 10 26 58 AM" src="https://github.com/andysingal/llm-course/assets/20493493/48cdddca-75ae-4e38-b498-91fc3dcf91e7">

A copilot has a scope. It means that it is grounded to domain-specific data, so that it is entitled to answer only within the perimeter of the application or domain.
Definition

- Grounding is the process of using large language models (LLMs) with information that is use-case specific, relevant, and not available as part of the LLM’s trained knowledge. It is crucial for ensuring the quality, accuracy and relevance of the output. Grounding also helps Copilot to be restricted or scoped to application-specific data, so that it can support only within the boundaries of the provided knowledge base.

Being restricted and scoped also means that the information that is used to ground the LLMs is not stored or used to train the LLMs. The LLMs are trained on a large corpus of public information, but they are not updated or fine-tuned with your data. The information that is used to ground the LLMs is only provided as an input to the LLMs along with your prompt, and it is not retained or shared with anyone else.


<img width="444" alt="Screenshot 2024-04-16 at 10 28 10 AM" src="https://github.com/andysingal/llm-course/assets/20493493/66eb223a-e2a8-438b-ae49-43850840a46c">


### The copilot's capabilities can be extended by skills, which can be code or calls to other models. In fact, the LLM (our reasoning engine) might have two kind of limitations:

- Limited parametric knowledge. This is due to the knowledge base cutoff date that is a physiological feature of LLM. In fact, their training dataset will always be “outdated”, not in line with the current news. This can be overcome by adding non-parametric knowledge with grounding, as previously seen.

- Lack of executive power. This means that LLMs by themselves are not empowered to make actions. Let’s consider for example the well-known ChatGPT: if we ask it to generate a LinkedIn post about productivity tips, we will then need to copy and paste it in our LinkedIn profile as ChatGPT is not able to do so by itself. That is the reason why we need plug-ins. Plug-ins are LLMs’ connector towards the external world that not only serve as input sources to extend LLMs’ non-parametric knowledge (for example, to allow web search), but also as output sources so that the copilot can actually execute actions. For example, with a LinkedIn plug-in, our copilot powered by an LLM will be not only able to generate the post, but also to post it online.

<img width="587" alt="Screenshot 2024-04-16 at 10 30 04 AM" src="https://github.com/andysingal/llm-course/assets/20493493/2446f857-9733-41d1-92e3-c4963a659ec1">
