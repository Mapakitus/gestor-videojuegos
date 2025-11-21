"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# crear motor de conexión a base de datos
engine = create_engine(
    "sqlite:///videogames.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# clase base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass

# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()


# INICIALIZACIÓN BASE DE DATOS

# método inicializar con canciones por defecto
def init_db():
    """
    Inicializa la base de datos con datos por defecto si está vacía.
    Sólo crea los datos si no existen ya en la base de datos.
    """
    from app.models import Videogame
    
    # crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        existing_videogames = db.execute(select(Videogame)).scalars().all()
        
        if existing_videogames:
            return
        
        default_videogames = [
            Videogame(title="Mamma Mia", artist="ABBA", duration_seconds=300, explicit=False),
            Videogame(title="Sin ti no soy nada", artist="Amaral", duration_seconds=250, explicit=False),
            Videogame(title="Sonata para piano nº 14", artist="Ludwig van Beethoven", duration_seconds=800, explicit=False),
            Videogame(title="Mediterráneo", artist="Joan Manuel Serrat", duration_seconds=400, explicit=False),
            Videogame(title="Never to Return", artist="Darren Korb", duration_seconds=300, explicit=False),
            Videogame(title="Billie Jean", artist="Michael Jackson", duration_seconds=294, explicit=False),
            Videogame(title="Smells Like Teen Spirit", artist="Nirvana", duration_seconds=301, explicit=True)
        ]
        
        # agregar las canciones
        db.add_all(default_videogames)
        db.commit()
    finally:
        db.close()
        
