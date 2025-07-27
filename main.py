# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import uvicorn
#
#
# app = FastAPI()
#
# books = [
#
#     {'id': 1,
#     'author': 'Agatya'},
#
#     {'id': 2,
#     'author': 'Mura'}
#
# ]
#
# class NewBooks(BaseModel):
#     id: int
#     author: str
#
# @app.get('/', summary='Главная страница', tags=['Home'])
# def get_home():
#     return 'алло'
#
#
# @app.get('/books', summary='Получить все книги', tags=['Книги'])
# def get_books():
#     return books
#
#
# @app.get('/books/{book_id}', summary='Получить книгу', tags=['Книги'])
# def get_book(book_id: int):
#     for book in books:
#         if book['id'] == book_id:
#             return book
#     raise HTTPException(status_code=404, detail='Книга не найдена')
#
#
# @app.post('/books', summary='Добавить книгу', tags=['Книги'])
# def create_book(new_book: NewBooks):
#     books.append({
#         'id': len(books) + 1,
#         'author': new_book.author
#     })
#     return {'success': True, 'message': 'ура ура'}
# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session, engine, Base
from app import crud
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# При старте приложения создаём таблицы, если их нет
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Получение списка всех пользователей
@app.get("/users/")
async def read_users(session: AsyncSession = Depends(get_session)):
    users = await crud.get_users(session)
    return users

# Создание нового пользователя (через query параметры: ?name=...&email=...)
@app.post("/users/")
async def create_user(
    name: str,
    email: str,
    session: AsyncSession = Depends(get_session)
):
    return await crud.create_user(session, name, email)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
