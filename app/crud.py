# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User

# Получение всех пользователей
async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()

# Создание нового пользователя
async def create_user(session: AsyncSession, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)  # обновление с возвратом нового ID
    return user
