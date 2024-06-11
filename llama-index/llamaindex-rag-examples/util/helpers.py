import fandom
import os
import wikipedia
import python_weather

from fandom import FandomPage
from wikipedia import WikipediaPage
from mdutils.mdutils import MdUtils
from pydantic import Field

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.schema import NodeWithScore 
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

async def get_weather(city: str = Field("A city name")) -> str:
    """Useful for getting todays weather forecast for a given city."""
    async with python_weather.Client() as client:
        weather = await client.get(location=city, locale=python_weather.Locale.DANISH)
        
        day = next(iter(weather.daily_forecasts))
        forecast = [f'{str(hourly.time)}: {hourly.temperature}°C, Rain: {hourly.chances_of_rain}%, Cloud cover: {hourly.cloud_cover}%' for hourly in day.hourly_forecasts]
        return f'On {day.date}, {weather.location} will have a high of {day.highest_temperature}°C and a low of {day.lowest_temperature}°C. The forecast is:{chr(10)}{chr(10)}{f"{chr(10)}".join(forecast)}'


def get_wiki_pages(articles=[]) -> list[WikipediaPage]:
    """
    Retrieves Wikipedia pages for the given list of articles.

    Args:
        articles (list): A list of article titles.

    Returns:
        list: A list of WikipediaPage objects representing the retrieved pages.
    """
    return [wikipedia.page(article) for article in articles]


def get_malazan_pages(articles=["Anomander Rake", "Tayschrenn", "Kurald Galain", "Warrens", "Tattersail", "Whiskeyjack", "Kruppe"]) -> list[FandomPage]:
    """
    Retrieves FandomPage objects for the specified articles from the Malazan wiki.

    Args:
        articles (list[str], optional): A list of article names to retrieve. Defaults to ["Anomander Rake", "Tayschrenn", "Kurald Galain"].

    Returns:
        list[FandomPage]: A list of FandomPage objects corresponding to the specified articles.
    """
    fandom.set_wiki("malazan")
    pages = [fandom.page(article) for article in articles]
    return pages


def get_theoffice_pages() -> list[FandomPage]:
    """
    Retrieves FandomPage objects for the specified articles from the Malazan wiki.

    Args:
        articles (list[str], optional): A list of article names to retrieve. Defaults to ["Anomander Rake", "Tayschrenn", "Kurald Galain"].

    Returns:
        list[FandomPage]: A list of FandomPage objects corresponding to the specified articles.
    """
    articles = [
    "Michael Scott",
    "Dwight Schrute",
    "Jim Halpert",
    "Pam Beesly",
    "Ryan Howard",
    "Andy Bernard",
    "Angela Martin",
    "Kelly Kapoor",
    "Toby Flenderson",
    "Creed Bratton",
    "Darryl Philbin",
    "Kevin Malone",
    "Meredith Palmer",
    "Oscar Martinez",
    "Phyllis Vance",
    "Stanley Hudson"
]
    fandom.set_wiki("theoffice")
    pages = [fandom.page(article) for article in articles]
    return pages


def get_office_pages() -> list[FandomPage]:
    """
    Retrieves FandomPage objects for the specified articles from the Malazan wiki.

    Args:
        articles (list[str], optional): A list of article names to retrieve. Defaults to ["Anomander Rake", "Tayschrenn", "Kurald Galain"].

    Returns:
        list[FandomPage]: A list of FandomPage objects corresponding to the specified articles.
    """
    articles = [
    "Michael Scott",
    "Dwight Schrute",
    "Jim Halpert",
    "Pam Beesly",
    "Ryan Howard",
    "Andy Bernard",
    "Angela Martin",
    "Kelly Kapoor",
    "Toby Flenderson",
    "Creed Bratton",
    "Darryl Philbin",
    "Kevin Malone",
    "Meredith Palmer",
    "Oscar Martinez",
    "Phyllis Vance",
    "Stanley Hudson"
]
    fandom.set_wiki("theoffice")
    pages = [fandom.page(article) for article in articles]
    return pages


