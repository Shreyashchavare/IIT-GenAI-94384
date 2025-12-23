from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = [
    "I love football.",
    "Soccer is my favorite sports. ",
    "Messi talks spanish."
]

embeddings = embed_model.encode(sentences)

for embed_vect in embeddings:
    print("Len:", len(embed_vect), " -->", embed_vect[:4])

print("Sentence 1 & 2 similarity: ", cosine_similarity(embeddings[0], embeddings[1]))
print("Sentence 1 & 3 similarity: ", cosine_similarity(embeddings[0], embeddings[2]))