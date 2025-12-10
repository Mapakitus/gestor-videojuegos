from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.developer import DevORM
from app.models.videogame import VideogameORM


templates = Jinja2Templates(directory="app/templates")

# Creación del router con prefijo /developers
router = APIRouter(prefix="/developers", tags=["web-developers"])


@router.get("", response_class=HTMLResponse)
def list_developers(request: Request, db: Session = Depends(get_db)):
    """Muestra la lista de todas las desarrolladoras, ordenadas alfabéticamente."""
    developers = db.execute(select(DevORM).order_by(DevORM.name.asc())).scalars().all()

    return templates.TemplateResponse(
        
        "developer/list.html",
        {"request": request, "developers": developers}
    )


@router.get("/new", response_class=HTMLResponse)
def show_form_create(request: Request):
    """Muestra el formulario para crear una nueva desarrolladora."""
    return templates.TemplateResponse(
        
        "developer/form.html",
        {"request": request, "developer": None, "errors": None, "form_data": None}
    )


@router.post("/new", response_class=HTMLResponse)
def create_developer(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    #Valida y crea una nueva desarrolladora en la base de datos.
    
    errors = []
    form_data = {"name": name}

    # Validación
    if not name or not name.strip():
        errors.append("El nombre no puede estar vacío.")
    
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



@router.get("/{developer_id}", response_class=HTMLResponse)
def detail_developer(request: Request, developer_id: int, db: Session = Depends(get_db)):
    """Muestra el detalle de una desarrolladora específica."""
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()
    games_dev = db.execute(select(VideogameORM).where(VideogameORM.developer_id == developer_id)).scalars().all()

    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")
    
    return templates.TemplateResponse(
        
        "developer/detail.html",
        {"request": request, "developer": developer, "games_dev": games_dev}
    )


@router.get("/{developer_id}/edit", response_class=HTMLResponse)
def show_form_edit(request: Request, developer_id: int, db: Session = Depends(get_db)):
    """Muestra el formulario para editar una desarrolladora existente."""
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()

    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")
    
    return templates.TemplateResponse(
        # Usa el mismo formulario de creación
        "developer/form.html",
        {"request": request, "developer": developer, "errors": None, "form_data": None}
    )


@router.post("/{developer_id}/edit", response_class=HTMLResponse)
def edit_developer(
    request: Request,
    developer_id: int,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    #Valida y actualiza una desarrolladora existente en la base de datos.
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()
    
    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")
    
    errors = []
    form_data = {"name": name}

    # Validación
    if not name or not name.strip():
        errors.append("El nombre no puede estar vacío.")

    if errors:
        
        return templates.TemplateResponse(
            "developer/form.html",
            {"request": request, "developer": developer, "errors": errors, "form_data": form_data}
        )
    
    try:
        developer.name = name.strip()
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
@router.post("/{developer_id}/delete", status_code=status.HTTP_303_SEE_OTHER)
def delete_developer(developer_id: int, db: Session = Depends(get_db)):
    #Elimina una desarrolladora de la base de datos y redirige a la lista.
    developer = db.execute(select(DevORM).where(DevORM.id == developer_id)).scalar_one_or_none()

    if developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Desarrolladora no encontrada")

    # Nota: Hay que ver que hacemos si hay videojuegos asociados a una desarroladora al eliminar la desarrolladora.
    
    db.delete(developer)
    db.commit()

    # Redirige a la lista de desarrolladoras
    return RedirectResponse(url="/developers", status_code=303)