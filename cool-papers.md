[MASAI: Modular Architecture for Software-engineering AI Agents](https://arxiv.org/abs/2406.11638)


[Memory Retrieval via Reflective Reasoning](https://arxiv.org/pdf/2512.20237)

MemR3iteratively retrieves and reflects using anevidence–gap tracker (Acts 0–3), refines the query about Buddy’s adoption date, and produces the correct answer

The system has three core advantages: 1) Accuracy and efficiency. By tracking the evidence and gap, and dynamically
routing between retrieval and reflection, MemR3 minimizes
unnecessary lookups and reduces noise, resulting in faster, more accurate answers. 2) Plug-and-play usage. As a controller independent of existing retriever or memory storage,
MemR3 can be easily integrated into memory systems, improving retrieval quality without architectural changes. 3)
Transparency and explainability. Since MemR3 maintains an explicit evidence-gap state over the course of an interaction, it can expose which memories support a given answer
and which pieces of information were still missing at each step, providing a human-readable trace of the agent’s decision process
