from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

def generate_response(query, retrieved_chunks):
    """Generate a grounded answer from retrieved chunks."""
    if not retrieved_chunks:
        return {
            "answer": "I couldn't find anything relevant in the loaded documents. Try rephrasing your question.",
            "sources": []
        }

    # Format context block
    context = ""
    for chunk in retrieved_chunks:
        context += f"[Source: {chunk['professor']}]\n{chunk['text']}\n\n"

    # Build programmatic source list (not left to LLM)
    sources = list(dict.fromkeys([chunk['professor'] for chunk in retrieved_chunks]))

    messages = [
        {
            "role": "system",
            "content": (
                "You are a university guide assistant. Answer the user's question using ONLY "
                "the context provided below. Do not use any outside knowledge. "
                "If the answer is not found in the context, say clearly: "
                "'I don't have enough information on that in the loaded documents.' "
                "Always indicate which professor or source your answer refers to."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\nQuestion: {query}"
        }
    ]

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }