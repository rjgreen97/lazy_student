import streamlit as st
import os
import shutil
from src.response_generator import ResponseGenerator
from src.rag_config import RagConfig

rag_config = RagConfig()
response_generator = ResponseGenerator(rag_config)
st.title("Lazy Student")

def find_pdf_files(directory):
    for _, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                return file

target_directory = "knowledge_store"
filename = find_pdf_files(target_directory)

filename_placeholder = st.empty()

if os.listdir(target_directory):
    filename_placeholder.write(f"Reference Document: **{filename}**")
else:
    filename_placeholder.write("There is currently no document uploaded.")

uploaded_file = st.file_uploader("Upload a file:", type=["pdf"])

if uploaded_file:
    if os.listdir(target_directory):
        shutil.rmtree(target_directory)
        os.makedirs(target_directory)

    file_path = os.path.join(target_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    filename = uploaded_file.name
    filename_placeholder.write(f"Reference Document: **{filename}**")

user_input = st.text_input("Enter your question:")
if st.button('Ask'):
    response = response_generator.generate_response(user_input)
    st.text_area("Answer", value=response, height=300)
