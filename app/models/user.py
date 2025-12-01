from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.database import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    nif: Mapped[str | None] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    # Unidireccional
    reviews: Mapped[list["ReviewORM"]] = relationship("ReviewORM")
