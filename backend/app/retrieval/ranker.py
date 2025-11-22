def score_chunk(chunk: dict, query: str) -> float:
    """
    Scores a chunk based on how well it matches the user's query.
    This improves retrieval quality after FAISS.
    """

    text = chunk["text"].lower()                # Convert chunk text to lowercase
    query = query.lower()                       # Convert query to lowercase

    score = 0

    # Boost score if query words appear in chunk text
    for word in query.split():
        if word in text:
            score += 1                           # Add point for each matching word

    # Bonus: longer chunks often contain more meaningful info
    score += len(text) / 500                    # Normalize length contribution

    return score                                 # Final score for ranking


def rerank_chunks(chunks: list[dict], query: str) -> list[dict]:
    """
    Reranks chunks based on score to improve final LLM context quality.
    """

    # Add a "rank_score" key to each chunk
    for chunk in chunks:
        chunk["rank_score"] = score_chunk(chunk, query)  # Compute score

    # Sort chunks highest-score first
    sorted_chunks = sorted(chunks, key=lambda c: c["rank_score"], reverse=True)

    return sorted_chunks                                # Best chunks appear first
