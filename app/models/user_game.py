from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

user_game_table = Table(
    "user_game",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("videogame_id", Integer, ForeignKey("videogames.id"), primary_key=True),
)
