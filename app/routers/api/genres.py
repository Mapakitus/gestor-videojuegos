from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.schemas.genre import GenreResponse, GenreCreate, GenreUpdate, GenrePatch
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.genre import GenreORM

# create router for endpoints
router = APIRouter(prefix="/api/generos", tags=["generos"])

# GET - retrieve ALL genres
@router.get("", response_model=list[GenreResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(GenreORM)).scalars().all()

@router.get("/{id}", response_model=GenreResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == id)).scalar_one_or_none()

    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún género con el id {id}")
    
    return genre

@router.post("",status_code=status.HTTP_201_CREATED, response_model=GenreResponse)
def create(genre_dto: GenreCreate, db: Session = Depends(get_db)):
    new_genre = GenreORM(
        name=genre_dto.name,
        description=genre_dto.description
    )

    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)

    return new_genre

@router.put("/{id}", response_model=GenreResponse)
def update_full(id: int, genre_dto: GenreUpdate, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == id)).scalar_one_or_none()
    
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el género con el id {id}")
    
    # store the dictionary obtained from genre_dto
    update_data = genre_dto.model_dump()

    # loop to assign the dictionary values to each attribute
    for field, value in update_data.items():
        setattr(genre, field, value)

    db.commit()
    db.refresh(genre)
    return genre

@router.patch("/{id}", response_model=GenreResponse)
def update_partial(id: int, genre_dto: GenrePatch, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == id)).scalar_one_or_none()

    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el género con el id {id}")
   
    update_data = genre_dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(genre, field, value)

    db.commit()
    db.refresh(genre)
    return genre

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    genre = db.execute(select(GenreORM).where(GenreORM.id == id)).scalar_one_or_none()

    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el género con el id {id}")
    
    db.delete(genre)
    db.commit()
    return None