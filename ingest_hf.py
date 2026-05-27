import fitz
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os, uuid

db = QdrantClient(path="./qdrant_data_hf")
COLLECTION = "medical_books_hf"
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Model loaded!")

if not db.collection_exists(COLLECTION):
    db.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

already_done = set()
results = db.scroll(collection_name=COLLECTION, limit=10000)
for point in results[0]:
    if "source" in point.payload:
        already_done.add(point.payload["source"])

if already_done:
    print(f"Already embedded: {already_done}")

def chunk_text(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size])
            for i in range(0, len(words), chunk_size)]

for pdf_file in os.listdir("books"):
    if not pdf_file.endswith(".pdf"):
        continue
    if pdf_file in already_done:
        print(f"Skipping {pdf_file} — already embedded")
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
        vector = model.encode(chunk).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": chunk, "source": pdf_file}
        ))
        if (i+1) % 50 == 0:
            print(f"  embedded {i+1}/{len(chunks)}")
            db.upsert(collection_name=COLLECTION, points=points)
            points = []

    if points:
        db.upsert(collection_name=COLLECTION, points=points)
    print(f"Done: {pdf_file}")

print("All books loaded!")