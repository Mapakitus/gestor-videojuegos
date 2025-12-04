

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserORM


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/users", tags=["web"])

@router.get("", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    users = db.execute(select(UserORM)).scalars().all()

    return templates.TemplateResponse(
        "user/list.html",
        {"request": request, "users": users}
    )

@router.get("/{user_id}", response_class=HTMLResponse)
def detail_by_id(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == user_id)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún usuario con el id {user_id}")
    
    return templates.TemplateResponse(
        "user/detail.html",
        {"request": request, "user": user}
    )

