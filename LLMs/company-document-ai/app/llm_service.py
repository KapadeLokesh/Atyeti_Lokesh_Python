import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)
def ask_llm(question: str, context: str = "") -> str:
    fallback = "Sorry, I couldn't generate a response."

    if client is None:
        return fallback

    # Build the prompt based on whether context is available
    if context.strip():
        system_prompt = """
You are an AI assistant for company documents.

Answer ONLY using the provided document context.
If the answer is not present in the context, reply exactly:
"I couldn't find that information in the uploaded documents."

Answer naturally in 1–3 concise sentences.
"""

        user_prompt = f"""
Context:
{context}

Question:
{question}
"""
    else:
        system_prompt = """
You are a knowledgeable and friendly AI assistant.

Answer naturally and clearly.
- Be concise for simple questions.
- Give detailed explanations when appropriate.
- Use examples if they help.
- If you don't know the answer, say so instead of making something up.
"""

        user_prompt = question

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        answer = response.choices[0].message.content
        return answer.strip() if answer else fallback

    except Exception:
        return fallback