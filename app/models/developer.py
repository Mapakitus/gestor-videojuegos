from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.videogame import Videogame

class DevORM(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    videogames = relationship("Videogame", back_populates="developer")
