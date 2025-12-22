
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.developer import DevORM
from app.models.genre import GenreORM
from app.models.user import UserORM
from app.models.videogame import VideogameORM

# Configura la carpeta de plantillas
templates = Jinja2Templates(directory="app/templates")

# Crea el router con el prefijo /admin
router = APIRouter(prefix="/admin", tags=["admin"])

# Endpoint para la página principal del panel de administración
@router.get("", response_class=HTMLResponse)
def admin_dashboard(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    """
    Renderiza la página del panel de administración.
    """

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "title": "Panel de Administración", "result": result, "q": q}
    )


# Lista de videojuego admin
@router.get("/videogame", response_class=HTMLResponse)
def list_games(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    games = db.execute(select(VideogameORM).order_by(VideogameORM.title)).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "admin/videogame.html",
        {"request": request, "games": games, "result": result, "q": q}
    )


# ========================
# CREAR NUEVO VIDEOJUEGO
# ========================
@router.get("/videogame/new", response_class=HTMLResponse)
def form_create(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    genres = db.execute(select(GenreORM).order_by(GenreORM.name)).scalars().all()
    devs = db.execute(select(DevORM).order_by(DevORM.name)).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse("videogame/form.html", {"request": request, "game": None, "genres": genres, "devs": devs, "result": result, "q": q})

@router.post("/videogame/new", response_class=HTMLResponse)
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
    description_value = description.strip() if description else None
    cover_url_value = cover_url.strip() if cover_url else None
    genre_id_value = int(genre_id.strip()) if genre_id and genre_id.strip().isdigit() else None
    developer_id_value = int(developer_id.strip()) if developer_id and developer_id.strip().isdigit() else None

    if errors:
        return templates.TemplateResponse("videogame/form.html", {"request": request, "game": None, "errors": errors, "form_data": form_data})

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
        return templates.TemplateResponse("videogame/form.html", {"request": request, "game": None, "errors": errors, "form_data": form_data})
    




# ========================
# EDITAR VIDEOJUEGO
# ========================
@router.get("/videogame/{game_id}/edit", response_class=HTMLResponse)
def form_edit(
    request: Request,
    game_id: int,
    q: str | None = None,
    db: Session = Depends(get_db) 
):
    
    game = db.execute(select(VideogameORM).where(VideogameORM.id == game_id)).scalar_one_or_none()
    genres = db.execute(select(GenreORM).order_by(GenreORM.name)).scalars().all()
    devs = db.execute(select(DevORM).order_by(DevORM.name)).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "videogame/form.html",
        {"request": request, "game": game, "genres": genres, "devs": devs, "result": result, "q": q}
    )
    
# POST EDIT VIDEOGAME
@router.post("/videogame/{game_id}/edit", response_class=HTMLResponse)
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
    form_data = {
        "title": title,
        "description": description,
        "cover_url":cover_url,
        "genre_id": genre_id,
        "developer_id": developer_id
    }

    if not title or not title.strip():
        errors.append("El título no puede estar vacío")
    title_value = title.strip()
    description_value = description.strip() if description else None
    cover_url_value = cover_url.strip() if cover_url else None
    genre_id_value = int(genre_id.strip()) if genre_id and genre_id.strip().isdigit() else None
    developer_id_value = int(developer_id.strip()) if developer_id and developer_id.strip().isdigit() else None

    if errors:
        return templates.TemplateResponse("videogame/form.html", {"request": request, "game": game, "errors": errors, "form_data": form_data})

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
        return templates.TemplateResponse("videogame/form.html", {"request": request, "game": game, "errors": errors, "form_data": form_data})
    
# delete videogame

@router.post("/videogame/{game_id}/delete", response_class=HTMLResponse)
def delete_game(request: Request, game_id: int, db: Session = Depends(get_db)):
    game = db.execute(select(VideogameORM).where(VideogameORM.id == game_id)).scalar_one_or_none()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - El juego que intentas borrar no existe")
    
    db.delete(game)
    db.commit()
    
    return RedirectResponse(url="/admin/videogame", status_code=303)


# ------------------------------------- GENRES -------------------------------------------------

# list genres

@router.get("/genre", response_class=HTMLResponse)
def list_genres(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "admin/genre.html",
        {"request": request, "genres": genres, "q":q, "result": result}
    )



# show form create

@router.get("/genre/new", response_class=HTMLResponse)
def show_form_create(request: Request, q: str | None = None, db: Session = Depends(get_db)):

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "genre/form.html",
        {"request": request, "genre": None, "q": q, "result": result}
    )

# create new genre

@router.post("/genre/new", response_class=HTMLResponse)
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
    

