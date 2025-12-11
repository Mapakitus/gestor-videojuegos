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
def list_user_games(request: Request, db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario por defecto no encontrado")
    games = user.videogames
    return templates.TemplateResponse(
        "videogame/list.html",
        {"request": request, "games": games}
    )

# ========================
# CREAR NUEVO VIDEOJUEGO
# ========================
@router.get("/new", response_class=HTMLResponse)
def form_create(request: Request):
    return templates.TemplateResponse("videogame/form.html", {"request": request, "videogame": None})

@router.post("/new", response_class=HTMLResponse)
def create(
    request: Request,
    title:str = Form(...),
    description: str = Form(None),
    cover_url: str = Form(None),
    genre_id: str = Form(None),
    developer_id: str = Form(None),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "title": title, "description": description,
        "cover_url": cover_url, "genre_id": genre_id,
        "developer_id": developer_id
    }
    if not title or not title.strip():
        errors.append("El título del videojuego no puede estar vacío")
    description_value = description.strip() if description else None
    cover_url_value = cover_url.strip() if cover_url else None
    genre_id_value = int(genre_id.strip()) if genre_id and genre_id.strip().isdigit() else None
    developer_id_value = int(developer_id.strip()) if developer_id and developer_id.strip().isdigit() else None

    if errors:
        return templates.TemplateResponse("videogame/form.html", {"request": request, "videogame": None, "errors": errors, "form_data": form_data})

    try:
        new_game = VideogameORM(
            title=title.strip(),
            description=description_value,
            cover_url=cover_url_value,
            genre_id=genre_id_value,
            developer_id=developer_id_value
        )
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return RedirectResponse(url=f"/videogame/{new_game.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el videojuego: {str(e)}")
        return templates.TemplateResponse("videogame/form.html", {"request": request, "videogame": None, "errors": errors, "form_data": form_data})

# ========================
# DETALLE DEL VIDEOJUEGO
# ========================
@router.get("/{game_id}", response_class=HTMLResponse)
def game_detail(game_id: int, request: Request, db: Session = Depends(get_db)):
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

    return templates.TemplateResponse(
        "videogame/detail.html",
        {
            "request": request,
            "videogame": videogame,
            "genre": genre,
            "user": user,
            "has_game": has_game,
            "reviews": videogame.reviews or [],
            "user_review": user_review
        }
    )

# ========================
# EDITAR VIDEOJUEGO
# ========================
@router.post("/{game_id}/edit", response_class=HTMLResponse)
def edit_videogame(
    request: Request, 
    game_id: int,
    title: str = Form(...),
    description: str = Form(None),
    cover_url: str = Form(None),
    genre_id: str = Form(None),
    developer_id: str = Form(None),
    db: Session = Depends(get_db)               
):
    game = db.get(VideogameORM, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="No existe este videojuego")

    errors = []
    if not title or not title.strip():
        errors.append("El título no puede estar vacío")
    title_value = title.strip()
    description_value = description.strip() if description else None
    cover_url_value = cover_url.strip() if cover_url else None
    genre_id_value = int(genre_id.strip()) if genre_id and genre_id.strip().isdigit() else None
    developer_id_value = int(developer_id.strip()) if developer_id and developer_id.strip().isdigit() else None

    if errors:
        return templates.TemplateResponse("videogame/form.html", {"request": request, "game": game, "errors": errors})

    try:
        game.title = title_value
        game.description = description_value
        game.cover_url = cover_url_value
        game.genre_id = genre_id_value
        game.developer_id = developer_id_value
        db.commit()
        db.refresh(game)
        return RedirectResponse(url=f"/videogame/{game.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"No se ha podido actualizar el videojuego: {str(e)}")
        return templates.TemplateResponse("videogame/form.html", {"request": request, "game": game, "errors": errors})

# ========================
# DESCARGAR / DESINSTALAR VIDEOJUEGO
# ========================
@router.post("/{game_id}/download", response_class=HTMLResponse)
def toggle_download(game_id: int, request: Request, db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    game = db.get(VideogameORM, game_id)
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
            "message": message
        }
    )
