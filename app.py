import streamlit as st
from src.response_generator import ResponseGenerator
from src.rag_config import RagConfig

rag_config = RagConfig()
response_generator = ResponseGenerator(rag_config)
st.title("Lazy Student")

user_input = st.text_input("Enter your question:")

if st.button('Answer'):
    response = response_generator.generate_response(user_input)
    st.text_area("Answer", value=response, height=300)
