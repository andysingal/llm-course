#### Store the logic, connects all agents, and run the crew
from crewai import Crew, Process
from langchain_community.chat_models.ollama import ChatOllama
# setup tools
from tools.youtube_video_details_tool import YoutubeVideoDetailsTool
from tools.youtube_video_search_tools import YoutubeVideoSearchTool

from dotenv import load_dotenv
load_dotenv()

youtube_video_details_tool = YoutubeVideoDetailsTool()
youtube_video_search_tool = YoutubeVideoSearchTool()

chatOllama = ChatOllama(model="llama2")

# 1. Create agents
from agents import YoutubeAutomationAgents
from tasks import YoutubeAutomationTasks


agents = YoutubeAutomationAgents()

youtube_manager = agents.youtue_manager()
research_manager = agents.research_manager(youtube_video_details_tool=youtube_video_details_tool, youtube_video_search_tool=youtube_video_search_tool)
title_creator = agents.title_creator()
description_creator = agents.description_creator()
email_creator = agents.email_creator()

# Background info about youtube video 
video_topic = "Automating Tasks Using CrewAI"
video_details = """
In this video, we're diving into the innovative ways I'm using CrewAI to 
automate my YouTube channel. From conducting thorough research to 
streamline video preparation, CrewAI is revolutionizing how I create content. 
But that's not all - I'm also exploring how to harness the power of CrewAI 
to generate personalized emails for my subscribers. Join me on this journey 
as I unlock the potential of AI to enhance my YouTube channel and connect 
with my audience like never before.
"""
# 2. Create tasks

tasks = YoutubeAutomationTasks()

manage_youtube_creation = tasks.manage_youtube_video_creation(agent=youtube_manager, video_topic=video_topic, video_details=video_details)
manage_youtube_video_research = tasks.manage_youtube_video_research(agent=research_manager, video_topic=video_topic, video_details=video_details)
create_youtube_video_title = tasks.create_youtube_video_title(agent=title_creator, video_topic=video_topic, video_details=video_details)
create_youtube_video_description = tasks.create_youtube_video_description(agent=description_creator, video_topic=video_topic, video_details=video_details)
create_email_announcement_for_new_video = tasks.create_email_announcement_for_new_video(agent=email_creator, video_topic=video_topic, video_details=video_details)

# 3. Setup Crew

crew = Crew(
    agents=[
        youtube_manager,
        research_manager,
        title_creator,
        description_creator,
        email_creator
    ], 
    tasks=[
        manage_youtube_creation,
        manage_youtube_video_research,
        create_youtube_video_title,
        create_youtube_video_description,
        create_email_announcement_for_new_video
    ],
    process=Process.hierarchical,
    manager_llm=chatOllama

)

# Kick off 
results = crew.kickoff()

print("Crew usage", crew.usage_metrics)

print("Crew work results:")
print(results)