def get_friends_pages() -> list[FandomPage]:
    """
    Retrieves FandomPage objects for the specified articles from the Malazan wiki.

    Args:
        articles (list[str], optional): A list of article names to retrieve. Defaults to ["Anomander Rake", "Tayschrenn", "Kurald Galain"].

    Returns:
        list[FandomPage]: A list of FandomPage objects corresponding to the specified articles.
    """
    articles = [
    "Ross Geller",
    "Chandler Bing"
    ]
    
    fandom.set_wiki("friends")
    pages = [fandom.page(article) for article in articles]
    return pages
    
def create_and_save_wiki_md_files(pages: list[WikipediaPage], path="./data/docs/"):
    """
    Creates and saves Markdown files for a list of Wikipedia pages.

    Args:
        pages (list[WikipediaPage]): A list of WikipediaPage objects representing the pages to be saved.
        path (str, optional): The path where the Markdown files will be saved. Defaults to "./data/docs/".

    Returns:
        None
    """
    if not os.path.exists(path):
        print("Creating directory: ", path)
        os.makedirs(path)

    for page in pages:
        print(page)
        create_and_save_wiki_md_file(page, path)


def create_and_save_wiki_md_file(page: WikipediaPage, path="./data/docs/"):
    """
    Create and save a Markdown file from a WikipediaPage object.

    Args:
        page (WikipediaPage): The WikipediaPage object containing the page information.
        path (str, optional): The path where the Markdown file will be saved. Defaults to "./data/docs/".
    """
    title: str = page.title
    filename = os.path.join(
        "", f"{path}{ title.lower().replace(' ', '-') }.md")
    mdFile = MdUtils(file_name=filename, title=title)
    mdFile.new_header(level=1, title="Summary")
    mdFile.new_paragraph(page.summary)
    mdFile.new_line()
    mdFile.new_header(level=1, title=title)
    mdFile.new_paragraph(page.content
                         .replace("\n====", "###")
                         .replace("====", "")
                         .replace("\n===", "##")
                         .replace("===", "")
                         .replace("\n==", "#")
                         .replace("==", ""))
    mdFile.create_md_file()


def create_and_save_md_files(pages: list[FandomPage], path="./data/docs/"):
    """
    Create Markdown files based on the given page objects.

    Args:
        pages (list[FandomPage]): A list of page objects containing the content to be written to the Markdown files.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)

    for page in pages:
        create_and_save_md_file(page, path)


def create_and_save_md_file(page: FandomPage, path="./data/docs/"):
    """
    Create a Markdown file based on the given page object.

    Args:
        page (Page): The page object containing the content to be written to the Markdown file.

    Returns:
        None
    """
    title: str = page.content["title"]
    filename = os.path.join(
        "", f"{path}{ title.lower().replace(' ', '-') }.md")
    mdFile = MdUtils(file_name=filename, title=title)
    mdFile.new_header(level=1, title="Summary")
    mdFile.new_paragraph(page.summary)
    mdFile.new_line()
    mdFile.new_header(level=1, title=title)
    mdFile.new_paragraph(page.content["content"])
    mdFile.new_line()
    sections = page.content["sections"]
    for section in sections:
        mdFile.new_header(level=2, title=section["title"])
        mdFile.new_paragraph(section["content"])
        mdFile.new_line()
    mdFile.create_md_file()



def generate_vector_index(docs_path="./data/docs", chunk_size=512) -> VectorStoreIndex:
    """
    Generates a vector store index from a collection of documents.

    Args:
        docs_path (str): The path to the directory containing the documents. Defaults to "./data/docs".
        chunk_size (int): The size of each chunk for sentence splitting. Defaults to 512.

    Returns:
        VectorStoreIndex: The generated vector store index.
    """
    documents = SimpleDirectoryReader(docs_path).load_data()
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",
        embed_batch_size=256
    )

    splitter = SentenceSplitter(chunk_size=chunk_size)
    index = VectorStoreIndex.from_documents(
        documents, transformations=[splitter], embed_model=embed_model
    )
    return index

def pretty_print_node(node: NodeWithScore):
    print(str(node))
    print("Size: ", len(node.text))
    print("Full text: ")
    print("---------------------------")
    print(str(node.text))
    print("---------------------------")