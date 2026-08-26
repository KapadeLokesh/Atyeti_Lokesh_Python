import os
import logging

from dotenv import load_dotenv
from groq import Groq


logger = logging.getLogger(__name__)


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


if GROQ_API_KEY:

    client = Groq(
        api_key=GROQ_API_KEY
    )

else:

    client = None

    logger.warning(
        "GROQ_API_KEY is not configured."
    )


def ask_llm(
    question: str,
    context: str = "",
    tabular: bool = False,
) -> str:
    """
    Generate an answer using Groq.

    Parameters
    ----------
    question:
        User's natural-language question.

    context:
        Retrieved context from either the PDF
        or tabular RAG pipeline.

    tabular:
        When True, use a structured-data prompt
        suitable for CSV/Excel retrieval.

    Returns
    -------
    str
        Generated answer.
    """

    fallback = (
        "Sorry, I couldn't generate a response."
    )

    if client is None:

        logger.error(
            "Groq client is not configured."
        )

        return fallback

    if not question or not question.strip():

        return (
            "Please provide a valid question."
        )

    # ==========================================================
    # TABULAR PROMPT
    # ==========================================================

    if tabular:

        system_prompt = """
You are an AI assistant for a company CSV/Excel
intelligent search system.

You are given structured rows retrieved from a
company dataset.

Answer the user's question ONLY using the
provided dataset context.

IMPORTANT RULES:

1. Treat the context as authoritative structured data.

2. Look carefully at column names and values.

3. Answer questions about:
   - names
   - roles
   - projects
   - skills
   - departments
   - cities
   - emails
   - and other fields present in the rows.

4. Do not invent information.

5. Do not make assumptions that are not supported
   by the retrieved rows.

6. If the answer is present in the context,
   answer directly.

7. If the answer is not present in the context,
   reply exactly:

"I couldn't find that information in the uploaded dataset."

8. Be concise and natural.

9. Do not mention embeddings, ChromaDB, tokens,
   retrieval, or internal implementation details.

10. Never expose encoded/tokenized values to the user.

Answer in 1–3 concise sentences.
"""

        user_prompt = f"""
Dataset context:

{context}

Question:

{question}
"""

    # ==========================================================
    # EXISTING PDF PROMPT
    # ==========================================================

    else:

        if context.strip():

            system_prompt = """
You are an AI assistant for company documents.

Answer ONLY using the provided document context.

If the answer is not present in the context,
reply exactly:

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
- If you don't know the answer, say so instead
  of making something up.
"""

            user_prompt = question

    # ==========================================================
    # GROQ REQUEST
    # ==========================================================

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.1,
            max_tokens=500,
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        if not answer:

            return fallback

        return answer.strip()

    except Exception as exc:

        logger.exception(
            "Groq LLM request failed: %s",
            exc,
        )

        return fallback