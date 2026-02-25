Model Context Protocol (MCP): A  shared language that ensures our engineered contexts are passed between agents with perfect fidelity

- MAS(Multi-Agent Systems): We will design a system that can run multiple independent agents, each one specialized in a distinct task such as research, writing, or data analysis. By giving each agent a clear context, we ensure it can excel at its specific responsibility.
- MCP: For our agents to collaborate, they need a shared language. MCP gives us the rules for how our agents pass tasks and information to one another. It provides a framework that ensures every message is structured, reliable, and perfectly understood.

- The flowchart illustrates the system’s complete workflow. Let’s break down the role of each component in this cognitive pipeline:

- Orchestrator (the project manager): The Orchestrator is the brain of the operation. It doesn’t perform specialized tasks itself but manages the entire workflow. It receives the user’s high-level goal, breaks it down into logical steps, and delegates each step to the right agent. It is also responsible for receiving the results from one agent and passing them as context to the next. In other words, it applies context chaining at the system level to our MAS.
- Researcher agent (the information specialist): This is our first specialized agent. Its purpose is to take a specific topic, find relevant information, and synthesize that information into a structured summary. In our project, it will receive a research task from the Orchestrator and return the results as a clear, bullet-pointed list.
- Writer agent (the content creator): This is our second specialized agent. Its strength lies in communication and creative expression. It takes the structured summary from the Researcher and transforms it into a polished, human-readable piece of content, with careful attention to tone, style, and narrative.

- **** Four key capabilities that make MCP tools “agentic” – streaming, resumability, durability, and [multi-turn interactions](https://developer.microsoft.com/blog/can-you-build-agent2agent-communication-on-mcp-yes)

- The MCP spec now supports agentic capabilities –
1. specifically, tools are now resumable
2.  can stream progress update notifications to clients, can request user input, and support the ability to poll for results (by returning resource links). These capabilities can be composed to build complex agent-to-agent systems.

The MCP specification has been significantly enhanced over the past few months with capabilities that narrow the gap for building long-running agentic behavior:

- Streaming & Partial Results: Real-time progress updates during execution (with proposals supporting partial results). See docs on progress updates.
- Resumability: Long-running agents benefit from maintaining task continuity across network interruptions, allowing clients to reconnect and resume where they left off rather than losing progress or restarting complex operations.
- Durability: Results survive server restarts. Tools can now return Resource Links which clients can poll or subscribe to. See docs on Resource Links
- Multi-turn: Interactive input mid-execution via elicitation (requesting user input mid-execution) and sampling (requesting LLM completions from client/host application)

### Best Practices
1. The structure of every MCP message is strictly defined to ensure consistency:

- All messages follow the JSON-RPC 2.0 format as clean JSON objects
- Messages must be UTF-8 encoded for universal compatibility
- Each message must appear on a single line with no embedded newlines, making parsing fast and reliable

2. Transport Layer: The transport layer defines how messages are transmitted between agents. The two primary methods are as follows:

- STDIO (standard input/output): For agents running on the same machine , they can communicate directly through standard input/output. This is the simplest and most direct method.
- HTTP: For agents running on different servers, messages are sent over the internet using standard HTTP requests.

3. Protocol Management: MCP also includes rules for compatibility and safety:
- Versioning: When using HTTP, a version header is required to ensure the client and server are using the same set of rules
- Security: There are rules for validating connections to prevent common cyberattacks and ensure you are communicating with the intended server

[Example_1](https://github.com/Denis2054/Context-Engineering-for-Multi-Agent-Systems/blob/main/Chapter02/MAS_MCP.ipynb)


#### Building the Agent
- Define each agent as a Python function
- Every agent function will accept a structured MCP message as input and return another MCP message as output.
- An agent’s specific role is shaped by its system prompt, which tells the LLM how to behave. 

#### Building the Orchestrator
We now have our specialized agents, but we need a way to manage them. That role belongs to the Orchestrator. Think of it as the project manager of our AI team. Its job is to take a high-level goal, break it into a sequence of tasks, and delegate those tasks to the right agent. It also manages the flow of information, taking the output from one agent and passing it as input to the next.

The workflow in the preceding figure begins when an initial goal is sent to the Orchestrator. The Orchestrator acts as a central hub, first sending a task to the Researcher agent. Once the research is complete, the agent sends its findings back to the Orchestrator. The Orchestrator then processes this information and sends a new task to the Writer agent. After the Writer finishes, it sends the completed content back to the Orchestrator. Finally, the Orchestrator assembles everything to produce the final output, completing the entire process.

```py
def orchestrator(initial_goal):
    """
    Manages the multi-agent workflow to achieve a high-level goal.
    """
    print("="*50)
    print(f"[Orchestrator] Goal Received: '{initial_goal}'")
    print("="*50)

    # --- Step 1: Orchestrator plans and calls the Researcher Agent ---
    print("\n[Orchestrator] Task 1: Research. Delegating to Researcher Agent.")
    research_topic = "Mediterranean Diet"
    mcp_to_researcher = create_mcp_message(
        sender="Orchestrator",
        content=research_topic
    )
    mcp_from_researcher = researcher_agent(mcp_to_researcher)
    print("\n[Orchestrator] Research complete. Received summary:")
    print("-" * 20)
    print(mcp_from_researcher['content'])
    print("-" * 20)

    # --- Step 2: Orchestrator calls the Writer Agent ---
    print("\n[Orchestrator] Task 2: Write Content. Delegating to Writer Agent.")
    mcp_to_writer = create_mcp_message(
        sender="Orchestrator",
        content=mcp_from_researcher['content']
    )
    mcp_from_writer = writer_agent(mcp_to_writer)
    print("\n[Orchestrator] Writing complete.")

    # --- Step 3: Orchestrator presents the final result ---
    final_output = mcp_from_writer['content']
    print("\n" + "="*50)
    print("[Orchestrator] Workflow Complete. Final Output:")
    print("="*50)
    print(final_output)
```

#### Running the system

The final step is to run the system and watch them work together.
```py
#@title 5. Run the System
# ------------------------------------------------------------------------
# Let's give our Orchestrator a high-level goal and watch the agent team work.
# ------------------------------------------------------------------------
user_goal = "Create a blog post about the benefits of the Mediterranean diet."
orchestrator(user_goal)
```


### Error Handling, Validation and Safeguards
To make the workflow more reliable and move closer to production-ready, we need to strengthen it with error handling, validation, and safeguards.


