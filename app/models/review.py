from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    videogame_id = Column(Integer, ForeignKey("videogames.id"), nullable=False)

    user = relationship("User", back_populates="reviews")
    videogame = relationship("Videogame", back_populates="reviews")
