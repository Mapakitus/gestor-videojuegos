from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserORM
from app.schemas.user import UserResponse, UserCreate, UserUpdate, UserPatch


router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=list[UserResponse])
def find_all(db: Session = Depends(get_db)):
    users = db.execute(select(UserORM)).scalars().all()

    return users

@router.get("/{id}", response_model=UserResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún usuario con el id {id}")
    
    return user

@router.post("", response_model=UserResponse)
def create(user_dto: UserCreate, db: Session = Depends(get_db)):
    new_user = UserORM(
        nick=user_dto.nick,
        email=user_dto.email,
        nif=user_dto.nif,
        password=user_dto.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/{id}", response_model=UserResponse)
def update_full(id: int, user_dto: UserUpdate, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el usuario con id {id}")

    new_data = user_dto.model_dump()

    for field, value in new_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

@router.patch("/{id}", response_model=UserResponse)
def update_partial(id: int, user_dto: UserPatch, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el usuario con id {id}")
    
    new_data = user_dto.model_dump(exclude_unset=True)

    for field, value in new_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe el usuario con id {id}")
    
    db.delete(user)
    db.commit()
    
    return None