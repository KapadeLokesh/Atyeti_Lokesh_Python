import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

while True:
    question = input("\nAsk a question (type 'exit' to quit):")
    if question.lower() == "exit":
        break

    response = client.responses.create(
        model="llama-3.3-70b-versatile",
        input=question
    )
    print("\nAI:",response.output_text)