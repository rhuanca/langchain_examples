from __future__ import annotations

import os
import re
from typing import List, Tuple

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Small in-memory knowledge base for demonstration.
DOCUMENTS = [
    "Bolivia is a landlocked country in central South America. Sucre is the constitutional capital, while La Paz is the seat of government.",
    "The Salar de Uyuni in Bolivia is the world's largest salt flat and contains major lithium reserves.",
    "Bolivia recognizes Spanish and many Indigenous languages, including Aymara, Quechua, and Guarani.",
    "Bolivia's economy includes natural gas, mining, agriculture, and services, with Santa Cruz as an economic hub.",
    "Lake Titicaca lies on the border of Bolivia and Peru and is one of the highest navigable lakes in the world.",
]


def llm_call(message: str) -> str:
    """Call the chat model with a plain string prompt."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is not set. Retrieval worked, but LLM generation is skipped."

    base_model = ChatOpenAI(model="gpt-5", temperature=0.1)
    result = base_model.invoke(message)
    return result.content


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def retrieve_documents(query: str, k: int = 3) -> List[str]:
    """Retrieve top-k docs with a simple keyword-overlap scoring."""
    query_terms = _tokenize(query)

    scored: List[Tuple[int, str]] = []
    for doc in DOCUMENTS:
        score = len(query_terms & _tokenize(doc))
        scored.append((score, doc))

    scored.sort(key=lambda item: item[0], reverse=True)

    # Keep docs that matched at least one term; fall back to first k docs otherwise.
    matched_docs = [doc for score, doc in scored if score > 0]
    return matched_docs[:k] if matched_docs else DOCUMENTS[:k]


def rag_chain(query: str) -> str:
    # Step 1: Retrieve relevant context
    context_docs = retrieve_documents(query)
    context = "\n".join(f"- {doc}" for doc in context_docs)

    # Step 2: Generate answer with context
    prompt = (
        "Answer based on context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "If the context is insufficient, say what is missing."
    )
    answer = llm_call(prompt)
    return answer


if __name__ == "__main__":
    question = "What are Bolivia's capitals and what is Salar de Uyuni known for?"
    print("Question:", question)
    print("\nRetrieved context:")
    for idx, doc in enumerate(retrieve_documents(question), start=1):
        print(f"{idx}. {doc}")

    print("\nRAG answer:\n")
    print(rag_chain(question))
