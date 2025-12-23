from langchain_openai import OpenAIEmbeddings
import numpy as np

def consine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

embed_model = OpenAIEmbeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    base_url="http://localhost:1234/v1",
    api_key="dummy-token",
    check_embedding_ctx_length=False
)

sentences = [
    "I love football.",
    "Soccar is my favorite sports.",
    "Messi talks spanish."
]

embeddings = embed_model.embed_documents(sentences)

for embed_vect in embeddings:
    print("Len:", len(embed_vect), " -->", embed_vect[:4])

print("Sentence 1 & 2 similarity:", consine_similarity(embeddings[0], embeddings[1]))
print("Sentence 1 & 3 similarity:", consine_similarity(embeddings[0], embeddings[2]))