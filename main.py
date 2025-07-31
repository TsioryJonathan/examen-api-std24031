from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from starlette.requests import Request

app = FastAPI()

@app.get("/")
def root():
    return JSONResponse(content={"message": "Hello, World!"}, status_code=200)

class User(BaseModel):
    name:str
    age:int

users_list: List[User] = []

def serialized_stored_user():
    users_converted = []
    for user in users_list:
        users_converted.append(user.model_dump())
    return users_converted

@app.post("/user")
def postUser(user: User, request: Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    return JSONResponse({"User": user.model_dump()}, status_code=200)
