from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.db import engine, SessionLocal
from backend.models import Base, Document
from backend.embedding import get_embedding, cosine_similarity

import json

app = FastAPI()

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


def save_document(filename: str, content: str, embedding):
    db = SessionLocal()
    embedding_str = json.dumps(embedding)

    doc = Document(
        filename=filename,
        content=content,
        embedding=embedding_str
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)
    db.close()
    return doc


# ✅ Upload API
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    text = text[:500]

    embedding = get_embedding(text)

    doc = save_document(file.filename, text, embedding)

    return {
        "message": "File uploaded successfully",
        "doc_id": doc.id,
        "filename": doc.filename,
        "embedding_length": len(embedding)
    }


# ✅ Get all documents
@app.get("/documents/")
def get_documents():
    db = SessionLocal()
    docs = db.query(Document).all()
    db.close()

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "content": d.content
        }
        for d in docs
    ]


# ✅ Search API
@app.get("/search/")
def search(query: str):
    db = SessionLocal()
    docs = db.query(Document).all()

    query = query[:200]

    try:
        query_embedding = get_embedding(query)
    except Exception as e:
        db.close()
        return {"error": str(e)}

    results = []

    for doc in docs:
        if not doc.embedding:
            continue

        try:
            # Split content into sentences (simple split)
            sentences = doc.content.split(".")

            best_sentence = ""
            best_score = -1

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                sent_emb = get_embedding(sentence)
                score = cosine_similarity(query_embedding, sent_emb)

                if score > best_score:
                    best_score = score
                    best_sentence = sentence

            results.append({
                "filename": doc.filename,
                "score": round(best_score, 3),
                "relevant_text": best_sentence  # ✅ only best part
            })

        except Exception as e:
            print("Error:", e)

    db.close()

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:3]