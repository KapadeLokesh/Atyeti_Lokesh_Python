from fastapi import FastAPI
from app.routers.chat import router as chat_router
from app.routers.documents import router as document_router
from app.routers.web_search import router as web_search_router

app = FastAPI(title="Company Document AI")
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(web_search_router)

@app.get("/")
def home():
    return {"message": "Company Document AI Assistant"}


