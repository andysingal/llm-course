<img width="1008" height="604" alt="Screenshot 2026-07-31 at 4 28 29 PM" src="https://github.com/user-attachments/assets/ae4866f3-72df-4647-a1fb-e0d60e48a2ab" />

The "Why": Framework vs Pattern

- A framework is a Tool (The " How")
- concrete library of code (langchain, MAF), a set of high-quality hammers, saws and power tools

- A pattern is a Blueprint( The "What" & "Why")

- - A conceptual, resuable solution to a common problem
  - The arhcitectural blueprint for a 'self-correcting system' or a 'delegation system'
 
  <img width="1124" height="371" alt="Screenshot 2026-07-31 at 4 43 27 PM" src="https://github.com/user-attachments/assets/19b20df3-f361-4a55-b7f3-e2a068392028" />

  
### Stateful Systems

- Saves data: Keeps track of client sessions and past history in its own memory or storage.
- Harder to scale: You must connect a user back to the exact same server or sync data across multiple servers.
- Risk of data loss: If a server crashes, active session info can be lost unless saved elsewhere.
- Examples: Traditional login sessions saved on a server, online video games, and databases

### Stateless Systems

- No memory: Does not store past request data on the server; each request must bring its own details or tokens.
- Easy to scale: Any server can answer any request, making it simple to add more computers to handle heavy traffic.
- Safe from crashes: If a server dies, another server takes over instantly without breaking the user experience.
- Examples: HTTP web requests, REST APIs, and token-based checks like JWT


### Four pillars of Agentic Design

<img width="665" height="274" alt="Screenshot 2026-08-01 at 2 29 13 PM" src="https://github.com/user-attachments/assets/e00f2b54-62db-4e3a-bef2-ed7a436a842d" />

Principle 1: Goal Directed

__ The Concept: An agent is defined by its purpose, not its tasks

Instruction-Driven (Old Way)

- call_api("weather", "London")
- call_search("best laptop")
- You must provide the exact steps

Goal-Driven (New Way)
Goal: "Plan a 3-day trip to London for me"
The agent must discover the steps (check weather , find flights, book flights)

Architectural Implication:
The 'Goal' is the primary input that initiates the reasoning loop. All planning is derived from this goal


Principle 2: Reactive

<img width="671" height="327" alt="Screenshot 2026-08-01 at 2 36 39 PM" src="https://github.com/user-attachments/assets/9b592309-8b16-473b-9927-dd58be49ffa5" />

Perception in large language models (LLMs) refers to how an AI system receives, translates, and processes external multi-modal inputs—such as images, video, audio, or continuous sensor signals—into the internal token embedding space of the model


Principle 3: Stateful (Has Memory)

<img width="670" height="275" alt="Screenshot 2026-08-01 at 2 40 58 PM" src="https://github.com/user-attachments/assets/eb730de8-ae5a-4e63-a9c0-a8c0132e1f80" />

Principle 4: Autonomous 

The Concept: An agent can act on its own to make progress. This is the result of the other three principles

Because an agent is ...

Goal Directed (it knows its destination)
Reactive (it can see the road)
Stateful (it knows where it's been)

... it can be Autonomous (it can "drive the car")


### The "Tool Use" Pattern 

<img width="912" height="495" alt="Screenshot 2026-08-01 at 3 00 24 PM" src="https://github.com/user-attachments/assets/ecbda0f6-bdb7-4b02-b516-b6375a37f2af" />

Mechanics Part 1: The "Schema" (Describing the Tool)

<img width="925" height="423" alt="Screenshot 2026-08-01 at 3 03 49 PM" src="https://github.com/user-attachments/assets/9d75b362-d6d1-4c25-90b6-7d15a99d7a69" />

Mechanics Part 2: The LLM Role (The "Chooser")

The LLM Reasoning Process:

- It receives the user's goal: "Whats the weather
- It reviews the list of available tool schemas
- It reasons: "The goal is about weather. The get_weather tool's description matches this goal. The goal specifies a city, 'London'. The tool requires a 'city" parameter"

Mechanics Part 3: The Orchestrator's Role (The "Executor")

<img width="930" height="382" alt="Screenshot 2026-08-01 at 3 09 27 PM" src="https://github.com/user-attachments/assets/004eeb3b-0dc9-4d19-bc1f-7e277956c9ed" />



### The Planning Pattern 

The process of using an LLM to deompose a high-level goal into an explicit ordered list of executable steps 

The Enabling Technique: "Chain of Thought" (CoT)

Thought: The user wants the weather, and they want it emailed
Plan:
  - Call get_weather for "London"
  - Call send_email with the result of step

Action: [Outputs the first tool call: call_weather("London")]



<img width="862" height="403" alt="Screenshot 2026-08-01 at 3 15 44 PM" src="https://github.com/user-attachments/assets/45e686dd-9412-444d-b14e-b13976df598a" />


