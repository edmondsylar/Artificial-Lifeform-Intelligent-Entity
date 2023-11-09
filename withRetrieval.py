from langchain.chains.router import MultiRetrievalQAChain
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
import pathlib
import os
import openai
from dotenv import load_dotenv


load_dotenv()
# get key from .env file
key = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = key
# openai.api_key = key

class CustomTextLoader(TextLoader):
    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            raise RuntimeError(f"Error loading {self.file_path}") from e
        return self.split_into_documents(text)


# get /Memory/GeneralKnowledge.txt location 
path = pathlib.Path(__file__).parent.absolute()
docpath = str(path) + "\GeneralKnowledge.txt"

# creat the GK Loader and retriever
GK_docs = TextLoader(docpath, encoding="utf-8").load_and_split()
Gkretriever = FAISS.from_documents(GK_docs, OpenAIEmbeddings()).as_retriever()

# get he contacts.txt location
path = pathlib.Path(__file__).parent.absolute()
contactspath = str(path) + "/Memory/contacts.txt"

