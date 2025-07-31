from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from datetime import datetime
import json
import base64

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
    return JSONResponse(
        content={"Posts": serialized_stored_posts()},
        status_code=201
    )
    
@app.get("/posts")
def list_posts():
    return JSONResponse(
        content={"Posts": serialized_stored_posts()},
        status_code=200
    )

@app.put("/posts")
def modify_post(posts: List[PostModel]):
    for post in posts:
        index = -1
        for i, existing_post in enumerate(posts_list):
            if existing_post.title == post.title:
                index = i
                break
        if index == -1:
            posts_list.append(post)
        else:
            posts_list[index] = post
    return JSONResponse(
        content={"Posts": serialized_stored_posts()},
        status_code=200
    )
    
@app.get("/ping/auth")
def read_ping_with_auth(request: Request):
    valid_username = "admin"
    valid_password = "123456"
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return JSONResponse(
            content={"message": "Authorization header is missing"},
            status_code=401
        )
    auth_type, credentials = authorization_header.split(" ")
    decoded_credentials = base64.b64decode(credentials.encode('utf-8')).decode('utf-8')
    username, password = decoded_credentials.split(':')
    if username != valid_username or password != valid_password:
        return JSONResponse(
            content={"message": "unauthorized Ressource"},
            status_code=401
        )
    elif username == valid_username and password == valid_password:
        return Response(content="pong", media_type="text/plain", status_code=200)
    
@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open ("404.html" , "r" , encoding="utf-8") as file:
        html_content = file.read()
    return Response(
        content=html_content,
        status_code=404,
        media_type="text/html"
    )