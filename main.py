from fastapi import FastAPI
from routes.frontend import router as frontend_router
from routes.backend import router as backend_router


app = FastAPI()

app.include_router(frontend_router)
app.include_router(backend_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
