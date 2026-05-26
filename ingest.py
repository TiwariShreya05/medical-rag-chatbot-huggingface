import fitz
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os, uuid, time
from dotenv import load_dotenv

load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
db = QdrantClient(path="./qdrant_data")

COLLECTION = "medical_books"

if not db.collection_exists(COLLECTION):
    db.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
    )

def chunk_text(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size])
            for i in range(0, len(words), chunk_size)]

def embed(text, retries=5):
    for attempt in range(retries):
        try:
            time.sleep(2)
            result = client_ai.models.embed_content(
                model="models/gemini-embedding-001",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            if "429" in str(e):
                wait = 60 * (attempt + 1)
                print(f"  Rate limit hit. Waiting {wait} seconds...")
                time.sleep(wait)
            else:
                raise e
    raise Exception("Failed after retries")

for pdf_file in os.listdir("books"):
    if not pdf_file.endswith(".pdf"):
        continue
    print(f"Processing {pdf_file}...")
    doc = fitz.open(f"books/{pdf_file}")
    full_text = " ".join(page.get_text() for page in doc)
    chunks = chunk_text(full_text)
    print(f"  {len(chunks)} chunks found")

    points = []
    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 50:
            continue
        vector = embed(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": chunk, "source": pdf_file}
        ))
        if (i+1) % 10 == 0:
            print(f"  embedded {i+1}/{len(chunks)}")
            db.upsert(collection_name=COLLECTION, points=points)
            points = []

    if points:
        db.upsert(collection_name=COLLECTION, points=points)
    print(f"Done: {pdf_file}")

print("All books loaded!")