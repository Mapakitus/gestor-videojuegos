from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from app.models.videogame import VideogameORM

class DevORM(Base):
    __tablename__ = "developers"

    id = Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = Mapped[str] = mapped_column(String, nullable=False)

    videogames = relationship("Videogame", back_populates="developer")

    videogames: Mapped[list[VideogameORM]] = relationship(back_populates="developer")