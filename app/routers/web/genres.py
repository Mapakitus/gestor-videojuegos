

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.genre import GenreORM
from app.models.videogame import VideogameORM


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/genres", tags=["web"])

# list genres

@router.get("", response_class=HTMLResponse)
def list_genres(request: Request, db: Session = Depends(get_db)):
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()

    return templates.TemplateResponse(
        "genre/list.html",
        {"request": request, "genres": genres}
    )


# videogame with same genre id

@router.get("/{genre_id}", response_class=HTMLResponse)
def genre_detail(request: Request ,genre_id: int, db: Session = Depends(get_db)):
    videogame = db.execute(select(VideogameORM).where(VideogameORM.genre_id == genre_id)).scalars().all()
    genre = db.execute(select(GenreORM).where(GenreORM.id == genre_id)).scalar_one_or_none()

    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún género con el id {genre_id}")
    
    return templates.TemplateResponse(
        "genre/detail.html",
        {"request": request, "videogame": videogame, "genre": genre}
    )
    

