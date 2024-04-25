# Store the logic for running all agents,
# Describing the agents (goal, backstory, etc...)
from crewai import Agent
from langchain.agents import load_tools 

# Human tools
human_tools = load_tools(["human"])

class YoutubeAutomationAgents():
    def youtue_manager(self):
        return Agent(
            role="YouTube Manager",
            goal="""Oversee the YouTube preparation proceess including market research, title ideation, 
                description, and email announcement creation required to make a YouTube Video
            """,
            backstory="""As a methodical and detailed oriented manager, you are responsible for overseeing the preparation of YouTube videos.
                When creating YouTube videos, you follow the following process to create a video that has a high chance of success.
                1. Search YouTube to find a minimum of 15 other videos on the same topic and analyze their titles and descriptions.
                2. Create a list of 10 potential titles that are less than 70 characters and should have a high click-through-rate.
                    - Make sure you pass the list of 1 videos to the title creator
                    so that they can use the information to create the titles.
                3. Write a description for the YouTube video.
                4. Write an email that can be sent to all subscribers to promote the new video.
            """,
            allow_delegation=True,
            verbose=True,
        )

    def research_manager(self, youtube_video_search_tool, youtube_video_details_tool):
        return Agent(
            role="YouTube Research Manager",
            goal="""For a given topic and description for a new YouTube video, find a minimum of 15 high-performing videos 
                on the same topic with the ultimate goal of populating the research table which will be used by 
                other agents to help them generate titles  and other aspects of the new YouTube video 
                that we are planning to create.""",
            backstory="""As a methodical and detailed research managar, you are responsible for overseeing researchers who 
                actively search YouTube to find high-performing YouTube videos on the same topic.""",
            verbose=True,
            allow_delegation=True,
            tools=[youtube_video_search_tool, youtube_video_details_tool]
        )
    
    def title_creator(self):
        return Agent(
            role="Title Creator",
            goal="""Create 10 potential titles for a given YouTube video topic and description. 
                You should also use previous research to help you generate the titles.
                The titles should be less than 70 characters and should have a high click-through-rate.""",
            backstory="""As a Title Creator, you are responsible for creating 10 potential titles for a given 
                YouTube video topic and description.""",
            verbose=True
        )
    
    def description_creator(self):
        return Agent(
            role="Description Creator",
            goal="""Create a description for a given YouTube video topic and description.""",
            backstory="""As a Description Creator, you are responsible for creating a description for a given 
                YouTube video topic and description.""",
            verbose=True
        )
    
    def email_creator(self):
        return Agent(
            role="Email Creator",
            goal="""Create an email to send to the marketing team to promote the new YouTube video.""",
            backstory="""As an Email Creator, you are responsible for creating an email to send to the marketing team 
                to promote the new YouTube video.
                
                It is vital that you ONLY ask for human feedback after you've created the email.
                Do NOT ask the human to create the email for you.
                """,
            verbose=True,
            tools=human_tools
        )