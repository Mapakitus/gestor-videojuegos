
from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, select
from app.database import get_db
from app.models.developer import DevORM
from app.models.genre import GenreORM
from app.models.videogame import VideogameORM

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="", tags=["web"])


@router.get("/", response_class=HTMLResponse)
def home(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    videogame = db.execute(select(VideogameORM)).scalars().all()
    last_videogame = db.execute(select(VideogameORM).order_by(VideogameORM.id.desc()).limit(5)).scalars().all()    
    games_action = db.execute(select(VideogameORM).join(VideogameORM.genre).where(GenreORM.name == "Acción").limit(3)).scalars().all()
    games_aventure = db.execute(select(VideogameORM).join(VideogameORM.genre).where(GenreORM.name == "Aventura").limit(3)).scalars().all()
    

    result = None

    if q and q.strip():
        result = db.execute(select(VideogameORM).where(VideogameORM.title.ilike(f"%{q}%"))).scalars().all()


    return templates.TemplateResponse(
        "home.html",
        {"request": request, "videogame": videogame, "last_videogame": last_videogame, "games_action": games_action, "games_aventure": games_aventure, "result": result, "q":q}
    )