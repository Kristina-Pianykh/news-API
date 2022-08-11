import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .articles import router as articles_router

app = FastAPI()

app.include_router(articles_router)


class InvalidIdError(HTTPException):
    def __init__(self, id: str):
        self.id = id


@app.exception_handler(InvalidIdError)
async def invalid_id_exception_handler(request: Request, exc: InvalidIdError):
    return JSONResponse(
        status_code=404, content={"message": "Invalid article id: {exc.id}"}
    )


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
