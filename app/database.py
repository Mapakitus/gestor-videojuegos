"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine, select
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
    from app.models.videogame import Videogame
    from app.models.developer import Developer

    # Crear todas las tablas
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        # Si ya hay géneros, asumimos que la DB ya tiene datos
        if db.query(GenreORM).first():
            return

        # Crear géneros de ejemplo
        action = GenreORM(name="Acción", description="Juegos de acción")
        adventure = GenreORM(name="Aventuras", description="Juegos de aventuras")
        rpg = GenreORM(name="Rol", description="Juegos de rol")
        db.add_all([action, adventure, rpg])
        db.commit()
        
         # Crear developers
        dev1 = Developer(name="Dev Studio 1")
        dev2 = Developer(name="Dev Studio 2")
        dev3 = Developer(name="Dev Studio 3")
        db.add_all([dev1, dev2, dev3])
        db.commit()

        # Crear videojuegos de ejemplo
        db.add_all([
            Videogame(title="Super Action Game", description="Juego de acción épico", genre_id=action.id, developer_id=1),
            Videogame(title="Adventure Quest", description="Explora mundos fantásticos", genre_id=adventure.id, developer_id=2),
            Videogame(title="RPG Legends", description="RPG clásico con héroes y mazmorras", genre_id=rpg.id, developer_id=3)
        ])
        db.commit()
    finally:
        db.close()
