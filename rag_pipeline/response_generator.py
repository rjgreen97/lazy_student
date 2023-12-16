import os
from pathlib import Path
from dotenv import load_dotenv
import nest_asyncio
import openai
import llama_index
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, StorageContext
from llama_index.llms import OpenAI
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine

load_dotenv()
nest_asyncio.apply()
openai.api_key = os.environ["OPENAI_API_KEY"]

class ResponseGenerator:
    def __init__(self, model_name: str, temperature: float = 0.0, whitepaper_kb_dir: str = "knowledge_stores"):
        self.model_name = model_name
        self.whitepaper_kb_dir = whitepaper_kb_dir
        self.llm = OpenAI(temperature=temperature, model=self.model_name)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.whitepaper_kb = self._build_or_load_kb(self.whitepaper_kb_dir)
        self.sq_query_engine = self._build_subquestion_engine()
        self.base_prompt = """
            You are an expert in machine learning, artificial intelligence, and computer science. \
            Your goal is to help students learn about a specific whitepaper, with a focus on the machine learning concepts. \
            You will be provided with a single whitepaper that you will help the students understand. \
            Please construct a response that is educational and deconstructs complicated ideas so they are easy to understand. \
            Your response aims to educate. \
            When possible, please provide examples to help students understand the concepts. \
        """

    def generate_response(self, question: str):
        prompt = self.base_prompt + question
        response = self.sq_query_engine.query(prompt)
        return response

    def run_conversation(self):
        while True:
            print("===================================================================")
            question = input("Enter your question (type 'Exit' to end conversation): ")
            
            if question.lower() == 'exit':
                print("Hope you learned something!")
                break
            response = self.generate_response(question)

    def _build_kb(self, kb_dir: str):
        docs = SimpleDirectoryReader(input_dir=kb_dir).load_data()
        index = VectorStoreIndex.from_documents(docs, verbose=False)
        return index

    def _build_or_load_kb(self, kb_dir: str):
        persist_dir = Path(kb_dir) / Path("index")
        if not os.path.exists(persist_dir):
            index = self._build_kb(kb_dir)
            index.storage_context.persist(persist_dir=persist_dir)
        else:
            index = llama_index.load_index_from_storage(
                StorageContext.from_defaults(persist_dir=persist_dir),
                service_context=self.service_context,
            )
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
        return SubQuestionQueryEngine.from_defaults(query_engine_tools=self.query_engine_tools)

if __name__ == "__main__":
    response_generator = ResponseGenerator(
        model_name="gpt-3.5-turbo",
        temperature=0.0,
        whitepaper_kb_dir="knowledge_stores",
    )
    response_generator.run_conversation()
