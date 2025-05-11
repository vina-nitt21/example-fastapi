import curses
from enum import auto
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. import models, schemas, utils, oauth2
from sqlalchemy import select
from ..database import engine, get_db, conn, cursor
from sqlalchemy.orm import Session


router = APIRouter( prefix= '/posts')

# here fastapi will driectly convert the array into a Json
## pass the sql (.execute) then runn it 
@router.get("/")
def get_posts():
    cursor.execute("""Select * from posts""")
    posts = cursor.fetchall()
    return posts

# returns as a pydantic model so new_posts is a pydantic model 
# fast api directly verifies the payload from the post request to match the schema that we expect from the pydantic package
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, user_id: int = Depends(oauth2.get_current_user)): #post- pydantic model , Post - schema
    print(user_id)
    cursor.execute("""INSERT INTO posts (title, content, published) Values (%s, %s, %s) Returning *  """, 
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

#id here is the path parameter
@router.get("/{id}")
def get_post(id: int):
    cursor.execute(""" select * from posts where id = %s""", (str(id)))
    test_post = cursor.fetchone()
    print(test_post)
    if not test_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="NOT found resourse")
    return test_post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "post to be deleted not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate,  user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post to be updated not found")
    return {"data": updated_post}



# auth - session based - keep in backend, info that says user is logged in
# no info on backend to track in JWT, token on frontend keeps track - stateless, client holds on to token and in the backend we jjust verify if its valid.
# payload is not encrypted - ie. jwt toek sent in header is not encrypted, you just have the signing algo, payload and the signature - which is header + payload + secret (secret in our API) - makes sure - its a unique string that says no one can access our token
# so one user one set of acess only, cant see others access - so sign = data integrity - its always been same, no one messed with it

