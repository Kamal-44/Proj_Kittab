from email.policy import default

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.sql.operators import contains
from sqlmodel import select, Session
from typing import Optional
from auth import verify_apikey
from models import book, user
from database import get_session
from models.book import Book,BookRead,BookCreate,BookUpdate


router=APIRouter(prefix="/book", tags=["Book"])

@router.get("/",response_model=list[BookRead])
def list_books(
        author:Optional[str]=Query(default=None,detail="Filter the list of books from Author"),
        title:Optional[str]=Query(default=None,detail="Filter the list of books from Title"),
        session:Session=Depends(get_session)
        ):
    query=select(Book).where(
        Book.is_sold==False
    )
    if author:
        query=query.where(Book.author.contains(author))
    if title:
        query=query.where(Book.title.contains(title))

    return session.exec(query).all()


@router.post("/",response_model=BookRead)
def add_book(
        book_data:BookCreate,
        session:Session=Depends(get_session)
):
    book=Book.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.patch("/",response_model=BookRead)
def update_book(
        update_data:BookUpdate,
        session:Session=Depends(get_session)
):
    book=session.get(Book,update_data.id)
    if not book:
        raise HTTPException(status_code=404,detail="No Book found with this id")

    book_data=update_data.model_dump(exclude_unset=True) #converting to dictionary

    for key,value in book_data.items():
        setattr(book,key,value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book






