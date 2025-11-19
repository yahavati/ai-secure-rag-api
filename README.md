This project is an AI-powered Document Question-Answering system that uses a FastAPI backend combined with JWT-based authentication to ensure secure user access. Uploaded documents (PDF, Word, or TXT) are processed and converted into clean text, followed by automatic PII masking to remove sensitive information. The cleaned text is embedded using OpenAI’s text-embedding-3-small model and stored in ChromaDB, a vector database that enables efficient semantic search. When a user submits a question, the system performs Retrieval-Augmented Generation (RAG) by semantically matching the question to the user’s own documents, retrieving the most relevant content, and generating an answer using GPT-4o-mini strictly based on the retrieved context

Features:

Secure Authentication:
JWT-based login
Tokens store: username, user ID, role, expiration
Every route validates authentication
Access control ensures users only access their own documents

Document Upload System:
Accepts PDF, Word, and TXT
Converts files into clean text
Removes personal data via PII masking
Generates embeddings using text-embedding-3-small
Stores text + embeddings inside ChromaDB
Metadata contains the username → ensures isolation of users

Semantic Search (RAG):
User asks a question
System embeds the question
ChromaDB retrieves the most relevant document belonging to the same user
AI responds based only on the document

PII Masking:
Automatically removes:
Email addresses
Phone numbers
ID numbers
Credit card numbers

Dates

This prevents leaking sensitive user information to the LLM.

