from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.database import Base
from app.models.user_game import user_game_table

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    nif: Mapped[str | None] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)


    videogames = relationship(
        "VideogameORM",
        secondary=user_game_table,
        back_populates="users"
    )
    # Unidireccional
    reviews: Mapped[list["ReviewORM"]] = relationship("ReviewORM")
