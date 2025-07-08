
import os
from pinecone import Pinecone,ServerlessSpec
from config import INDEX_NAME,EMBEDDING_DIM,PINECONE_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists (using proper Pinecone ServerlessSpec)
try:
    if INDEX_NAME not in [idx['name'] for idx in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
except Exception as e:
    print(f"Error (probably index already exists): {e}")