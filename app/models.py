from sqlite3 import Timestamp
from time import timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.expression import null
from .database import Base
from sqlalchemy.sql import func


#this model just defines what the table should look like, responsible for defining the columns of the table
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default='TRUE', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String,nullable= False, unique=True)
    password = Column(String,nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)