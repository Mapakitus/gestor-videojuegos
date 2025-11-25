from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str] = mapped_column(String, nullable=False) 
    email: Mapped[str] = mapped_column(String, nullable=False)
    nif: Mapped[str | None] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

