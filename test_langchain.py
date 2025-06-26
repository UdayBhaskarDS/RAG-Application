import os
import dotenv
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import (
    WebBaseLoader, 
    PyPDFLoader, 
    Docx2txtLoader,
)
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
#from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

dotenv.load_dotenv()


# Load docs

doc_paths = [
    "docs/test_rag.pdf",
    "docs/test_rag.docx",
]

docs = [] 
for doc_file in doc_paths:
    file_path = Path(doc_file)

    try:
        if doc_file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif doc_file.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif doc_file.endswith(".txt") or doc_file.name.endswith(".md"):
            loader = TextLoader(file_path)
        else:
            print(f"Document type {doc_file.type} not supported.")
            continue

        docs.extend(loader.load())

    except Exception as e:
        print(f"Error loading document {doc_file.name}: {e}")


# Load URLs

url = "https://docs.streamlit.io/develop/quick-reference/release-notes"
try:
    loader = WebBaseLoader(url)
    docs.extend(loader.load())

except Exception as e:
    print(f"Error loading document from {url}: {e}")