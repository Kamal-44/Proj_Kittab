from dataclasses import field
from sqlalchemy import table
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from fastapi import Query


class User(SQLModel,table=True):
    id: Optional[int]=Field(default=None,primary_key=True)
    name: str= Field(index=True)
    email: str= Field(unique=True)
    college: str
    books:list["Book"]= Relationship(back_populates="owner")

class UserCreate(SQLModel):
    name: str
    email: str
    college: str

class UserRead(SQLModel):
    id:int
    name: str
    email: str
    college : str

# for taking circular
from models.book import Book
User.model_rebuild()