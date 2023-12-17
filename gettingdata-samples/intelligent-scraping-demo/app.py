import os
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.chat_models import AzureChatOpenAI
import json
from time import sleep
import requests
from bs4 import BeautifulSoup
from html2text import HTML2Text
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain

load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_base = os.getenv("AZURE_OPENAI_BASE")

llm_gpt35 = AzureChatOpenAI(
    deployment_name="chat-gpt35",
    model="gpt-3.5-turbo-16k-0613",
    temperature=0,
    max_tokens=10000,
)

llm_gpt4 = AzureChatOpenAI(
    deployment_name="chat-gpt4", model="gpt-4", temperature=0, max_tokens=4000
)


def find_newsroom(company, num_results=1):
    """ "Given company, attempt to find their newsroom url"""

    search = GoogleSerperAPIWrapper(k=num_results)
    results = search.results(f"{company} Company Newsroom")
    link = results["organic"][0]["link"]
    print(f"Newsroom for {company}: {link}")
    return link


def scrape_links_from_site(company, url):
    """ "Given company newsroom url, find links to most salient articles"""

    # Scrape all links from the newsroom url
    print(f"finding links from {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    filtered_links = [
        i for i in links if (not i.startswith("//") and i.count("/") > 1)
    ][
        :50
    ]  # Limit links to 50 to stay within token limits

    # Define prompt for selecting top 3 from the list of URLs
    prompt = """
    In the below list of urls, select up to 3 that seem most likely to lead to an interesting news article about {company}.
    Ignore generic links like "https://www.intel.com/press" or "https://www.hubspot.com/careers", instead trying to select links like https://www.intc.com/news-events/press-releases/detail/1645/intel-to-sell-minority-stake-in-ims-nanofabrication that lead to specific articles.
    Ignore links that contain developer documentation or other guides. Only select links that look like news items.
    Your response should only include a comma-separated list of selected urls, in the format: url1,url2,url3.
    Include nothing else but the comma-separated list in your response. If you fail to find links, return 'None' 
    Links: 
    {links}
    """
    prompt_template = PromptTemplate(
        template=prompt, input_variables=["company", "links"]
    )

    # Use LLMChain with GPT4 to reduce hallucination
    if len(links) > 0:
        chain = LLMChain(llm=llm_gpt4, prompt=prompt_template, verbose=True)
        output = chain.run(company=company, links=", ".join(filtered_links))
        return output.strip().split(",")
    else:
        print(f"\nUnable to scrape links from website: {url}\n")
        return None


def scrape_articles(urls, base_url):
    """Scrape link of articles, and summarize each with gpt"""
    summaries = []
    # Loop through the given list of URLs
    for url in urls:
        url = url.strip()
        if url.startswith("/"):  # If relative url, then combine with newsroom
            url = base_url + url
        print(f"Scraping website {url}...")
        r = requests.get(url)
        if r.status_code == 200:
            # Convert HTML-results into text with HTML2Text
            h = HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            markdown = h.handle(r.text)

            # Summarize text and append it to list summaries
            output = summarize(markdown)
            summaries.append(f"{{'url': '{url}', 'content': '{output}'}}")
            sleep(10)  # Delay to avoid API rate limits
        else:
            print(f"HTTP request failed with {r.status_code}.")
    return summaries


def summarize(content):
    """Summarizes text content from a website"""

    # Define custom prompt for summarize-chain
    prompt = """Write a concise summary of the following: 
    "{text}". 
    Emphasize things that are news-worthy and surprising, leaving out points that are more generic.   
    CONCISE SUMMARY:"""
    prompt_template = PromptTemplate(template=prompt, input_variables=["text"])

    # Split content into chunks
    text_splitter = CharacterTextSplitter(chunk_size=6000)
    docs = text_splitter.create_documents([content])

    # Configure and run map-reduce chain
    chain = load_summarize_chain(
        llm=llm_gpt35,
        chain_type="map_reduce",
        map_prompt=prompt_template,
        combine_prompt=prompt_template,
        verbose=False,
    )
    results = chain.run(input_documents=docs)
    print(f"Summary: {results}\n")
    return results


def main(json_obj):
    """For given json of companies, find and summarize recent news for each company and write the results into new file"""

    new_clients = []
    for client in json_obj:
        name = client["companyName"]
        newsroom_url = find_newsroom(name)
        article_urls = scrape_links_from_site(name, newsroom_url)
        if len(article_urls) > 1:
            content = scrape_articles(article_urls, newsroom_url.rsplit("/", 1)[0])
        client["news"] = content
        new_clients.append(client)

    with open("data/clients_with_news.json", "w") as f:
        json.dump(new_clients, f, indent=4)


with open("data/clients.json", "r") as f:
    json_obj = json.load(f)
    main(json_obj=json_obj)
