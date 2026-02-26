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
#### Error handling and validation
To make the workflow more reliable and move closer to production-ready, we need to strengthen it with error handling, validation, and safeguards.

- Resilience: Hardening the connection to the LLM so temporary issues (such as API timeouts or rate limits) don’t crash the system
- Reliability: Ensuring message integrity so that agents always exchange predictable, valid MCP messages

##### Making the Agent System More Robust
```
# --- Hardening the call_llm Function ---
def call_llm_robust(system_prompt, user_content, retries=3, delay=5):
    """A more robust helper function to call the OpenAI API with retries."""
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-5.2",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API call failed on attempt {i+1}/{retries}. Error: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retries failed.")
                return None
```
```
def create_mcp_message(sender, content, metadata=None):
    """Creates a standardized MCP message."""
    return {
        "protocol_version": "1.0",
        "sender": sender,
        "content": content,
        "metadata": metadata or {}
    }
```

In this upgraded function, call_llm_robust, we wrap the API call in a try/except block inside a loop. If an error occurs, the system waits a few seconds before trying again, with time.sleep pausing execution between attempts. This retry mechanism makes the system more resilient to temporary network issues.

#### Validating MCP messages

For agents to communicate reliably, they must be able to trust the messages they receive. If a malformed message slips through, the entire workflow could fail. To prevent this, we introduce an MCP validator, a simple guardrail that checks that every message conforms to our protocol.

```
# --- The MCP Validator ---
def validate_mcp_message(message):
    """A simple validator to check the structure of an MCP message."""
    required_keys = ["protocol_version", "sender", "content", "metadata"]
    if not isinstance(message, dict):
        print(f"MCP Validation Failed: Message is not a dictionary.")
        return False
    for key in required_keys:
        if key not in message:
            print(f"MCP Validation Failed: Missing key '{key}'")
            return False
    print(f"MCP message from {message['sender']} validated successfully.")
    return True
```

This function is a crucial guardrail. The Orchestrator will call validate_mcp_message before passing any message along, ensuring the structure is complete and predictable. It first checks that the input is a dictionary, then verifies that all required keys (protocol_version, sender, content, and metadata) are present. This prevents errors caused by malformed context slipping into the workflow.

#### Adding agent specialization controls and validation
```

#@title 4.Building the Agents: The Specialists

# --- Agent 1: The Researcher ---
def researcher_agent(mcp_input):
    """This agent takes a research topic, finds information, and returns a summary."""
    print("\n[Researcher Agent Activated]")
    simulated_database = {
        "mediterranean diet": "The Mediterranean diet is rich in fruits, vegetables, whole grains, olive oil, and fish. Studies show it is associated with a lower risk of heart disease, improved brain health, and a longer lifespan."
    }
    research_topic = mcp_input['content']
    research_result = simulated_database.get(research_topic.lower(), "No information found.")
    system_prompt = "You are a research analyst. Synthesize the provided information into 3-4 concise bullet points."
    summary = call_llm_robust(system_prompt, research_result)
    print(f"Research summary created for: '{research_topic}'")
    return create_mcp_message(
        sender="ResearcherAgent",
        content=summary,
        metadata={"source": "Simulated Internal DB"}
    )

# --- Agent 2: The Writer ---
def writer_agent(mcp_input):
    """This agent takes research findings and writes a short blog post."""
    print("\n[Writer Agent Activated]")
    research_summary = mcp_input['content']
    system_prompt = "You are a content writer. Take the following research points and write a short, appealing blog post (approx. 150 words) with a catchy title."
    blog_post = call_llm_robust(system_prompt, research_summary)
    print("Blog post drafted.")
    return create_mcp_message(
        sender="WriterAgent",
        content=blog_post,
        metadata={"word_count": len(blog_post.split())}
    )

# --- Agent 3: The Validator ---
def validator_agent(mcp_input):
    """This agent fact-checks a draft against a source summary."""
    print("\n[Validator Agent Activated]")
    source_summary = mcp_input['content']['summary']
    draft_post = mcp_input['content']['draft']
    system_prompt = """
    You are a meticulous fact-checker. Determine if the 'DRAFT' is factually consistent with the 'SOURCE SUMMARY'.
    - If all claims in the DRAFT are supported by the SOURCE, respond with only the word \"pass\".
    - If the DRAFT contains any information not in the SOURCE, respond with \"fail\" and a one-sentence explanation.
    """
    validation_context = f"SOURCE SUMMARY:\n{source_summary}\n\nDRAFT:\n{draft_post}"
    validation_result = call_llm_robust(system_prompt, validation_context)
    print(f"Validation complete. Result: {validation_result}")
    return create_mcp_message(
        sender="ValidatorAgent",
        content=validation_result
    )
```
The workflow is no longer strictly sequential. After writer_agent produces a draft, the Orchestrator delegates to validator_agent. If the validation fails, the Orchestrator sends the draft back to the Writer and includes the validator’s feedback. This creates a powerful self-correcting system that mimics a real-world editorial process.

