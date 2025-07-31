from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import List
from starlette.requests import Request

app = FastAPI()

@app.get("/ping")
def read_ping():
    return Response(content="pong", media_type="text/plain",status_code=200)

@app.get("/home")
def read_home():
    with open("home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(
        content=html_content,
        status_code=200,
        media_type="text/html"
    )
# class User(BaseModel):
#     name:str
#     age:int

# users_list: List[User] = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

# def serialized_stored_user():
#     users_converted = []
#     for user in users_list:
#         users_converted.append(user.model_dump())
#     return users_converted

# @app.post("/user")
# def postUser(user: User, request: Request):
#     accept_headers = request.headers.get("Accept")
#     if accept_headers != "text/plain":
#         return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
#     return JSONResponse({"User": user.model_dump()}, status_code=200)
