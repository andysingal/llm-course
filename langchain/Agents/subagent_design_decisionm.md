In the subagents architecture, a central main agent (often referred to as a supervisor) coordinates subagents by calling them as tools. The main agent decides which subagent to invoke, what input to provide, and how to combine results. Subagents are stateless—they don’t remember past interactions, with all conversation memory maintained by the main agent. This provides context isolation: each subagent invocation works in a clean context window, preventing context bloat in the main conversation.


<img width="655" height="440" alt="Screenshot 2026-01-16 at 8 35 34 PM" src="https://github.com/user-attachments/assets/09cf1f4b-cddc-4f95-9f2d-cb857ba6a2e9" />







### References:

[###1](https://www.blog.langchain.com/choosing-the-right-multi-agent-architecture/#:~:text=In%20the%20subagents%20pattern%2C%20a,stateless%2C%20providing%20strong%20context%20isolation.)

[##2](https://www.youtube.com/watch?v=A3DKwLORVe4)

