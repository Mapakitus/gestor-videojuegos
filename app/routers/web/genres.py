

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

# show form create

@router.get("/new", response_class=HTMLResponse)
def show_form_create(request: Request):
    return templates.TemplateResponse(
        "genre/form.html",
        {"request": request, "genre": None}
    )

# create new genre

@router.post("/new", response_class=HTMLResponse)
def create_genre(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    image_url: str = Form(None),
    db: Session = Depends(get_db)
):
    errors = []

    form_data = {
        "name": name,
        "description": description
    }

    if not name or not name.strip():
        errors.append("El nombre no puede estar vacío")
    if not description or not description.strip():
        errors.append("La descripcion no puede estar vacía")

    image_url_value = None
    if image_url and image_url.strip():
        image_url_value = image_url.strip()


    if errors:
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": None, "errors": errors, "form_data": form_data}
        )
    
    try:

        new_genre = GenreORM(
            name = name.strip(),
            description = description.strip(),
            image_url=image_url_value
        )

        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)

        return RedirectResponse(url=f"/genres/{new_genre.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el género: {str(e)}")
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": None, "errors": errors, "form_data": form_data}
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
    
# form edit genre

@router.get("/{genre_id}/edit", response_class=HTMLResponse)
def show_form_edit(request: Request, genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == genre_id)).scalar_one_or_none()

    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ningún género con este id")
    
    return templates.TemplateResponse(
        "genre/form.html",
        {"request": request, "genre": genre}
    )

# edit genre

@router.post("/{genre_id}/edit", response_class=HTMLResponse)
def update_genre(
    request: Request,
    genre_id: int,
    name: str = Form(...),
    description: str = Form(...),
    image_url: str = Form(None),
    db: Session = Depends(get_db)
    ):

    genre = db.execute(select(GenreORM).where(GenreORM.id == genre_id)).scalar_one_or_none()
    
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ningún género con este id")
    

    errors = []

    form_data = {
        "name": name,
        "description": description,
        "image_url": image_url
    }

    if not name or not name.strip():
        errors.append("El nombre no puede estar vacío")
    if not description or not description.strip():
        errors.append("La descripción no puede estar vacía")

    image_url_value = None
    if image_url and image_url.strip():
        image_url_value = image_url.strip()

    if errors:
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": genre, "errors": errors, "form_data": form_data}
        )
    
    try:
        
        genre.name = name.strip()
        genre.description = description.strip()
        genre.image_url = image_url_value

        db.commit()
        db.refresh(genre)

        return RedirectResponse(url=f"/genres/{genre.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append("No se ha podido editar el género con exito")
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": genre, "errors": errors, "form_data": form_data}
        )
