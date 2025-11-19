import chromadb
import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv
import hmac, hashlib

load_dotenv()

client = OpenAI()


chroma = chromadb.Client()


#making a secret key
SECRET = os.getenv("SECRET")

def make_doc_id(username: str, content: str) -> str:
    msg = (username + "|" + content).encode("utf-8")
    return hmac.new(SECRET.encode("utf-8"), msg, hashlib.sha256).hexdigest()

# coding the text to vector
def embed_text(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

#add a document to the chroma
def add_document(username: str, text: str):
    collection = chroma.get_or_create_collection("docs")

    doc_id = make_doc_id(username, text)

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embed_text(text)],
        metadatas=[{"username": username}]
    )

    return {"status": "ok", "doc_id": doc_id}


def ask_ai(username: str, question: str):
    collection = chroma.get_or_create_collection("docs")

    q_emb = embed_text(question)

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=1,
        where={"username": username},  
        include=["documents"]  #take all the documents accroding to the query
    )

    if not results["documents"] or not results["documents"][0]:
        return "No matching documents found for this user."

    context = results["documents"][0][0]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "Answer ONLY based on the document context and NEVER reveal any personal data (PII)."

            },
            {
                "role": "assistant",
                "content": f"Documentation:\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content
