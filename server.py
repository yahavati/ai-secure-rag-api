import os
from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI, Depends, HTTPException, status,File,UploadFile
from pydantic import BaseModel, Field
from typing import Annotated
from ai_docs_rag import ask_ai
from ai_docs_rag import add_document
from ai_test_gen import generate_tests
from auth import get_current_user
from ai_security import is_malicious_query
from database import SessionLocal
from models import Users
from auth import router as auth_router
from models import Base
from database import engine
from file_utiles import convert_to_text
from pii_utils import mask_pii




app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
user_dependency=Annotated[dict,Depends(get_current_user)]

class CodeRequest(BaseModel):
    code: str

class QuestionRequest(BaseModel):
    username: str
    question: str


@app.post("/generate-tests")
def generate_tests_api(
    req: CodeRequest,
    user: user_dependency
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    return {"tests": generate_tests(req.code)}

class AddDocRequest(BaseModel):
    username: str
    content: str

from fastapi import UploadFile, File

@app.post("/add-doc")
async def add_doc(
    user: user_dependency,
    username: str,
    file: UploadFile = File(...)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    # Read file bytes
    file_bytes = await file.read()

    # Convert file → text
    try:
        text = convert_to_text(file.filename, file_bytes)
        text = mask_pii(text)  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    add_document(username, text)
    print("TEXT AFTER MASKING:")
    print(text)
    return {"message": "Document saved successfully!"}


@app.post("/ask-docs")
def ask_docs_api(
    req: QuestionRequest,
    user: user_dependency
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
        
    answer = ask_ai(req.username,req.question)
    return {"answer": answer}
