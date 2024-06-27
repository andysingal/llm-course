from textwrap import dedent
from crewai import Task



class MeetingPrepTask():
    
    def research_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description = dedent(f"""\
                Conduct comprehensive reasearch on each of the individuals and companies
                involve in the upcoming meeting. Gather information on recent
                news, achievements, professional background, and any relevent
                business activities.
                
                Participants: {meeting_participants}
                Meeting Context: {meeting_context}"""),
            expected_output = dedent(f"""\
                A detailed report summarizing key findings about each participant and company, highlighting information
                that could be relevant for the meeting."""),
            agent = agent,
            async_execution=True
        )

    def industry_analysis_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description = dedent(f"""\
                Analyze the current industry trends, challenges, and opportunities
                relevan to the meeting's context. Consider market reports, recent
                developments, and expert opinions to provide a ccomprehensive overview of the industry landscape.
                
                Participants: {meeting_participants}
                Meeting Context: {meeting_context}"""),
            expected_output = dedent(f"""\
                An insightful analysis that identifies major trends, potential
                challenges, and strategic cpportunities."""),
            agent = agent,
            async_execution=True
        )

    def meeting_strategy_task(self, agent, meeting_context, meeting_objective):
        
        return Task(
            description = dedent(f"""\
                Develop strategic talking points, questions, and discussion angles
                for the meeting based on the research and industry analysis conducted.
                
                Meeting Context: {meeting_context}
                Meeting Objective: {meeting_objective}"""),
            expected_output = dedent(f"""\
                Complete report with a list of key talking points, strategic questions
                to ask to help achieve the meetings objective during the meeting."""),
            agent = agent
        )

    def summary_and_briefing_task(self, agent, meeting_context, meeting_objective):
        return Task(
            description = dedent(f"""\
                Compile all the research findings, industry analysis, and strategic
                talking points into a concise, comprehensive briefing document for the meeting.
                Ensure the briefing is easy to digest and equips the meeting
                participants with all necessary information and strategies.
                
                Meeting Context: {meeting_context}
                Meeting Objective: {meeting_objective}"""),
            expected_output = dedent(f"""\
                A well-structured briefing document that includes seactions for participants bios, industry overview, talking points and strategic recommendations."""),
            agent = agent
        )





