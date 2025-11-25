from fastapi import FastAPI
from .routers import router

app = FastAPI(title="Lead Distribution CRM")
app.include_router(router=router)

@app.get("/")
def read_root():
    return {"message": "Lead Distribution CRM API"}