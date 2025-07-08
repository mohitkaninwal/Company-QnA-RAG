import os
from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
INDEX_NAME = "company-2"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "llama3-70b-8192"

DOCS_DIR = "./company_docs"
ALLOWED_EXT = ["pdf", "docx", "txt", "csv"]
EMBEDDING_DIM = 384  # for MiniLM-L6-v2
MAX_INPUT_TOKENS = 512  # model limit (words, not tokens, for simplicity)
CHUNK_SIZE = 350
CHUNK_OVERLAP = 75
