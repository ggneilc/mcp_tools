# embedder.py
import pickle, numpy as np, faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMB_PATH   = "docs_index.faiss"

# 1. Load metadata
with open("docs_metadata.pkl", "rb") as f:
    chunks = pickle.load(f)

# 2. Compute embeddings
model  = SentenceTransformer(MODEL_NAME)
texts  = [c["text"] for c in chunks]
embs   = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# 3. Build FAISS index
dim    = embs.shape[1]
index  = faiss.IndexFlatIP(dim)   # inner-product for cosine if vectors are normalized
faiss.normalize_L2(embs)
index.add(embs)

# 4. Save index
faiss.write_index(index, EMB_PATH)
print("→ Saved FAISS index with", index.ntotal, "vectors")
