from dotenv import load_dotenv
from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    VectorStoreIndex,
)
from llama_index.llms import OpenAI
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from pathlib import Path
import nest_asyncio
import openai
import os
import shutil

from src.rag_config import RagConfig

load_dotenv()
nest_asyncio.apply()
openai.api_key = os.environ["OPENAI_API_KEY"]


class ResponseGenerator:
    def __init__(self, rag_config: RagConfig):
        self.model_name = rag_config.model_name
        self.whitepaper_kb_dir = rag_config.whitepaper_kb_dir
        self.llm = OpenAI(temperature=rag_config.temperature, model=self.model_name)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.whitepaper_kb = self._build_or_load_kb(self.whitepaper_kb_dir)
        self.sq_query_engine = self._build_subquestion_engine()
        self.base_prompt = rag_config.base_prompt

    def generate_response(self, question: str):
        prompt = self.base_prompt + question
        response = self.sq_query_engine.query(prompt)
        return response

    def run_conversation(self):
        while True:
            print("========================================================")
            question = input("Enter your question (type 'Exit' to end conversation): ")

            if question.lower() == "exit":
                print("Hope you learned something!")
                break
            response = self.generate_response(question)
            print(f"\n{response}\n")

    def _build_kb(self, kb_dir: str):
        docs = SimpleDirectoryReader(input_dir=kb_dir).load_data()
        index = VectorStoreIndex.from_documents(docs, verbose=False)
        return index

    def _clear_existing_kb(self, persist_dir: Path):
        if os.path.exists(persist_dir):
            for file_name in os.listdir(persist_dir):
                file_path = os.path.join(persist_dir, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    def _build_or_load_kb(self, kb_dir: str):
        persist_dir = Path(kb_dir) / Path("index")
        self._clear_existing_kb(persist_dir)
        index = self._build_kb(kb_dir)
        index.storage_context.persist(persist_dir=persist_dir)
        return index

    def _build_subquestion_engine(self):
        whitepaper_engine = self.whitepaper_kb.as_query_engine()
        self.query_engine_tools = [
            QueryEngineTool(
                query_engine=whitepaper_engine,
                metadata=ToolMetadata(
                    name="Whitepaper",
                    description="Provides information and explanations about the whitepaper.",
                ),
            ),
        ]
        return SubQuestionQueryEngine.from_defaults(
            query_engine_tools=self.query_engine_tools, verbose=False
        )


if __name__ == "__main__":
    rag_config = RagConfig()
    response_generator = ResponseGenerator(rag_config)
    response_generator.run_conversation()
