from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from app.database import Base
from app.models.user import UserORM
from app.models.videogame import VideogameORM

class ReviewORM(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    videogame_id: Mapped[int] = mapped_column(ForeignKey("videogames.id"), nullable=False)

    user: Mapped[UserORM] = relationship(back_populates="reviews")
    videogame: Mapped[VideogameORM] = relationship(back_populates="reviews")


