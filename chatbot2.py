import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI
# from dotenv import load_dotenv
import os

# Load environment variables from .env file
# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process text into chunks
def split_text_into_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    return text_splitter.split_text(text)

# Initialize session state for storing the vector store and chunks
if 'vector_store' not in st.session_state:
    st.session_state['vector_store'] = None
    st.session_state['chunks'] = None
    st.session_state['qa_history'] = []
    st.session_state['key_counter'] = 0

# Streamlit App
st.header("My First Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")

# Extract and process text if file is uploaded
if file is not None:
    with st.spinner("Processing PDF..."):
        text = extract_text_from_pdf(file)
        chunks = split_text_into_chunks(text)
        st.session_state['chunks'] = chunks

        # Generating embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        # Creating vector store - FAISS
        vector_store = FAISS.from_texts(chunks, embeddings)
        st.session_state['vector_store'] = vector_store

# Function to handle the question
def handle_question(question):
    if question and st.session_state['vector_store'] is not None:
        with st.spinner("Searching for answers..."):
            match = st.session_state['vector_store'].similarity_search(question)

            # Define the LLM
            llm = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                temperature=0,
                max_tokens=1000,
                # model_name="gpt-3.5-turbo"，
                model_name="gpt-4o",
            )

            # Load QA chain and get response
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=match, question=question)
            return response

# Display the Q&A history
for i, (question, answer) in enumerate(st.session_state['qa_history']):
    st.write(f"**Q:** {question}")
    st.write(f"**A:** {answer}")

# Get user question and handle it
if st.session_state['vector_store'] is not None:
    key = st.session_state['key_counter']

    with st.form(key=f"question_form_{key}"):
        user_question = st.text_input("Type your question here", key=f"question_{key}")
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button:
        if user_question:
            answer = handle_question(user_question)
            if answer:
                st.session_state.qa_history.append((user_question, answer))
                # Increment the key counter to create a new input field
                st.session_state['key_counter'] += 1
                st.experimental_rerun()
