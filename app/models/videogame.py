from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app.database import Base
from app.models.genre import GenreORM
from app.models.developer import DevORM
from app.models.review import ReviewORM

class VideogameORM(Base):
    __tablename__ = "videogames"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    cover_url: Mapped[str | None] = mapped_column(String, nullable=True)

    genre_id: Mapped[int | None] = mapped_column(ForeignKey("genres.id"))
    developer_id: Mapped[int | None] = mapped_column(ForeignKey("developers.id"))

    genre: Mapped[GenreORM] = relationship(back_populates="videogames")
    developer: Mapped[DevORM] = relationship(back_populates="videogames")
    reviews: Mapped[list["ReviewORM"]] = relationship(back_populates="videogame")
    #Temporalmente comentado hasta que se creen las tablas
    #usergames = relationship("UserGame", back_populates="videogame")
