import ollama
import numpy as np


def cosine_similarity(vec1, vec2, epsilon=1e-8):
    vec1 = vec1.squeeze()
    vec2 = vec2.squeeze()

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 < epsilon or norm2 < epsilon:
        return 0.0

    return np.dot(vec1, vec2) / (norm1 * norm2)


embModule = "qwen2.5:14b"

test_pairs = [
    ("珠穆朗玛峰", "世界最高峰"),
    ("珠穆朗玛峰", "喜马拉雅山"),
    ("珠穆朗玛峰", "苹果"),
    ("美丽", "丑陋"),
    ("apple", "苹果")
]

for word1, word2 in test_pairs:
    emb1 = ollama.embed(embModule, word1)
    emb2 = ollama.embed(embModule, word2)

    if emb1.embeddings is None or emb2.embeddings is None:
        print(f"Error embedding {word1} or {word2}")
    else:
        npArry1 = np.array(emb1.embeddings).squeeze()
        npArry2 = np.array(emb2.embeddings).squeeze()
        similarity = cosine_similarity(npArry1, npArry2)
        print(f"Cosine Similarity ({word1}, {word2}): {similarity:.4f}")
        print(f"欧几里得距离 ({word1}, {word2}): {np.linalg.norm(npArry2 - npArry1):.4f}")
