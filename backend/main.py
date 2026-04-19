from fastapi import FastAPI

app = FastAPI(title="AI Research Assistant API")

@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}