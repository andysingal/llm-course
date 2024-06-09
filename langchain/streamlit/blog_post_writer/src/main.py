import os
import re
import bs4
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
        
class BlogPostCreator:
    def __init__(self, keyword, web_references):
            self.keyword = keyword
            self.web_references = web_references

    def parse_links(self, search_results: str):
            print("-----------------------------------")
            print("Parsing links ...")
            return re.findall(r'link:\s*(https?://[^\],\s]+)', search_results)

    def save_file(self, content: str, filename: str):
            print("-----------------------------------")
            print("Saving file in blogs ...")
            directory = "blogs"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f" 🥳 File saved as {filepath}")

    def get_links(self):
            try:
                print("-----------------------------------")
                print("Getting links ...")

                wrapper = DuckDuckGoSearchAPIWrapper(max_results=self.web_references)
                search = DuckDuckGoSearchResults(api_wrapper=wrapper)
                results = search.run(tool_input=self.keyword)

                links = []
                for link in self.parse_links(results):
                    links.append(link)

                return links

            except Exception as e:
                print(f"An error occurred while getting links: {e}")

    def create_blog_post(self):
            try:
                print("-----------------------------------")
                print("Creating blog post ...")

                # Define self and docs variables
                self = BlogPostCreator(keyword=self.keyword, web_references=self.web_references)
                docs = []

                # Define splitter variable
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=2000,
                    chunk_overlap=400,
                    add_start_index=True,
                )

                # Load documents
                bs4_strainer = bs4.SoupStrainer(('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'))

                document_loader = WebBaseLoader(
                    web_path=(self.get_links())
                )

                docs = document_loader.load()

                # Split documents
                splits = splitter.split_documents(docs)

                # step 3: Indexing and vector storage
                vector_store = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

                # step 4: retrieval
                retriever = vector_store.as_retriever(search_type="similarity", search_kwards={"k": 10})

                # step 5 : Generation
                llm = ChatOpenAI()

                template = """
                    Given the following information, generate a blog post                   
                    Write a full blog post that will rank for the following keywords: {keyword}                 
                    
                    Instructions:
                    The blog should be properly and beautifully formatted using markdown.
                    The blog title should be SEO optimized.
                    The blog title, should be crafted with the keyword in mind and should be catchy and engaging. But not overly expressive.
                    Generate a title that is concise and direct. Avoid using introductory phrases like 'Exploring' or 'Discover'. For example:

                    Incorrect: 'Exploring Gulu: 10 Best Things to Do in Gulu'

                    Correct: '10 Best Things to Do in Gulu'

                    Incorrect: 'Who is Jordan Mungujakisa: Exploring the Mind of a Mobile App Alchemist'

                    Correct: 'The story of Jordan Mungujakisa'

                    Please provide titles in the correct format.

                    Do not include : in the title.

                    

                    Each sub-section should have at least 3 paragraphs.

                    

                    Each section should have at least three subsections.

                    

                    Sub-section headings should be clearly marked.

                    

                    Clearly indicate the title, headings, and sub-headings using markdown.

                    Each section should cover the specific aspects as outlined.

                    For each section, generate detailed content that aligns with the provided subtopics. Ensure that the content is informative and covers the key points.

                    Ensure that the content is consistent with the title and subtopics. Do not mention an entity in the title and not write about it in the content.

                    Ensure that the content flows logically from one section to another, maintaining coherence and readability.

                    Where applicable, include examples, case studies, or insights that can provide a deeper understanding of the topic.

                    Always include discussions on ethical considerations, especially in sections dealing with data privacy, bias, and responsible use. Only add this where it is applicable.

                    In the final section, provide a forward-looking perspective on the topic and a conclusion.

                    

                    Please ensure proper and standard markdown formatting always.

                    

                    Make the blog post sound as human and as engaging as possible, add real world examples and make it as informative as possible.

                    

                    You are a professional blog post writer and SEO expert.

                    Each blog post should have atleast 5 sections with 3 sub-sections each.

                    Each sub section should have atleast 3 paragraphs.

                    

                    Context: {context}

                    

                    Blog Post: 
                
                """

                prompt = PromptTemplate.from_template(template=template)

                def format_docs(docs):
                    return "\n\n".join(doc.page_content for doc in docs)

                chain = (
                    {"context": retriever | format_docs, "keyword": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                )
                
                return chain.invoke(input=self.keyword)

            except Exception as e:
                return e