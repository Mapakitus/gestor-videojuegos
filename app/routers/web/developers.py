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
def list_developers(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    """Muestra la lista de todas las desarrolladoras, ordenadas alfabéticamente."""
    developers = db.execute(select(DevORM).order_by(DevORM.name.asc())).scalars().all()

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()

    return templates.TemplateResponse(
        
        "developer/list.html",
        {"request": request, "developers": developers, "q":q, "result": result}
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


