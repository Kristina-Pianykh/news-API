from fastapi import FastAPI

from .articles import router as articles_router

app = FastAPI()

app.include_router(articles_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
