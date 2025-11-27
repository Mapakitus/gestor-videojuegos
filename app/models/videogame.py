from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Videogame(Base):
    __tablename__ = "videogames"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    
    cover_url = Column(String, nullable=True)

    genre_id = Column(Integer, ForeignKey("genres.id"))
    developer_id = Column(Integer, ForeignKey("developers.id"))

    genre = relationship("GenreORM")
    developer = relationship("Developer")

    #Temporalmente comentado hasta que se creen las tablas
    #reviews = relationship("Review", back_populates="videogame")
    #usergames = relationship("UserGame", back_populates="videogame")
