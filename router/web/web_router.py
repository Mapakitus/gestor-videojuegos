
from fastapi import APIRouter


router = APIRouter()

@router.get("/info")
def get_info():
    return {"app": "Gestor de Videojuegos", "para que sirve el router": "Para organizar las rutas de la web, habrá otro router para la API por si queremos separar ambas cosas"}