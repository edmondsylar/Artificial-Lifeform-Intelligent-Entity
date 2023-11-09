import os 
import getpass
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

os.environ['OPENAI_API_KEY'] = ""


# get the general knowledge file from the current directory.
current_directory = os.path.dirname(os.path.abspath(__file__))
general_knowledge_file = os.path.join(current_directory, 'GeneralKnowledge.txt')



# Load the document, split it into chunks, embed each chunk and load it into the vector store.
raw_documents = TextLoader(general_knowledge_file, encoding="UTF-8").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = FAISS.from_documents(documents, OpenAIEmbeddings())


query = "What is my current location ?"
docs = db.similarity_search(query)
print(docs[0].page_content)