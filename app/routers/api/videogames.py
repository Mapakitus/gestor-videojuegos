from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.videogame import Videogame
from app.schemas.videogame import VideogameResponse, VideogameCreate, VideogameUpdate, VideogamePatch

# crear router para endpoints de videojuegos
router = APIRouter(prefix="/api/videogames", tags=["videogames"])

# GET - retrieve ALL videogames
@router.get("", response_model=list[VideogameResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Videogame)).scalars().all()

# GET - retrieve videogame by id
@router.get("/{id}", response_model=VideogameResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    videogame = db.execute(select(Videogame).where(Videogame.id == id)).scalar_one_or_none()

    if not videogame:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún videojuego con el id {id}")
    
    return videogame

# POST - create a new videogame
@router.post("", status_code=status.HTTP_201_CREATED, response_model=VideogameResponse)
def create(videogame_dto: VideogameCreate, db: Session = Depends(get_db)):
    new_videogame = Videogame(
        title=videogame_dto.title,
        description=videogame_dto.description,
        genre_id=videogame_dto.genre_id,
        developer_id=videogame_dto.developer_id
    )

    db.add(new_videogame)
    db.commit()
    db.refresh(new_videogame)

    return new_videogame

# PUT - update full videogame
@router.put("/{id}", response_model=VideogameResponse)
def update_full(id: int, videogame_dto: VideogameUpdate, db: Session = Depends(get_db)):
    videogame = db.execute(select(Videogame).where(Videogame.id == id)).scalar_one_or_none()

    if not videogame:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el videojuego con el id {id}")

    update_data = videogame_dto.model_dump()

    for field, value in update_data.items():
        setattr(videogame, field, value)

    db.commit()
    db.refresh(videogame)
    return videogame

# PATCH - update partial videogame
@router.patch("/{id}", response_model=VideogameResponse)
def update_partial(id: int, videogame_dto: VideogamePatch, db: Session = Depends(get_db)):
    videogame = db.execute(select(Videogame).where(Videogame.id == id)).scalar_one_or_none()

    if not videogame:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el videojuego con el id {id}")

    update_data = videogame_dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(videogame, field, value)

    db.commit()
    db.refresh(videogame)
    return videogame

# DELETE - remove a videogame
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    videogame = db.execute(select(Videogame).where(Videogame.id == id)).scalar_one_or_none()

    if not videogame:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el videojuego con el id {id}")

    db.delete(videogame)
    db.commit()
    return None
