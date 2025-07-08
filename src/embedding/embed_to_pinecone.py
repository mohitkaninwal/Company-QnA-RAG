import os
import hashlib
from glob import glob
from uuid import uuid4
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config import PINECONE_API_KEY,INDEX_NAME,EMBEDDING_DIM,MAX_INPUT_TOKENS,EMBEDDING_MODEL,ALLOWED_EXT,DOCS_DIR,CHUNK_OVERLAP,CHUNK_SIZE
from src.embedding.setup_pinecone import pc
from src.documentLoader.docLoader import file_hash,get_loader,truncate_text,chunk_hash
load_dotenv()

# ========== MAIN FUNCTION ==========
def embed_all_files():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    index = pc.Index(INDEX_NAME)

    # Load all files with allowed extensions
    all_files = []
    for ext in ALLOWED_EXT:
        all_files += glob(os.path.join(DOCS_DIR, f"*.{ext}"))

    new_vectors = []
    for filepath in all_files:
        filename = os.path.basename(filepath)
        ftype = filename.split('.')[-1].lower()
        if ftype not in ALLOWED_EXT:
            continue
        fhash = file_hash(filepath)
        loader_cls = get_loader(ftype)
        try:
            # Use correct loader constructor for CSV
            if ftype == "csv":
                docs = loader_cls(filepath, encoding='utf-8').load()
            else:
                docs = loader_cls(filepath).load()
        except Exception as e:
            print(f"Could not load {filename}: {e}")
            continue

        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_documents(docs)

        for i, chunk in enumerate(chunks):
            chunk_text = chunk.page_content.strip()
            chunk_text = truncate_text(chunk_text, MAX_INPUT_TOKENS)
            c_hash = chunk_hash(chunk_text + str(fhash) + str(i))
            # DEBUG print for sanity check
            print(f"Embedding chunk {i} of {filename}: {chunk_text[:70].replace('\n',' ')}...")

            meta = {
                "source_file": filename,
                "file_hash": fhash,
                "file_type": ftype,
                "chunk_index": i,
                "chunk_hash": c_hash,
                "page_content": chunk_text,   # THIS IS THE CRITICAL LINE!
            }
            new_vectors.append({
                "id": str(uuid4()),
                "values": embeddings.embed_query(chunk_text),
                "metadata": meta,
            })

    # Batch upsert
    BATCH_SIZE = 100
    print(f"Upserting {len(new_vectors)} new vectors to Pinecone...")
    for i in range(0, len(new_vectors), BATCH_SIZE):
        batch = new_vectors[i:i + BATCH_SIZE]
        pinecone_vectors = [(vec['id'], vec['values'], vec['metadata']) for vec in batch]
        index.upsert(vectors=pinecone_vectors)
        print(f"Upserted {i + len(batch)}/{len(new_vectors)} vectors...")

    print("All eligible documents embedded and stored in Pinecone!")

if __name__ == "__main__":
    embed_all_files()
 