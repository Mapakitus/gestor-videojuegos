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
        db.add(user1)
        db.commit()

        # -------------------------
        # Crear reviews de ejemplo
        # -------------------------
        review1 = ReviewORM(rating=8.6, comment="Muy divertido", user_id=user1.id, videogame_id=vg1.id)
        review2 = ReviewORM(rating=9.0, comment="Me encantó", user_id=user1.id, videogame_id=vg2.id)
        db.add_all([review1, review2])
        db.commit()

    finally:
        db.close()
