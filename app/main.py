import curses
from enum import auto
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
from . import models, schemas, utils
from sqlalchemy import select
from .database import engine, get_db
from sqlalchemy.orm import Session
from .router import post,user, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)



my_posts = [{"title": "a", "content":"b", "id":1},{"title": "c", "content":"d", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

#url/docs gives swagger ui api documentation


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


#app - @ decorator to fastapi instance to function imported then call http method then function definition
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def tests_posts(db: Session = Depends(get_db)):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

#sqlalchemy is an orm- a abstraction layer so you dont need to talk in sql and can use python code to directly create tables and access etc
