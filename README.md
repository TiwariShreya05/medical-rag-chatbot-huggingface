<<<<<<< HEAD
\# Medical RAG Chatbot



A RAG (Retrieval Augmented Generation) chatbot that answers

medical questions using uploaded medical textbooks.



\## Tech stack

\- Python 3.14

\- Google Gemini API (LLM + embeddings)

\- Qdrant (vector database, local)

\- Gradio (chat UI)

\- PyMuPDF (PDF reading)



\## How it works

1\. Medical PDFs are chunked and embedded using Gemini

2\. Embeddings stored in local Qdrant vector DB

3\. User question is embedded and matched to top 5 chunks

4\. Gemini generates answer using only retrieved context



\## Setup

1\. Clone this repo

2\. Create venv and install: pip install -r requirements.txt

3\. Add your Gemini API key to .env file

4\. Add PDF books to books/ folder

5\. Run: python ingest.py

6\. Run: python app.py

=======
# medical-rag-chatbot
>>>>>>> 70623bbc13e412d66743bb453f6e0acb6d2b5e63
