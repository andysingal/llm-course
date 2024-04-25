# Defining specific task neeeds to execute

from functools import partial
from crewai import Task
from textwrap import dedent


class YoutubeAutomationTasks():

    def manage_youtube_video_creation(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Oversee the YouTube prepration process including market research, title ideation, 
                description creation, and email creation reqired to make a YouTube video. The ultimate goal is for you to generate 
                a report including a research table, potential high click-through-rate titles, 
                a YouTube video description, and an emails newsletter update about the new video.
                               
                The video topic is: {video_topic}
                The video details are: {video_details}  

                 
                Here is an example report that you can use as a template:
                - It is important to note that the example report only contains 2 videos, 
                    but the final report should contain 15 videos.
                - It is important to note that the example report only contains 3 potential high CTRO titles,
                     but the final report should contain 10 titles.               
                
                Example Report:
                # YouTube Competition Research Table:
                - Video 1:
                    - Title: "How to Make a YouTube Video"
                    - View Count: 100,000
                    - Days Since Published: 30
                    - Channel Subscriber Count: 1,000
                    - Video URL: https://www.youtube.com/watch?v=1234
                - Video 2:
                    - Title: "How to Make a YouTube Video"
                    - View Count: 100,000
                    - Days Since Published: 30
                    - Channel Subscriber Count: 1,000
                    - Video URL: https://www.youtube.com/watch?v=1234

                ...
                                    
                # Potential High CTRO Titles:
                - How to Make a YouTube Video
                - How to Make a YouTube Video in 2021
                - How to Make a YouTube Video for Beginners
                [THE REST OF THE POTENTIAL HIGH CTRO TITLES GO HERE]
                                    
                # YouTube Video Description:
                🤖 Download the CrewAI Source Code Here:
                https://brandonhancock.io/crewai-updated-tutorial-hierarchical 

                Don't forget to Like and Subscribe if you're a fan of free source code 😉

                Ready to lead an AI revolution? Watch and learn how to build your own CrewAI from the ground up using the latest CrewAI features, and get set to deploy an army of AI agents at your command. This video is your ultimate guide to creating a powerful digital workforce, enhancing your projects with intelligent automation and streamlined workflows. Discover the secrets to customizing AI agents, setting them on tasks, and managing a smooth operation with CrewAI. It’s time to amplify your tech capabilities, and after this tutorial, you'll be equipped to engineer an AI crew that transforms any complex challenge into a simple task. Start your journey to AI mastery with CrewAI today!

                📰 Stay updated with my latest projects and insights:
                LinkedIn: https://www.linkedin.com/in/brandon-hancock-ai/
                Twitter: https://twitter.com/bhancock_ai

                Resources:
                - https://github.com/joaomdmoura/crewAI-examples/
                - https://www.crewai.io/
                - https://twitter.com/joaomdmoura/status/1756428892045496608
                - https://serper.dev/
                
                # Email Announcement:
                
                Subject: New CrewAI Tutorial: Learn How To Use the Latest CrewAI Features

                Hey [FIRST NAME GOES HERE]!

                Exciting update: CrewAI's new version is here, making it quicker and more dependable!

                You loved our first CrewAI tutorial, so I just published a new one for you.

                In this tutorial, you'll get up to speed with CrewAI's new features. We'll then apply these updates by building an AI Newsletter, demonstrating how to use what you've learned in a real project.

                [VIDEO PREVIEW HERE]

                Here's what's in store:

                Learn to manage a team with CrewAI's new Hierarchical workflow.
                Discover how asynchronous tasks can boost your efficiency.
                Find out how the Expected Output feature ensures accuracy and reliability.
                Plus, lots more insights!
                Dive into the tutorial to explore CrewAI's enhanced functions:

                [VIDEO PREVIEW HERE]

                Questions or want to share how you're doing? Email me or comment on YouTube.

                Happy coding!

                Cheers, 
                Brandon Hancock
            """),
            agent=agent,
            output_file="output/YouTube_Video_Creation_Report.txt",
            expected_output=dedent(f"""
                Generate a report that is formatted exactly like the example report provided to you earlier.
                Make sure the report contains 15 videos, 10 potential high CTRO titles, a YouTube video description, and an email newsletter update about the new video.
                The researched video should have all the required details and valid URLs.
            """)
        )

    def manage_youtube_video_research(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""For a given video topic and description, search youtube videos to find 
                15 high-performing YouTube videos on the same topic. Once you have found the videos, 
                research the YouTube video details to finish populate the missing fields in the 
                research CSV. When delegating tasks to other agents, make sure you include the 
                URL of the video that you need them to research.
                            
                This research CSV which will be used by other agents to help them generate titles 
                and other aspects of the new YouTube video that we are planning to create.
                               
                Research CSV Outline:
                - Title of the video
                - View count
                - Days since published
                - Channel subscriber count
                - Video URL
                       
                The video topic is: {video_topic}
                The video details is: {video_details}

                Important Notes: 
                - Make sure the CSV uses ; as the delimiter
                - Make sure the final Research CSV Outline doesn't contain duplicate videos
                - It is SUPER IMPORTANT that you properly match up view counts, subscriber counts, 
                    and everything else to the video URL.
                - It is SUPER IMPORTANT that you only populate the research CSV with real YouTube videos 
                    and YouTube URLs that actually link to the YouTube Video.
                """),
            agent=agent,
            expected_output=dedent(f"""
                Video Title; View Count; Days Since Published; Channel Subscriber Count; Video URL
                How to Make a YouTube Video; 100,000; 30; 1,000; https://www.youtube.com/watch?v=1234;
                How to Get Your First 1000 Subscribers; 100,000; 30; 1,000; https://www.youtube.com/watch?v=1234;
                       ...              
                """)
        )

    def create_youtube_video_title(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Create 10 potential titles for a given YouTube video topic and description. 
                It is also very important to use researched videos to help you generate the titles.
                The titles should be less than 70 characters and should have a high click-through-rate.
                               
                Video Topic: {video_topic}
                Video Details: {video_details}
                """),
            agent=agent,
            expected_output=dedent(f"""
                - CrewAI Tutorial for Beginners: Learn How To Use Latest CrewAI Features
                - CrewAI Tutorial: Complete Crash Course for Beginners
                - How To Connect Local LLMs to CrewAI [Ollama, Llama2, Mistral]
                - How to Use CrewAI to Automate Your Workflow
                - CrewAI Tutorial: How to Build a Digital Workforce
                ...                
                """),
        )

    def create_youtube_video_description(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Create a description for a given YouTube video topic and description.     
                Video Topic: {video_topic}
                Video Details: {video_details}
                """),
            agent=agent,
            expected_output=dedent(f"""
                🤖 Download the CrewAI Source Code Here:
                https://brandonhancock.io/crewai-updated-tutorial-hierarchical 
                                   
                Don't forget to Like and Subscribe if you're a fan of free source code 😉
                                   
                Want to join a community of AI developers? Join the AI Developer Accelerator Skook Community for FREE:
                https://www.skool.com/ai-developers-9308

                Ready to lead an AI revolution? Watch and learn how to build your own CrewAI from the ground up using the latest CrewAI features, and get set to deploy an army of AI agents at your command. This video is your ultimate guide to creating a powerful digital workforce, enhancing your projects with intelligent automation and streamlined workflows. Discover the secrets to customizing AI agents, setting them on tasks, and managing a smooth operation with CrewAI. It’s time to amplify your tech capabilities, and after this tutorial, you'll be equipped to engineer an AI crew that transforms any complex challenge into a simple task. Start your journey to AI mastery with CrewAI today!

                📰 Stay updated with my latest projects and insights:
                LinkedIn: https://www.linkedin.com/in/brandon-hancock-ai/
                Twitter: https://twitter.com/bhancock_ai

                Resources:
                [LEAVE BLANK]
                                   
                Timestamps: 
                [LEAVE BLANK]
            """),
        )

    def create_email_announcement_for_new_video(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Create an email to send to an email list to promote the new YouTube video.
                               
                Video Topic: {video_topic}
                Video Details: {video_details}

                Here are a few previous email announcements that you can use as inspiration. 
                
                Important Notes:
                - Make sure to copy my style, tone, and voice when writing the email.
                - Create a draft email. Once you have created a draft email, you MUST have a human review your tenative final email.

                Email 1:
                ----------------
                Subject: New CrewAI Tutorial: Learn How To Use the Latest CrewAI Features

                Hey [FIRST NAME GOES HERE]!

                Exciting update: CrewAI's new version is here, making it quicker and more dependable!

                You loved our first CrewAI tutorial, so I just published a new one for you.

                In this tutorial, you'll get up to speed with CrewAI's new features. We'll then apply these updates by building an AI Newsletter, demonstrating how to use what you've learned in a real project.

                video preview​
                Here's what's in store:

                Learn to manage a team with CrewAI's new Hierarchical workflow.
                Discover how asynchronous tasks can boost your efficiency.
                Find out how the Expected Output feature ensures accuracy and reliability.
                Plus, lots more insights!
                Dive into the tutorial to explore CrewAI's enhanced functions:

                video preview​
                Questions or want to share how you're doing? Email me or comment on YouTube.

                Happy coding!

                Cheers, 
                Brandon Hancock
                ----------------


                Email 2:
                ----------------
                Subject: New CrewAI + Ollama Tutorial: Learn How To Run CrewAI for Free

                Hey [FIRST NAME GOES HERE]!

                You asked, and I delivered! 🚀

                After posting my latest CrewAI tutorial, the 2 biggest questions flooding my inbox have been:

                How do I connect CrewAI with LLMs like Llama 2 and Mistral?
                How can I run CrewAI for free?
                Since it would be wrong to leave you hanging, I just published a new step-by-step YouTube tutorial for you to answer these questions!

                [VIDEO PREVIEW HERE]

                This tutorial shows you how to connect CrewAI with LLMs running on your own machine, which let's you run CrewAI completely for free!

                🎥 New Tutorial Alert: Connect CrewAI with Llama 2 & Mistral for Free!

                In this step-by-step guide for beginners, I'm pumped to walk you through the process of connecting CrewAI to locally running LLMs on your machine. Whether you're working with Llama 2, Mistral, or another LLM, I've got you covered. This tutorial is your golden ticket to running your crew at no cost!

                Here's a sneak peek of what you'll learn:

                Understanding CrewAI, Ollama, Llama 2, and Mistral: Dive into the basics of these powerful tools and their potential to revolutionize your projects.
                Step-by-Step Integration: Follow my detailed instructions to seamlessly connect CrewAI with Llama 2 or Mistral.
                Run Your Crew for Free: Yes, you read that right! I'll show you how to leverage these technologies without dipping into your wallet.
                I can't wait for you to check out the tutorial and start experimenting with CrewAI, Ollama, Llama 2, and Mistral. Your feedback and questions are what fuel this community, so don't hesitate to drop a comment on the video or shoot me an email with your thoughts and experiences.

                [VIDEO PREVIEW HERE]

                Once again, you can check out the latest video here:

                Happy coding, and here's to many more innovative projects ahead!

                Cheers,
                Brandon Hancock
                ----------------
                """),
            agent=agent,
            expected_output=dedent(f"""
                An email that contains a subject and body that is formatted exactly like the example email provided to you earlier.
            """)
        )
