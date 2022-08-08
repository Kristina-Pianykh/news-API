import uvicorn
from articles import router as articles_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(articles_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
