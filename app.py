import streamlit as st
import os
import shutil
from src.response_generator import ResponseGenerator
from src.rag_config import RagConfig

rag_config = RagConfig()
response_generator = ResponseGenerator(rag_config)
st.title("Lazy Student")

target_directory = "knowledge_store"

if os.listdir(target_directory):
    st.write("There is currently a whitepaper uploaded.")
else:
    st.write("There is currently no whitepaper uploaded.")

uploaded_file = st.file_uploader("Upload a file:", type=["pdf"])

if uploaded_file:
    if os.listdir(target_directory):
        st.write("Deleting existing files...")
        shutil.rmtree(target_directory)
        os.makedirs(target_directory)

    st.write("Adding the new file...")
    file_path = os.path.join(target_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

user_input = st.text_input("Enter your question:")
if st.button('Answer'):
    response = response_generator.generate_response(user_input)
    st.text_area("Answer", value=response, height=300)
