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
from .. import models, schemas, utils
from sqlalchemy import select
from ..database import engine, get_db, conn, cursor
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users", status_code= status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# in authentication, if user in frontend cant access the api endpoint for his own acc info, he needs to fetch a new JWT token
@router.get('/users/{id}')
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "not foound")
    return user