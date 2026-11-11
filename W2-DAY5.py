# breakfast.py

import os
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment="gpt-4.1-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    temperature=0  # more consistent results across runs
)

prompt = """
Give exactly 5 healthy breakfast ideas.

Requirements:
- Numbered list
- One item per line
- No preamble
- No explanation
"""

response = llm.invoke(prompt)

# Print the whole AIMessage object first
print("=== Raw invoke() result ===")
print(response)

print("\n=== Only the text ===")
print(response.content)
