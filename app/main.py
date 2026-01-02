from fastapi import FastAPI
from app.api.v1.extract import router

app = FastAPI(title="Financial Extractor MVP")
app.include_router(router, prefix="/api/v1")
