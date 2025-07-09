# Company QnA RAG Assistant

This is an AI-powered Q&A Assistant built using Retrieval-Augmented Generation (RAG) to answer employee queries based on your company's internal documents like HR policies, SOPs, and employee handbooks — all in a professional HR tone.

---

## Features

- Natural language Q&A interface
- Accurate responses based on embedded company documents
- Answers tailored in a professional HR voice
- Web-based interface built with Streamlit
- Powered by Groq LLM for fast and reliable generation

---
## Sample Interface and Output

### User Interface
(![Screenshot 2025-07-10 002906](https://github.com/user-attachments/assets/5105dfa7-089f-49b1-9075-bd5beefac6ec)


### Query and Answer Example
(![Screenshot 2025-07-10 002958](https://github.com/user-attachments/assets/6ab36faa-97d1-460b-a80b-165a23b01f2d)



## Tech Stack

| Component            | Technology                                 |
|---------------------|--------------------------------------------|
| Embeddings          | `sentence-transformers` (Hugging Face)     |
| Vector Database     | [Pinecone](https://www.pinecone.io)        |
| Language Model      | [Groq API](https://console.groq.com/)      |
| Orchestration       | [LangChain](https://www.langchain.com/)    |
| UI                  | [Streamlit](https://streamlit.io)          |
| Environment Config  | `.env` with `python-dotenv` (optional)     |

---

## How It Works

1. **Document Preprocessing**  
   Company documents are read and chunked into meaningful sections.

2. **Embedding**  
   Each chunk is embedded using `sentence-transformers` and stored in Pinecone for fast similarity search.

3. **Query Handling**  
   When a user asks a question via the Streamlit interface:
   - The query is embedded
   - Relevant document chunks are retrieved from Pinecone using vector similarity

4. **Answer Generation**  
   LangChain uses the Groq API to generate a concise and accurate answer in a professional HR tone using the retrieved context.

---

## Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/mohitkaninwal/Company-QnA-RAG.git
cd Company-QnA-RAG
