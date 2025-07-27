# indexer.py
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle

DATA_DIR   = Path(r"C:\Users\nchur\Documents\second-brain\$school")          # your PDF/MD folder
META_PATH  = "docs_metadata.pkl"
CHUNKS_KEY = "chunks"

# 1. Load + chunk
all_chunks = []
splitter   = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
for f in DATA_DIR.rglob("*.*"):     # .md, .pdf, etc.
    loader = TextLoader(str(f), autodetect_encoding=True)
    docs   = loader.load()
    for doc in docs:
        texts = splitter.split_text(doc.page_content)
        for i, t in enumerate(texts):
            all_chunks.append({
                "text":   t,
                "source": str(f),
                "idx":    i
            })

# 2. Persist metadata (we’ll add embeddings separately)
with open(META_PATH, "wb") as f:
    pickle.dump(all_chunks, f)
print(f"→ Prepared {len(all_chunks)} chunks")
