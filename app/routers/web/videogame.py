from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.genre import GenreORM
from app.models.user import UserORM
from app.models.videogame import VideogameORM


templates = Jinja2Templates(directory="app/templates/")

router = APIRouter(prefix="/videogame", tags=["web"])

# show all games

@router.get("", response_class=HTMLResponse)
def list_videogames(request: Request, db: Session = Depends(get_db)):
    videogames = db.execute(select(VideogameORM)).scalars().all()
    last_games = db.execute(select(VideogameORM).order_by(VideogameORM.id.desc()).limit(3)).scalars().all()
    
    if not videogames:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Base de datos no encontrada")
    

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "videogames": videogames, "last_games": last_games}
    )

# show form create videogame
    
@router.get("/new", response_class=HTMLResponse)
def form_create(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "videogame/form.html",
        {"request": request, "videogame": None}
    )


# create new videogame

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
        "title": title,
        "description": description,
        "cover_url": cover_url,
        "genre_id": genre_id,
        "developer_id": developer_id
    }

    if not title or not title.strip():
        errors.append("El título del videojuego no puede estar vacío")

    description_value = None
    if description and description.strip():
        description_value = description.strip()

    cover_url_value = None
    if cover_url and cover_url.strip():
        cover_url_value = cover_url.strip()

    genre_id_value = None
    if genre_id and genre_id.strip():
        try:
            genre_id_value = int(genre_id.strip())
            if genre_id_value < 0:
                errors.append("El género id no puede ser negativo")
        except ValueError:
            errors.append("El id debe ser un número válido")

    developer_id_value = None
    if developer_id and developer_id.strip():
        try:

            developer_id_value = int(developer_id.strip())
            if developer_id_value < 0:
                errors.append("El desarrolladora id no puede ser negativo")
        except ValueError:
            errors.append("El id debe ser un número válido")

    if errors:
        return templates.TemplateResponse(
            "videogame/form.html",
            {"request": request, "videogame": None, "errors": errors, "form_data": form_data}
        )
    
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
        return templates.TemplateResponse(
            "videogame/form.html",
            {"request": request, "videogame": None, "errors": errors, "form_data": form_data}
        )
    
# show detail videogame

@router.get("/{game_id}", response_class=HTMLResponse)
def game_detail(game_id: int, request: Request, db: Session = Depends(get_db)):
    videogame = db.execute(select(VideogameORM).where(VideogameORM.id == game_id)).scalar_one_or_none()
    genre = db.execute(select(GenreORM).where(GenreORM.id == videogame.genre_id)).scalar_one_or_none()
    

    if videogame is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"404 - No existe ningún videojuego con el id {game_id}")
    
    return templates.TemplateResponse(
        "videogame/detail.html",
        {"request": request, "videogame": videogame, "genre": genre}
    )


# edit videogame by id

@router.get("/{game_id}/edit", response_class=HTMLResponse)
def form_edit(request: Request, game_id: int, db: Session = Depends(get_db)):
    game = db.execute(select(VideogameORM).where(VideogameORM.id == game_id)).scalar_one_or_none()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - No existe este videojuego")
     
    return templates.TemplateResponse(
         "videogame/form.html",
         {"request": request, "game": game}
    )


# 

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

    game = db.execute(select(VideogameORM).where(VideogameORM.id == game_id)).scalar_one_or_none()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - No existe este videojuego")
    
    errors = []

    form_data = {
        "title": title,
        "description": description,
        "cover_url": cover_url,
        "genre_id": genre_id,
        "developer_id": developer_id
    }

    if not title or not title.strip():
        errors.append("El título no puede estar vacío")

    title_value = title.strip()

    description_value = None
    if description and description.strip():
        description_value = description.strip()

    cover_url_value = None
    if cover_url and cover_url.strip():
        cover_url_value = cover_url

    genre_id_value = None
    if genre_id and genre_id.strip():
        try:
            genre_id_value = int(genre_id.strip())
            if genre_id_value < 0:
                errors.append("El id no puede ser un número negativo")
        except ValueError:
            errors.append("El id tiene que ser un número válido")

    developer_id_value = None
    if developer_id and developer_id.strip():
        try:
            developer_id_value = int(developer_id.strip())
            if developer_id_value < 0:
                errors.append("El id no puede ser un número negativo")
        except ValueError:
            errors.append("El id tiene que ser un número válido")

    if errors:
        return templates.TemplateResponse(
            "videogames/form.html",
            {"request": request, "game": game, "errors": errors, "form_data": form_data}
        )
    
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
        errors.append(f"No se ha podido crea el videojuego: {str(e)}")
        return templates.TemplateResponse(
            "videogame/form.html",
            {"request": request, "game": game, "errors": errors, "form_data": form_data}
        )



# @router.post("{game_id}", response_class=HTMLResponse)
# def add_to_library(game_id: int, db: Session = Depends(get_db)):
#     user_id = 2

#     game = db.execute(select(VideogameORM).where(VideogameORM.id == game_id)).scalar_one_or_none()
#     user = db.execute(select(UserORM).where(UserORM == user_id))

#     if game is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"404 - No hay ningún juego con el id {game_id} en la base de datos")
    


            
