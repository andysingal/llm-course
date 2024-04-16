## LangChain
LangChain was launched as an open-source project by Harrison Chase, in October 2022. It can be used both in Python and JS/TS. LangChain is a framework for developing applications powered by language models, making them data-aware (with grounding) and agentic – that means, able to interact with external environments.LangChain provides modular abstractions for the components necessary to work with language models that we previously mentioned, such as prompts, memory and plug-ins. Alongside those components, LangChain also offer pre-built chains, that are structured contatenations of components. Those chains can be pre-built for specific use cases or also be customized.Overall, LangChain has the following core modules:

Models. These are the Large Language Models or Large Foundation Models that will be the engine of the application. LangChain supports proprietary models, such as those available in OpenAI and Azure OpenAI, and open-source models consumable from the Hugging Face Hub.
Definition

Hugging Face is a company and a community that builds and shares state-of-the-art models and tools for natural language processing and other machine learning domains. It developed the Hugging Face Hub, a platform where people can create, discover, and collaborate on machine learning models and LLMs, datasets, and demos. Hugging Face Hub hosts over 120k models, 20k datasets, and 50k demos in various domains and tasks, such as audio, vision, and language.

Alongside with models, LangChain also offers many prompts-related components that make it easier to manage the prompt flow.

1. Data connections. These refer to the building blocks needed to retrieve the additional non-parametric knowledge we want to provide the model with. Examples of data connetctions are document loaders or text embedding models.
2. Memory. It allows the application to keep references to user’s interactions, both in the short and long-term. It is typically based on vectorized embeddings stored into a VectorDB.
3. Chains. These are predetermined sequences of actions and calls to LLMs that make it easier to build complex applications that require chaining LLMs with each other or with other components. An example of chain might be: take the user query, chunk it into smaller pieces, embed those chunks, search for similar embeddings in a VectorDB, use the top three most similar chunks in the VectorDB as context to provide the answer, generate the answer.
4. Agents. Agents are entities that drive decision-making within LLMs-powered applications. They have access to a suite of tools and can decide which tool to call based on the user input and the context. Agents are dynamic and adaptive, meaning that they can change or adjust their actions based on the situation or the goal.
