
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.genre import GenreORM
from app.models.videogame import VideogameORM

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="", tags=["web"])


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    videogame = db.execute(select(VideogameORM)).scalars().all()
    last_videogame = db.execute(select(VideogameORM).order_by(VideogameORM.id.desc()).limit(5)).scalars().all()    
    games_action = db.execute(select(VideogameORM).join(VideogameORM.genre).where(GenreORM.name == "Acción").limit(3)).scalars().all()
    games_aventure = db.execute(select(VideogameORM).join(VideogameORM.genre).where(GenreORM.name == "Aventura").limit(3)).scalars().all()
    
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "videogame": videogame, "last_videogame": last_videogame, "games_action": games_action, "games_aventure": games_aventure}
    )
