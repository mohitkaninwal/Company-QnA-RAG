import os
from pinecone import Pinecone
from config import PINECONE_API_KEY,EMBEDDING_MODEL,INDEX_NAME
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

def initialize_pinecone():
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        return pc
    except Exception as e:
        st.error(f"Failed to initialize Pinecone: {e}")
        return None

def initialize_vectorstore(pc):
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        index = pc.Index(INDEX_NAME)
        return PineconeVectorStore(index=index, embedding=embeddings, text_key='page_content')
    except Exception as e:
        st.error(f"Could not connect to Pinecone vectorstore: {e}")
        return None