# form edit genre

@router.get("/genre/{genre_id}/edit", response_class=HTMLResponse)
def show_form_edit(request: Request, genre_id: int, q: str | None = None, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == genre_id)).scalar_one_or_none()

    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ningún género con este id")
    
    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()
    
    return templates.TemplateResponse(
        "genre/form.html",
        {"request": request, "genre": genre, "result": result, "q": q}
    )

# edit genre

@router.post("/genre/{genre_id}/edit", response_class=HTMLResponse)
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
        errors.append(f"No se ha podido editar el género con exito: {str(e)}")
        return templates.TemplateResponse(
            "genre/form.html",
            {"request": request, "genre": genre, "errors": errors, "form_data": form_data}
        )
    
# Delete Genre

@router.post("/genre/{genre_id}/delete", response_class=HTMLResponse)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == genre_id)).scalar_one_or_none()

    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - El género que se quiere eliminar no existe")
    
    db.delete(genre)
    db.commit()

    return RedirectResponse(url="/admin/genre", status_code=303)


# ----------------------------------USER------------------------------------------

# User List

@router.get("/user", response_class=HTMLResponse)
def list_users(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    users = db.execute(select(UserORM)).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "admin/user.html",
        {"request": request, "users": users, "result": result, "q": q}
    )

# User create

@router.get("/user/new", response_class=HTMLResponse)
def form_user(request: Request, q: str | None = None, db: Session = Depends(get_db)):

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "user/form.html",
        {"request": request, "user": None, "result": result, "q": q}
    )

# Post user create

@router.post("/user/new", response_class=HTMLResponse)
def create_user(
    request: Request,
    nick: str = Form(...),
    email: str = Form(...),
    nif: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    errors = []
    form_data = {
        "nick": nick,
        "email": email,
        "nif": nif,
        "password": password,
    }

    if not nick or not nick.strip():
        errors.append("El nombre de usuario no puede estar vacío")
    
    if not email or not email.strip():
        errors.append("El email no puede estar vacío")
    
    nif_value = None
    if nif and nif.strip():
        nif_value = nif

    if not password and not password.strip():
        errors.append("La contraseña no puede estar vacía")

    if errors:
        return templates.TemplateResponse(
            "user/form.html",
            {"request": request, "user": None, "errors": errors, "form_data": form_data}
        )

    try:

        new_user = UserORM(
            nick=nick.strip(),
            email=email.strip(),
            nif=nif_value,
            password=password.strip()
        )


        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RedirectResponse(url="/admin/user/", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Se ha producido un error: {str(e)}")
        return templates.TemplateResponse(
                    "user/form.html",
                    {"request": request, "user": None, "errors": errors, "form_data": form_data}
                )
    
# Edit user

@router.get("/user/{user_id}/edit", response_class=HTMLResponse)
def edit_user(request: Request, user_id: int, q: str | None = None, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == user_id)).scalar_one_or_none()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        "user/form.html",
        {"request": request, "user": user, "result": result, "q": q}
    )

# Post edit user