#### The final Orchestrator with a validation loop

```
#@title 5.The Final Orchestrator with Validation Loop
def final_orchestrator(initial_goal):
    """Manages the full multi-agent workflow, including validation and revision."""
    print("="*50)
    print(f"[Orchestrator] Goal Received: '{initial_goal}'")
    print("="*50)

    # --- Step 1: Research ---
    print("\n[Orchestrator] Task 1: Research. Delegating to Researcher Agent.")
    research_topic = "Mediterranean Diet"
    mcp_to_researcher = create_mcp_message(sender="Orchestrator", content=research_topic)
    mcp_from_researcher = researcher_agent(mcp_to_researcher)

    if not validate_mcp_message(mcp_from_researcher) or not mcp_from_researcher['content']:
        print("Workflow failed due to invalid or empty message from Researcher.")
        return

    research_summary = mcp_from_researcher['content']
    print("\n[Orchestrator] Research complete.")

    # --- Step 2 & 3: Iterative Writing and Validation Loop ---
    final_output = "Could not produce a validated article."
    max_revisions = 2
    for i in range(max_revisions):
        print(f"\n[Orchestrator] Writing Attempt {i+1}/{max_revisions}")

        writer_context = research_summary
        if i > 0:
            writer_context += f"\n\nPlease revise the previous draft based on this feedback: {validation_result}"

        mcp_to_writer = create_mcp_message(sender="Orchestrator", content=writer_context)
        mcp_from_writer = writer_agent(mcp_to_writer)

        if not validate_mcp_message(mcp_from_writer) or not mcp_from_writer['content']:
            print("Aborting revision loop due to invalid message from Writer.")
            break
        draft_post = mcp_from_writer['content']

        # --- Validation Step ---
        print("\n[Orchestrator] Draft received. Delegating to Validator Agent.")
        validation_content = {"summary": research_summary, "draft": draft_post}
        mcp_to_validator = create_mcp_message(sender="Orchestrator", content=validation_content)
        mcp_from_validator = validator_agent(mcp_to_validator)

        if not validate_mcp_message(mcp_from_validator) or not mcp_from_validator['content']:
            print("Aborting revision loop due to invalid message from Validator.")
            break
        validation_result = mcp_from_validator['content']

        if "pass" in validation_result.lower():
            print("\n[Orchestrator] Validation PASSED. Finalizing content.")
            final_output = draft_post
            break
        else:
            print(f"\n[Orchestrator] Validation FAILED. Feedback: {validation_result}")
            if i < max_revisions - 1:
                print("Requesting revision.")
            else:
                print("Max revisions reached. Workflow failed.")

    # --- Step 4: Final Presentation ---
    print("\n" + "="*50)
    print("[Orchestrator] Workflow Complete. Final Output:")
    print("="*50)
    print(final_output)
```
#### Running the final robust system
```
#@title 6.Run the Final, Robust System
user_goal = "Create a blog post about the benefits of the Mediterranean diet."
final_orchestrator(user_goal)
```



     


