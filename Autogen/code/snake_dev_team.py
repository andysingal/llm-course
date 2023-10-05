from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager

# Load the configuration for GPT-4 from a JSON file
config_list_gpt4 = config_list_from_json(
    "../OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-0613", "gpt-4-32k", "gpt-4", "gpt-4-0314"],
    },
)

# Define the GPT-4 configuration parameters
gpt4_config = {
    "seed": 42,
    "temperature": 0,
    "config_list": config_list_gpt4,
    "request_timeout": 1200,
}

# Define the common working directory for all agents
working_directory = "game_files"

# Initialize the Player agent, responsible for providing gameplay feedback
player = UserProxyAgent(
    name="Player",
    system_message="Player: Your role is to provide feedback on the gameplay. Collaborate with the Game Designer to ensure the game meets desired expectations.",
    code_execution_config={
        "work_dir": working_directory,
        "use_docker": False,
        "timeout": 120,
        "last_n_messages": 1,
    },
)

# Initialize the Game Designer agent, responsible for designing the game
game_designer = AssistantAgent(
    name="Game_Designer",
    llm_config=gpt4_config,
    system_message="Game Designer: Design the snake game, ensuring all details are documented in 'game_design.txt'. Collaborate with the Player to align the design with feedback and expectations."
)

# Initialize the Programmer agent, responsible for coding the game
programmer = AssistantAgent(
    name="Programmer",
    llm_config=gpt4_config,
    system_message="Programmer: Code the snake game and save it in the working directory. For code execution, collaborate with the Code Executor. If feedback is needed, consult the Game Tester."
)

# Initialize the Game Tester agent, responsible for playtesting the game
game_tester = UserProxyAgent(
    name="Game_Tester",
    system_message="Game Tester: Playtest the game and provide feedback on gameplay mechanics and user experience. Report any bugs or glitches. Collaborate with the Programmer for any necessary adjustments.",
    code_execution_config={
        "work_dir": working_directory,
        "use_docker": False,
        "timeout": 120,
        "last_n_messages": 3,
    },
    human_input_mode="ALWAYS",
)

# Initialize the Code Executor agent, responsible for executing the game code
code_executor = UserProxyAgent(
    name="Code_Executor",
    system_message="Code Executor: Execute the provided code from the Programmer in the designated environment. Report outcomes and potential issues. Ensure the code follows best practices and recommend enhancements to the Programmer.",
    code_execution_config={
        "work_dir": working_directory,
        "use_docker": False,
        "timeout": 120,
        "last_n_messages": 3,
    },
    human_input_mode="NEVER",
)

# Set up the group chat with all the agents
groupchat = GroupChat(
    agents=[player, game_tester, game_designer, programmer, code_executor],
    messages=[],
    max_round=150
)

# Create a manager for the group chat using the GPT-4 configuration
manager = GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

# Start the conversation with the Player's message
player.initiate_chat(
    manager,
    message="Let's design and implement a snake game. I aim for it to be entertaining and challenging."
)
