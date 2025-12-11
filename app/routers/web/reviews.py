from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.review import ReviewORM
from app.models.user import UserORM
from app.models.videogame import VideogameORM

router = APIRouter(prefix="/videogame", tags=["web-reviews"])

@router.post("/{game_id}/review")
def create_review(game_id: int, request: Request, rating: int = Form(...), comment: str = Form(None), db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    game = db.get(VideogameORM, game_id)

    if not user or not game:
        raise HTTPException(status_code=404, detail="Usuario o juego no encontrado")

    # evitar duplicados: un usuario, una reseña por juego
    existing = db.execute(
        select(ReviewORM).where(ReviewORM.user_id == user.id, ReviewORM.videogame_id == game_id)
    ).scalar_one_or_none()

    if existing:
        # ya existe, redirigir al detalle (podríamos mostrar mensaje)
        return RedirectResponse(f"/videogame/{game_id}", status_code=303)

    new_review = ReviewORM(
        rating=float(rating),
        comment=comment,
        user_id=user.id,
        videogame_id=game_id
    )
    db.add(new_review)
    db.commit()
    return RedirectResponse(f"/videogame/{game_id}", status_code=303)


@router.post("/{game_id}/review/edit")
def edit_review(game_id: int, request: Request, rating: int = Form(...), comment: str = Form(None), db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    review = db.execute(
        select(ReviewORM).where(ReviewORM.user_id == user.id, ReviewORM.videogame_id == game_id)
    ).scalar_one_or_none()

    if not review:
        # no hay reseña que editar
        return RedirectResponse(f"/videogame/{game_id}", status_code=303)

    review.rating = float(rating)
    review.comment = comment
    db.commit()
    return RedirectResponse(f"/videogame/{game_id}", status_code=303)


@router.post("/{game_id}/review/delete")
def delete_review(game_id: int, request: Request, db: Session = Depends(get_db)):
    USER_ID = 2
    user = db.get(UserORM, USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    review = db.execute(
        select(ReviewORM).where(ReviewORM.user_id == user.id, ReviewORM.videogame_id == game_id)
    ).scalar_one_or_none()

    if review:
        db.delete(review)
        db.commit()

    return RedirectResponse(f"/videogame/{game_id}", status_code=303)
