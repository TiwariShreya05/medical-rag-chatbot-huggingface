# Medical RAG Chatbot — HuggingFace + Llama 3

Version 2 of the medical RAG chatbot. Unlike Version 1 which 
uses Google Gemini for everything, this version uses:

- HuggingFace sentence-transformers for embeddings (runs locally)
- Llama 3 via Groq API for answering (free, fast)
- No rate limits on embeddings
- More private — embeddings never leave your machine

## Key files
- ingest_hf.py — loads books using HuggingFace embeddings
- rag_hf.py — retrieves and answers using Llama 3
- app_hf.py — Gradio chat UI on port 7861

## Version 1
github.com/TiwariShreya05/medical-rag-chatbot
