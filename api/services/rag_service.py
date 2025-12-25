from vectorstore.pinecone_client import query_vector
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")


def ask_parker(question: str) -> dict:
    """
    RAG pipeline: Query Pinecone, build context, call Gemini, return answer + sources.

    Args:
        question: User's fashion/style question

    Returns:
        dict with 'answer' (str) and 'sources' (list of dicts)
    """
    # 1. Retrieve relevant chunks from Pinecone
    vectordbresponse = query_vector(question, top_k=3)

    # 2. Extract text for context and metadata for citations
    context_parts = []
    sources = []

    for match in vectordbresponse.matches:
        metadata = match.metadata

        # Add text to context
        context_parts.append(metadata["text"])

        # Build source citation
        sources.append(
            {
                "title": metadata["title"],
                "url": f"https://www.youtube.com/watch?v={metadata['video_id']}&t={metadata['start_time']}s",
                "score": round(match.score, 2),
            }
        )

    # 3. Combine context chunks into one string
    context_str = "\n\n---\n\n".join(context_parts)

    # 4. Build the prompt for Gemini
    prompt = f"""You are a fashion AI assistant inspired by Parker York Smith, a content creator known for practical, approachable style advice.

Your goal: Help users look their best with simple, actionable tips.

Tone:
- Warm and encouraging
- Practical, not pretentious
- Use phrases like "Start with a neutral base" or "Fit is everything"

Context from Parker's videos:
{context_str}

User Question: {question}

Answer the question based on the context above. If the context doesn't fully answer it, give general fashion principles."""

    # 5. Call Gemini
    response = model.generate_content(prompt)

    # 6. Return structured response
    return {"answer": response.text.strip(), "sources": sources}


if __name__ == "__main__":
    # Test the function
    result = ask_parker("what is movie theater style fashion")
    print("ANSWER:")
    print(result["answer"])
    print("\nSOURCES:")
    for source in result["sources"]:
        print(f"- {source['title']} ({source['score']})")
        print(f"  {source['url']}")
