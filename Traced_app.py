import os

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "{question}"
)

model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment="gpt-4.1-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

chain = prompt | model | StrOutputParser()

questions = [
    "Explain LangSmith in one sentence.",
    "What is Retrieval Augmented Generation (RAG) in one sentence?",
    "Explain how LangChain, embeddings, vector databases and LLMs work together in an enterprise AI application.in one sentence"
]

for i, q in enumerate(questions, start=1):
    print(f"\n===== Run {i} =====")
    print(f"Question: {q}")

    response = chain.invoke({"question": q})

    print("Response:")
    print(response)
