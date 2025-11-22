from sentence_transformers import SentenceTransformer

print("Downloading embedding model...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model.save("./local_model")

print("Model downloaded and saved in local_model/")
