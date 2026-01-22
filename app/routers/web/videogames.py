from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models.genre import GenreORM
from app.models.user import UserORM
from app.models.videogame import VideogameORM
from app.models.review import ReviewORM

templates = Jinja2Templates(directory="app/templates/")
router = APIRouter(prefix="/videogame", tags=["web"])

# ========================
# LISTADO DE LA BIBLIOTECA DEL USUARIO POR DEFECTO
# ========================
@router.get("/library", response_class=HTMLResponse)
def list_user_games(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario por defecto no encontrado")
    games = user.videogames

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "videogame/library.html",
        {"request": request, "games": games, "q": q, "result": result}
    )


# ========================
# DETALLE DEL VIDEOJUEGO
# ========================
@router.get("/{game_id}", response_class=HTMLResponse)
def game_detail(game_id: int, request: Request, q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(VideogameORM).where(VideogameORM.id == game_id).options(
        selectinload(VideogameORM.reviews).selectinload(ReviewORM.user)
    )
    videogame = db.execute(stmt).scalar_one_or_none()
    if not videogame:
        raise HTTPException(status_code=404, detail=f"No existe ningún videojuego con id {game_id}")

    genre = db.get(GenreORM, videogame.genre_id) if videogame.genre_id else None
    USER_ID = 2
    user = db.get(UserORM, USER_ID)

    has_game = user and videogame in user.videogames
    user_review = None
    if user:
        user_review = next((r for r in videogame.reviews if r.user_id == user.id), None)

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "videogame/detail.html",
        {
            "request": request,
            "videogame": videogame,
            "genre": genre,
            "user": user,
            "has_game": has_game,
            "reviews": videogame.reviews or [],
            "user_review": user_review,
            "q": q,
            "result": result
        }
    )


# ========================
# DESCARGAR / DESINSTALAR VIDEOJUEGO
# ========================
@router.post("/{game_id}/download", response_class=HTMLResponse)
def toggle_download(game_id: int, request: Request, q: str | None = None, db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    game = db.get(VideogameORM, game_id)

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    if not user or not game:
        raise HTTPException(status_code=404, detail="Usuario o videojuego no encontrado")

    message = ""
    if game in user.videogames:
        user.videogames.remove(game)
        message = "Videojuego desinstalado correctamente"
    else:
        user.videogames.append(game)
        message = "Videojuego descargado correctamente"
    db.commit()

    genre = db.get(GenreORM, game.genre_id)
    # Comprobamos si el usuario ya tiene reseña
    user_review = next((r for r in game.reviews if r.user_id == user.id), None)
    has_game = game in user.videogames
    return templates.TemplateResponse(
        "videogame/detail.html",
        {
            "request": request,
            "videogame": game,
            "genre": genre,
            "user": user,
            "has_game": has_game,
            "reviews": game.reviews or [],
            "user_review": user_review,
            "message": message,
            "q": q,
            "result": result
        }
    )



