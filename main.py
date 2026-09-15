from fastapi import FastAPI
from routes.frontend import router as frontend_router

app = FastAPI()

app.include_router(frontend_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
