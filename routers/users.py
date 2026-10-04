from email.header import Header

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from auth import verify_apikey
from database import get_session
from models import book, user
from models.user import User,UserRead,UserCreate
from models.book import Book,BookRead,BookCreate


router=APIRouter(prefix="/user",tags=["User"])


@router.post("/", response_model=UserRead)
def register_user(
        user_data: UserCreate,
        session: Session = Depends(get_session)
):
    existing = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing:
        return HTTPException(status_code=400, detail="user already exists")
    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[User])
def list_users(
        session: Session = Depends(get_session)
):
    return session.exec(select(User)).all()
