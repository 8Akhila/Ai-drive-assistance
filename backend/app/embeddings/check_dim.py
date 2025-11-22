from sentence_transformers import SentenceTransformer

model = SentenceTransformer("./local_model")
print("Embedding dimension:", model.get_sentence_embedding_dimension())
