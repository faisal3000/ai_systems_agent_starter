import faiss, numpy as np

class SimpleVectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.texts = []

    def add(self, embeddings, text):
        self.index.add(np.asarray([embeddings]).astype("float32"))
        self.texts.append(text)

    def search(self, embedding, k=5):
        D, I = self.index.search(np.asarray([embedding]).astype("float32"), k)
        return [(self.texts[i], float(D[0][idx])) for idx, i in enumerate(I[0]) if i != -1]
