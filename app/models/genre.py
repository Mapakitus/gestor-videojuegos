from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

# Modelo Base de datos (Genero)

class GenreORM(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)