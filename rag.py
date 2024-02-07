import os
import PyPDF2
from PyPDF2 import PdfReader

# Importing necessary modules from langchain and langchain_openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.callbacks import get_openai_callback
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Insert your OpenAI API key here
OPENAI_KEY = "YOUR_OPENAI_API_KEY_HERE"

def chunk_processing(pdf):
    """
    Process a PDF file, extracting text and splitting it into chunks.
    """
    pdf_reader = PdfReader(pdf)
        
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)
    return chunks
 
def embeddings(chunks):
    """
    Create embeddings for text chunks using OpenAI.
    """
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    # Create vector store using FAISS
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

def generation(VectorStore):
    """
    Generate responses based on prompts and embeddings.
    """
    retriever = VectorStore.as_retriever()
    
    # Define template for prompts
    template = """Respond to the prompt based on the following context: {context}
    Questions: {questions}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize ChatOpenAI model
    model = ChatOpenAI(openai_api_key=OPENAI_KEY)
    
    # Define processing chain
    chain = (
        {"context": retriever, "questions": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    # Prompt user for input
    query = input("Insert Prompt: ")
    
    # Invoke the processing chain with user input
    output = chain.invoke(query)
    return output
