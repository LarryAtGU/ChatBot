import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI
import os

# get apikey
key = os.getenv("OPENAI_API_KEY")

# Upload PDF files

st.header("My First Chatbot")

with st.sidebar:
    st.title("Documents")
    file = st.file_uploader("Upload a PDF file and start to ask questions", type="pdf")

#Extract the text
if file is not None:
    pdf_reader = PdfReader(file)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        # st.write(text)    

#Break it into chunks
    
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    # st.write(chunks)


#Generate embedding
    embeddings = OpenAIEmbeddings(openai_api_key=key)


#Create vector store - FAISS
    vector_store = FAISS.from_texts(chunks,embeddings)

# - embedding (OpenAI)
# - initizling FAISS
# - store chunks & embeddings.
    
# get user question
    question = st.text_input("Type your question...")

# do similarity search
    
    if question:
        matches = vector_store.similarity_search(question)
        # st.write(matches)

# output results
# chain -> take the question -> retrieve relevant document -> pass to LLM -> generate answer.
        
#define llm
        llm = ChatOpenAI(
            openai_api_key=key,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-4o"
        )

        chain = load_qa_chain(llm, chain_type="stuff")
        result = chain.run(input_documents = matches, question = question)
        st.write(result)