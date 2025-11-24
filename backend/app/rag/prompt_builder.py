# backend/app/rag/prompt_builder.py

from typing import List, Dict

def build_prompt(chunks: List[Dict], question: str, mode: str = "default", max_chars: int = 4000) -> str:
    """
    Builds a clean RAG prompt:
    - Reads FAISS metadata chunks (file_name, snippet…)
    - Supports "default" (answer question) and "summary" (merge all info)
    """

    # -------------------------
    # 1. Select model behavior
    # -------------------------
    if mode == "summary":
        system_msg = (
            "You are a summarization assistant. Combine ALL context into one clean summary. "
            "Do NOT add anything that is not in the context."
        )
    else:
        system_msg = (
            "You are a helpful assistant. Only use the given context to answer the question. "
            "If answer is missing, reply: 'I don't know'."
        )

    # -------------------------
    # 2. Build context blocks
    # -------------------------
    blocks = []
    used_chars = 0

    for i, chunk in enumerate(chunks, start=1):
        file_name = chunk.get("file_name", "unknown_file")
        snippet = chunk.get("snippet", "")

        safe = snippet if len(snippet) <= 2000 else snippet[:2000] + " ... (truncated)"
        block = f"[{i}] {file_name}\n{safe}\n"

        if used_chars + len(block) > max_chars:
            break

        blocks.append(block)
        used_chars += len(block)

    context_section = "\n---\n".join(blocks)

    # -------------------------
    # 3. Final prompt
    # -------------------------
    prompt = (
        f"{system_msg}\n\n"
        f"Context:\n{context_section}\n\n"
        f"User request: {question}\n\n"
        f"Answer:"
    )

    return prompt
