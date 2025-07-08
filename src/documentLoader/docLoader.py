# ========== HELPERS ==========
import hashlib
from config import MAX_INPUT_TOKENS
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader

def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def chunk_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def truncate_text(text, limit=MAX_INPUT_TOKENS):
    words = text.split()
    if len(words) > limit:
        return " ".join(words[:limit])
    return text

def get_loader(ext):
    return {
        "pdf": PyPDFLoader,
        "txt": TextLoader,
        "docx": Docx2txtLoader,
        "csv": CSVLoader,
    }[ext]