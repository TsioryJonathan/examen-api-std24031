from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from datetime import datetime
import json

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

class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime
    
posts_list: List[PostModel] = []

def serialized_stored_posts():
    posts_converted = []
    for post in posts_list:
        to_append = {
            "author": post.author,
            "title": post.title,
            "content": post.content,
            "creation_datetime": post.creation_datetime.isoformat()
        }
        posts_converted.append(to_append)
    return posts_converted

@app.post("/posts")
def create_post(posts: List[PostModel]):
    for post in posts:
        posts_list.append(post)
    return Response(
        content=json.dumps({"Posts": serialized_stored_posts()}),
        status_code=201,
        media_type="application/json"
    )


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open ("404.html" , "r" , encoding="utf-8") as file:
        html_content = file.read()
    return Response(
        content=html_content,
        status_code=404,
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
