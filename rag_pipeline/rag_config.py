from pydantic import BaseModel, Field, PositiveFloat


class RagConfig(BaseModel):
    base_prompt: str = Field(
        default="""
            You are an expert in machine learning, artificial intelligence, and computer science. \
            Your goal is to help the reader learn about a specific whitepaper, with a focus on the machine learning concepts. \
            You will be provided with a single whitepaper that you will help the students understand. \
            Please construct a response that is educational and deconstructs complicated ideas so they are easy to understand. \
            Your response aims to educate, and it is very important that you provide detailed answers. \
            Your response should be consice and easy to understand. \
            Your response should focus on the core concepts of the whitepaper. \
        """,
        description="Base prompt for the OpenAI API.",
    )
    model_name: str = Field(
        default="gpt-3.5-turbo",
        description="Name of the OpenAI model to use.",
    )
    temperature: PositiveFloat = Field(
        default=0.0,
        description="Temperature parameter for OpenAI API.",
    )
    whitepaper_kb_dir: str = Field(
        default="knowledge_store",
        description="Directory containing the whitepaper.",
    )
