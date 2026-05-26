# Medical RAG Chatbot

A chatbot that answers medical questions using actual textbooks,
not the AI's general knowledge.

---

## What is RAG?

RAG (Retrieval Augmented Generation) forces the AI to answer
only from documents you provide — preventing hallucination.

---

## How it works

1. Medical PDFs are split into small chunks
2. Each chunk is converted to a vector using Gemini embeddings
3. Vectors are stored in a local Qdrant database
4. When you ask a question, the top 5 matching chunks are found
5. Gemini reads those chunks and generates a grounded answer

---

## Tech stack

| Component       | Tool                    |
|-----------------|-------------------------|
| LLM             | Google Gemini API       |
| Embeddings      | Gemini Embedding 001    |
| Vector database | Qdrant (local)          |
| PDF reading     | PyMuPDF                 |
| Chat UI         | Gradio                  |
| Language        | Python 3.14             |

---

## Setup

git clone https://github.com/TiwariShreya05/medical-rag-chatbot.git
cd medical-rag-chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Add your Gemini API key to a .env file:
GEMINI_API_KEY=your_key_here

Add PDF books to the books/ folder, then run:
python ingest.py
python app.py

Open browser at http://localhost:7860

---

## Example questions

- What is the function of the heart?
- What are symptoms of diabetes?
- How does the brain control movement?

---

Shreya Tiwari — 2026