from fastapi import FastAPI, UploadFile, File
from db import engine, SessionLocal
from models import Base, Document
from embedding import get_embedding, cosine_similarity
import json

app = FastAPI()

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
            doc_embedding = json.loads(doc.embedding)
            score = cosine_similarity(query_embedding, doc_embedding)

            results.append({
                "filename": doc.filename,
                "score": round(score, 3)
            })
        except Exception as e:
            print("Error:", e)

    db.close()

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:3]