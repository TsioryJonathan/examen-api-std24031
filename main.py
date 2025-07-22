from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel

from starlette.requests import Request

app = FastAPI()

@app.get("/")
def root():
    return JSONResponse(content={"message": "Hello, World!"}, status_code=200)

class User(BaseModel):
    name: str
    age: int

@app.post("/user")
def getUser(user: User, request: Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    return JSONResponse({"User": user.model_dump()}, status_code=200)
