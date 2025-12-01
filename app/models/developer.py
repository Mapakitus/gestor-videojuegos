from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.database import Base
from app.models.videogame import VideogameORM

class DevORM(Base):
    __tablename__ = "developers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    videogames: Mapped[list["VideogameORM"]] = relationship(back_populates="developer")
