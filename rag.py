from google import genai
from qdrant_client import QdrantClient
import os, time
from dotenv import load_dotenv

load_dotenv() 
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
db = QdrantClient(path="./qdrant_data")
COLLECTION = "medical_books"

def embed_query(text):
    time.sleep(1)
    result = client_ai.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def answer(question):
    vector = embed_query(question)
    results = db.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=5
    ).points
    context = "\n---\n".join([r.payload["text"] for r in results])
    prompt = f"""You are a helpful medical assistant.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't have enough information on that."
Always remind the user to consult a real doctor for medical advice.

Context:
{context}

Question: {question}
Answer:"""

    response = client_ai.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text
