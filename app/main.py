"""
Configuración de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routers.api import router as api_router
from app.routers.web import router as web_router


#Crea la instancia de la aplicación FastAPI
app = FastAPI(title="Videojuegos API", version="1.0.0")

# Montar la carpeta static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#inicializa la base de datos con videojuegos por defecto
init_db()

#incluir routers de la API
app.include_router(api_router)
app.include_router(web_router)