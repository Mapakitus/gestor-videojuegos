from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import ReviewORM
from app.schemas.review import ReviewResponse, ReviewCreate, ReviewUpdate, ReviewPatch

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.get("", response_model=list[ReviewResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(ReviewORM)).scalars().all()

@router.get("/{id}", response_model=ReviewResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    review = db.execute(select(ReviewORM).where(ReviewORM.id == id)).scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe review con id {id}")
    return review

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReviewResponse)
def create(review_dto: ReviewCreate, db: Session = Depends(get_db)):
    new_review = ReviewORM(
        rating=review_dto.rating,
        comment=review_dto.comment,
        user_id=review_dto.user_id,
        videogame_id=review_dto.videogame_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.put("/{id}", response_model=ReviewResponse)
def update_full(id: int, review_dto: ReviewUpdate, db: Session = Depends(get_db)):
    review = db.execute(select(ReviewORM).where(ReviewORM.id == id)).scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe review con id {id}")

    update_data = review_dto.model_dump()
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review

@router.patch("/{id}", response_model=ReviewResponse)
def update_partial(id: int, review_dto: ReviewPatch, db: Session = Depends(get_db)):
    review = db.execute(select(ReviewORM).where(ReviewORM.id == id)).scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe review con id {id}")

    update_data = review_dto.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    review = db.execute(select(ReviewORM).where(ReviewORM.id == id)).scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe review con id {id}")

    db.delete(review)
    db.commit()
    return None
