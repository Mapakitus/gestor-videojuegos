from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app.database import Base

class VideogameORM(Base):
    __tablename__ = "videogames"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    cover_url: Mapped[str | None] = mapped_column(String, nullable=True)

    genre_id: Mapped[int | None] = mapped_column(ForeignKey("genres.id"))
    developer_id: Mapped[int | None] = mapped_column(ForeignKey("developers.id"))

    # Unidireccionales
    genre: Mapped["GenreORM"] = relationship("GenreORM")
    developer: Mapped["DevORM"] = relationship("DevORM")

    # Reviews → usamos string para evitar import directo
    reviews: Mapped[list["ReviewORM"]] = relationship("ReviewORM")
    #Temporalmente comentado hasta que se creen las tablas
    #usergames = relationship("UserGame", back_populates="videogame")
