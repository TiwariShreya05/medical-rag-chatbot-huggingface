from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
model = SentenceTransformer('all-MiniLM-L6-v2')
db = QdrantClient(path="./qdrant_data_hf")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
COLLECTION = "medical_books_hf"

def answer(question):
    vector = model.encode(question).tolist()
    results = db.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=5
    ).points
    context = "\n---\n".join([r.payload["text"] for r in results])
    prompt = f"""You are a helpful medical assistant.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't have enough information on that."
Always remind the user to consult a real doctor.

Context:
{context}

Question: {question}
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content