@router.post("/user/{user_id}/edit", response_class=HTMLResponse)
def post_edit_user(
    request: Request,
    user_id: int,
    nick: str = Form(...),
    email: str = Form(...),
    nif: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    user = db.execute(select(UserORM).where(UserORM.id == user_id)).scalar_one_or_none()

    if user is None:
        raise HTMLResponse(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Usuario no encontrado")
    
    errors = []
    form_data = {
        "nick": nick,
        "email": email,
        "nif": nif,
        "password": password
    }

    if not nick or not nick.strip():
        errors.append("El nombre de usuario no puede estar vacío")
    
    if not email or not email.strip():
        errors.append("El email no puede estar vacío")
    
    nif_value = None
    if nif and nif.strip():
        nif_value = nif

    if not password and not password.strip():
        errors.append("La contraseña no puede estar vacía")

    
    if errors:
        return templates.TemplateResponse(
            "user/form.html",
            {"request": request, "user": None, "errors": errors, "form_data": form_data}
        )  

    try:

        user.nick=nick.strip()
        user.email=email.strip()
        user.nif=nif_value
        user.password=password

        db.commit()
        db.refresh(user)

        return RedirectResponse(url=f"/admin/user/{user.id}/edit", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"No se ha podido editar el usuario con exito: {str(e)}")
        return templates.TemplateResponse(
            "user/form.html",
            {"request": request, "user": None, "errors": errors, "form_data": form_data}
        ) 

# Delete user

@router.post("/user/{user_id}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == user_id)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - El usuario no existe")
    
    db.delete(user)
    db.commit()

    return RedirectResponse(url="/admin/user", status_code=303)



#--------------------------DEVELOPER------------------------------

# list developer


@router.get("/developer", response_class=HTMLResponse)
def list_developers(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    """Muestra la lista de todas las desarrolladoras, ordenadas alfabéticamente."""
    developers = db.execute(select(DevORM).order_by(DevORM.name.asc())).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        
        "admin/developer.html",
        {"request": request, "developers": developers, "result": result, "q": q}
    )



# Create dev



@router.get("/developer/new", response_class=HTMLResponse)
def show_form_create(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    """Muestra el formulario para crear una nueva desarrolladora."""


    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        
        "developer/form.html",
        {"request": request, "developer": None, "errors": None, "form_data": None, "result": result, "q": q}
    )


# Post Create dev

@router.post("/developer/new", response_class=HTMLResponse)
def create_developer(
    request: Request,
    name: str = Form(...),
    image_url: str = Form(None),
    db: Session = Depends(get_db)
):
    #Valida y crea una nueva desarrolladora en la base de datos.
    
    errors = []
    form_data = {
        "name": name,
        "image_url": image_url
    }

    # Validación
    if not name or not name.strip():
        errors.append("El nombre no puede estar vacío.")

    image_url_value = None
    if image_url and image_url.strip():
        image_url_value = image_url
    
    # Comprobar si ya existe una desarrolladora con ese nombre
    if not errors:
        existing_dev = db.execute(select(DevORM).where(DevORM.name == name.strip())).scalar_one_or_none()
        if existing_dev:
            errors.append(f"Ya existe una desarrolladora con el nombre '{name}'.")

    if errors:
        return templates.TemplateResponse(
            "developer/form.html",
            {"request": request, "developer": None, "errors": errors, "form_data": form_data}
        )
    
    try:
        new_dev = DevORM(name=name.strip())
        db.add(new_dev)
        db.commit()
        db.refresh(new_dev)

        # Redirige a la página de detalle de la nueva desarrolladora
        return RedirectResponse(url=f"/developers/{new_dev.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"No se pudo crear la desarrolladora: {str(e)}")
        return templates.TemplateResponse(
            "developer/form.html",
            {"request": request, "developer": None, "errors": errors, "form_data": form_data}
        )
    

# Edit developer


@router.get("/developer/{developer_id}/edit", response_class=HTMLResponse)
def show_form_edit(request: Request, developer_id: int, q: str | None = None, db: Session = Depends(get_db)):
    """Muestra el formulario para editar una desarrolladora existente."""
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()

    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")
    
    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()
    
    return templates.TemplateResponse(
        # Usa el mismo formulario de creación
        "developer/form.html",
        {"request": request, "developer": developer, "result": result, "q": q}
    )


@router.post("/developer/{developer_id}/edit", response_class=HTMLResponse)
def edit_developer(
    request: Request,
    developer_id: int,
    name: str = Form(...),
    image_url: str = Form(None),
    db: Session = Depends(get_db)
):
    #Valida y actualiza una desarrolladora existente en la base de datos.
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()
    
    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")
    
    errors = []
    form_data = {"name": name,
                 "image_url": image_url
                 }

    # Validación
    if not name or not name.strip():
        form_data["name"] = developer.name
        errors.append("El nombre no puede estar vacío.")
    
    image_url_value = None
    if image_url and image_url.strip():
        image_url_value = image_url.strip()

    if errors:
        
        return templates.TemplateResponse(
            "developer/form.html",
            {"request": request, "developer": developer, "errors": errors, "form_data": form_data}
        )
    
    try:
        developer.name = name.strip()
        developer.image_url = image_url_value
        db.commit()
        db.refresh(developer)

        # Redirige a la página de detalle de la desarrolladora editada
        return RedirectResponse(url=f"/developers/{developer.id}", status_code=303)
    
    except Exception as e:
        db.rollback()
        errors.append(f"No se pudo actualizar la desarrolladora: {str(e)}")
        return templates.TemplateResponse(
            "developer/form.html",
            {"request": request, "developer": developer, "errors": errors, "form_data": form_data}
        )

#Eliminar Developer
@router.post("/developer/{developer_id}/delete", status_code=status.HTTP_303_SEE_OTHER)
def delete_developer(developer_id: int, db: Session = Depends(get_db)):
    #Elimina una desarrolladora de la base de datos y redirige a la lista.
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()

    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")

    # Nota: Hay que ver que hacemos si hay videojuegos asociados a una desarroladora al eliminar la desarrolladora.
    
    db.delete(developer)
    db.commit()

    # Redirige a la lista de desarrolladoras
    return RedirectResponse(url="/admin/developer", status_code=303)