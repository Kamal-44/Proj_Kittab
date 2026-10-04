from fastapi import FastAPI
from routers import books, users
from contextlib import asynccontextmanager
from database import create_table


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_table()
    yield

app=FastAPI(title="Used Books selling platform",
            description="Regiter yourself as user and then list your books or buy used books as per your choice ",
            lifespan=lifespan)


app.include_router(users.router)
app.include_router(books.router)


@app.get("/")
def root():
    return {
        "messages":"Welcome to Kiaatb becho platform"
    }