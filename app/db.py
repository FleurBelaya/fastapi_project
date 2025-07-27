# db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# Создаём асинхронный движок SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)

# Создаём асинхронную сессию для взаимодействия с БД
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass


# Зависимость FastAPI для получения сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
