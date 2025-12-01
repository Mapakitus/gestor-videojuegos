from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from app.database import Base

class ReviewORM(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    videogame_id: Mapped[int] = mapped_column(ForeignKey("videogames.id"), nullable=False)
    
    # Unidireccionales
    user: Mapped["UserORM"] = relationship("UserORM")
    videogame: Mapped["VideogameORM"] = relationship("VideogameORM")


