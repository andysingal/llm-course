from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.embeddings.sentence_transformer import ( SentenceTransformerEmbeddings )
from langchain_community.vectorstores.chroma import Chroma

prompt_template = """
### [INST] 
Instruction: Answer the question based on your 
art of war knowledge. Here is context to help:

{context}

### QUESTION:
{question} 

[/INST]
 """

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

rag_prompt = hub.pull('rlm/rag-prompt')

llm = Ollama(model='llama2')

llm_chain = load_qa_chain(llm=llm, chain_type='stuff', verbose=True)

def get_documents(file):
  loader = TextLoader(file, encoding='utf-8')
  return loader.load()

def create_chunks(documents):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
  chunks = text_splitter.split_documents(documents)
  return chunks

def extract_page_content(chunks):
  pages = []
  for chunk in chunks:
    pages.append(chunk.page_content)
  return pages

def get_embedding_function():
  embedding_function = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')
  return embedding_function
 
def insert_embeddings(docs, embedding_function):
  db = Chroma.from_documents(docs, embedding_function, persist_directory='./chromadb')
  db.persist()
  return db

def get_data(db, query):
  retriever = db.as_retriever()
  return retriever

def send_prompt_llm(results, query):
  return llm_chain.invoke(input_documents=results, question=query)

def main():
  documents = get_documents('./art_of_war.txt')
  chunks = create_chunks(documents)
  embedding_function = get_embedding_function()
  db = insert_embeddings(chunks, embedding_function)
  query = 'What are the most important war technics?'
  retriever = get_data(db, query)
  rag_chain = { 'context': retriever, 'question': RunnablePassthrough()} | rag_prompt | llm
  response = rag_chain.invoke(query)
  # response = send_prompt_llm(results, query)
  print(response)

if __name__ == "__main__":
    main()