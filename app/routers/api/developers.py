

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.developer import DevORM
from app.schemas.developer import DevCreate, DevPatch, DevResponse, DevUpdate


router = APIRouter(prefix="/developer", tags=["dev"])


@router.get("", response_model=list[DevResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(DevORM)).scalars().all()

@router.get("/{id}", response_model=DevResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    dev = db.execute(select(DevORM).where(DevORM.id == id)).scalar_one_or_none()

    if dev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe la desarrolladora con id {id}")
    
    return dev

@router.post("", response_model=DevResponse)
def create(dev_dto: DevCreate, db: Session = Depends(get_db)):
    
    new_dev = DevORM(
        name=dev_dto.name
    )

    db.add(new_dev)
    db.commit()
    db.refresh(new_dev)

    return new_dev

@router.put("/{id}", response_model=DevResponse)
def update_full(id: int, dev_dto: DevUpdate, db: Session = Depends(get_db)):
    dev = db.execute(select(DevORM).where(DevORM.id == id)).scalar_one_or_none()

    if dev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ninguna desarrolladora con el id {id}")
    
    update_data = dev_dto.model_dump()

    for field, value in update_data.items():
        setattr(dev, field, value)

    db.commit()
    db.refresh(dev)

    return dev

@router.patch("/{id}", response_model=DevResponse)
def update_partial(id: int, dev_dto: DevPatch, db: Session = Depends(get_db)):

    dev = db.execute(select(DevORM).where(DevORM.id == id)).scalar_one_or_none()

    if dev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ninguna desarrolladora con el id {id}")
    
    update_data = dev_dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(dev, field, value)


    db.commit()
    db.refresh(dev)

    return dev

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    dev = db.execute(select(DevORM).where(DevORM.id == id)).scalar_one_or_none()

    if dev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ninguna desarrolladora con el id {id}")
    

    db.delete(dev)
    db.commit()

    return None