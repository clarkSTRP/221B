from fastapi import FastAPI
from routes import router

app = FastAPI(title="Sherlock Web (Host)")
app.include_router(router)

#uvicorn main:app --reload --port 8000