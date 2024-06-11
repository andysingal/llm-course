from pydantic import BaseModel, Field
from anthropic import Anthropic
from anthropic.types import Usage
from dotenv import load_dotenv
import polars as pl
import instructor

load_dotenv()


class PainService(BaseModel):
    pain_point: str
    service_offering: str


class Relevance(BaseModel):
    pain_relevance_score: int = Field(
        ...,
        description="Score between 0 and 5 of the relevance of pain point and service offering to the original job posting.",
    )
    pain_relevance_score_explanation: str
    service_offering_relevance_score: int = Field(
        ...,
        description="Score between 0 and 5 of the relevance of the service offering to the original job posting and the pain point.",
    )
    service_offering_relevance_score_explanation: str


client = instructor.from_anthropic(Anthropic())

d = open("./data/upwork.txt").read()

prompt = """
    Given a posting from a job listing website, identify the pain point of the job lister and generate the service offering from a professional that would alleviate that pain.
    The pain point and service offering should be concise, maximum of one sentence each.
    Generalize the service offering as much as possible.
    Output your answer in the structure and style of the examples. 


    Job Description:
    {job_description}

    Example Outputs:

    Service: Create a custom whiteboard animation explainer doodle video
    Pain Point: They want to leverage the engaging, explainer-style format of a whiteboard animation video to effectively communicate their ideas or showcase their products.

    Service: Find you a new job by searching and applying on your behalf
    Pain Point: Needs assistance with their job search, including identifying suitable opportunities and applying on their behalf, to secure a new role efficiently.

    Service: Do data analytics visualization power bi tableau dashboard
    Pain Point: Wants to leverage data analysis and visualization services to gain actionable insights from their raw data, leading to more informed decision-making for their business.

    Service: Do b2b lead generation database for targeted title person
    Pain Point: Needs a comprehensive, organized database of individuals categorized by their job titles or roles to streamline their data management and research efforts.

    Service: Cut cords of attachment with someone
    Pain Point: Seeks spiritual guidance and support to address emotional attachments and improve personal well-being.
    """.format(
    job_description=d
)


pain_service, raw = client.messages.create_with_completion(
    model="claude-3-haiku-20240307",
    messages=[{"role": "user", "content": prompt}],
    response_model=PainService,
    max_tokens=4000,
)

print(f"Pain Point: {pain_service.pain_point}")
print(f"Service Offering: {pain_service.service_offering}")


prompt_eval = """
    Given a posting from a job listing website, an identified pain point, and service offering, give a relevance score on for the pain point and service offering.
    Job Description:
    {job_description}
    Pain Point:
    {pain}
    Service Offering:
    {offering}
    """.format(
    job_description=d,
    pain=pain_service.pain_point,
    offering=pain_service.service_offering,
)

relevance, raw = client.messages.create_with_completion(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": prompt_eval}],
    response_model=Relevance,
    max_tokens=4000,
)

print("Job Posting")
print(f"{d}\n\n\n")
print(f"Pain Relevance Score: {relevance.pain_relevance_score}")
print(f"Pain Relevance Explanation: {relevance.pain_relevance_score_explanation}\n\n")
print(f"Service Offering Relevance Score: {relevance.service_offering_relevance_score}")
print(f"Service Offering Explanation: {relevance.service_offering_relevance_score_explanation}")
