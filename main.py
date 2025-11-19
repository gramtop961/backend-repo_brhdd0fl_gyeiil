from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import create_document, get_documents, db
from schemas import ContactInquiry
import os

app = FastAPI(title="Law Firm API")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running", "service": "law-firm"}

@app.get("/test")
def test_db():
    try:
        collections = []
        if db is not None:
            collections = db.list_collection_names()
        return {
            "backend": "ok",
            "database": "mongo",
            "database_url": os.getenv("DATABASE_URL", "unset"),
            "database_name": os.getenv("DATABASE_NAME", "unset"),
            "connection_status": "connected" if db is not None else "unavailable",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "ok", "database": "error", "error": str(e)}

@app.post("/contact")
def contact(inquiry: ContactInquiry):
    try:
        doc_id = create_document("contactinquiry", inquiry)
        return {"status": "received", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
