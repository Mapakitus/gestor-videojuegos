from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.genre import GenreORM
from app.models.user import UserORM
from app.models.videogame import VideogameORM

router = APIRouter(prefix="/videogame", tags=["web"])

templates = Jinja2Templates(directory="app/templates")

@router.post("/{user_id}/{videogame_id}/download", response_class=HTMLResponse)
def download_videogame(
    request: Request,
    user_id: int,
    videogame_id: int,
    db: Session = Depends(get_db)
):

    errors = []

    user = db.get(UserORM, user_id)
    game = db.get(VideogameORM, videogame_id)

    if not user:
        errors.append("Usuario no encontrado")

    if not game:
        errors.append("Videojuego no encontrado")

    if errors:
        return templates.TemplateResponse(
            "videogame/detail.html",
            {"request": request, "errors": errors, "game": game}
        )

    # Evita agregarlo si ya lo descargó
    if game in user.videogames:
        return templates.TemplateResponse(
            "videogame/detail.html",
            {
                "request": request,
                "game": game,
                "message": "Ya has descargado este videojuego"
            }
        )
    
    # Aquí se crea la relación en user_game ⬇⬇⬇
    user.videogames.append(game)
    db.commit()

    return templates.TemplateResponse(
        "videogame/detail.html",
        {
            "request": request,
            "game": game,
            "message": "Videojuego descargado correctamente"
        }
    )
