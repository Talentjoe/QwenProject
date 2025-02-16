import ollama
import numpy as np

emb1 = ollama.embed(model='nomic-embed-text:latest',input="C++")
emb1_np = np.array(emb1['embeddings'])

emb2 = ollama.embed(model='nomic-embed-text:latest',input="C")
emb2_np = np.array(emb2['embeddings'])

emb3 = ollama.embed(model='nomic-embed-text:latest',input="C#")
emb3_np = np.array(emb3['embeddings'])

print( np.linalg.norm(emb1_np - emb2_np))
print( np.linalg.norm(emb2_np - emb3_np))
print( np.linalg.norm(emb1_np - emb3_np))
