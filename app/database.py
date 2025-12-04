"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# -------------------------
# Clase base para modelos SQLAlchemy
# -------------------------
class Base(DeclarativeBase):
    pass

# -------------------------
# Motor de conexión a la base de datos
# -------------------------
engine = create_engine(
    "sqlite:///videogames.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# -------------------------
# Fábrica de sesiones
# -------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# -------------------------
# Dependencia para FastAPI
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Inicialización de la base de datos
# -------------------------
def init_db():
    # Importar modelos aquí dentro para evitar circular imports
    from app.models.genre import GenreORM
    from app.models.videogame import VideogameORM
    from app.models.developer import DevORM
    from app.models.user import UserORM
    from app.models.review import ReviewORM

    # Crear todas las tablas
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        # Si ya hay géneros, asumimos que la DB ya tiene datos
        if db.query(GenreORM).first():
            return

        # -------------------------
        # Crear géneros de ejemplo
        # -------------------------
        action = GenreORM(name="Acción", description="Juegos de acción")
        adventure = GenreORM(name="Aventuras", description="Juegos de aventuras")
        rpg = GenreORM(name="Rol", description="Juegos de rol")
        db.add_all([action, adventure, rpg])
        db.commit()

        # -------------------------
        # Crear developers de ejemplo
        # -------------------------
        dev1 = DevORM(name="Dev Studio 1")
        dev2 = DevORM(name="Dev Studio 2")
        dev3 = DevORM(name="Dev Studio 3")
        db.add_all([dev1, dev2, dev3])
        db.commit()

        # -------------------------
        # Crear videojuegos de ejemplo
        # -------------------------
        vg1 = VideogameORM(title="Super Action Game", description="Juego de acción épico", genre_id=action.id, developer_id=dev1.id)
        vg2 = VideogameORM(title="Adventure Quest", description="Explora mundos fantásticos", genre_id=adventure.id, developer_id=dev2.id)
        vg3 = VideogameORM(title="RPG Legends", description="RPG clásico con héroes y mazmorras", genre_id=rpg.id, developer_id=dev3.id)
        db.add_all([vg1, vg2, vg3])
        db.commit()

        # -------------------------
        # Crear usuarios de ejemplo
        # -------------------------
        user1 = UserORM(nick="admin", email="admin@hotmail.es", nif="1231231231", password="admin1234")
        user2 = UserORM(nick="player1", email="player1@gmail.com", nif="111111111A", password="player1234")
        user3 = UserORM(nick="player2", email="player2@gmail.com", nif="222222222B", password="player2345")
        db.add_all([user1, user2, user3])
        db.commit()
        
        # -------------------------
        # Asignar videojuegos a los usuarios (bibliotecas)
        # -------------------------
        user1.videogames.append(vg1)
        user1.videogames.append(vg2)

        user2.videogames.append(vg2)
        user2.videogames.append(vg3)

        user3.videogames.append(vg1)
        user3.videogames.append(vg3)

        db.commit()

        # -------------------------
        # Crear reviews de ejemplo
        # -------------------------
        review1 = ReviewORM(rating=8.6, comment="Muy divertido", user_id=user1.id, videogame_id=vg1.id)
        review2 = ReviewORM(rating=9.0, comment="Me encantó", user_id=user1.id, videogame_id=vg2.id)
        review3 = ReviewORM(rating=7.5, comment="Buen juego", user_id=user2.id, videogame_id=vg2.id)
        review4 = ReviewORM(rating=9.2, comment="Excelente RPG", user_id=user2.id, videogame_id=vg3.id)
        review5 = ReviewORM(rating=8.0, comment="Entretenido", user_id=user3.id, videogame_id=vg1.id)
        review6 = ReviewORM(rating=9.5, comment="Me fascinó", user_id=user3.id, videogame_id=vg3.id)

        db.add_all([review1, review2, review3, review4, review5, review6])
        db.commit()

    finally:
        db.close()
