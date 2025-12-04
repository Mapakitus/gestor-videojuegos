from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserORM
from app.models.videogame import VideogameORM
from app.schemas.user import UserResponse, UserCreate, UserUpdate, UserPatch
from app.schemas.videogame import VideogameResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=list[UserResponse])
def find_all(db: Session = Depends(get_db)):
    users = db.execute(select(UserORM)).scalars().all()

    result = []
    for user in users:
        user_copy = UserResponse.model_validate(user)  # en vez de from_orm
        # Filtrar reviews de cada videojuego para el usuario
        user_videogames = []
        for vg in user.videogames:
            filtered_reviews = [r for r in vg.reviews if r.user_id == user.id]
            vg_copy = VideogameResponse.model_validate(vg)
            vg_copy.reviews = filtered_reviews
            user_videogames.append(vg_copy)
        user_copy.videogames = user_videogames

        result.append(user_copy)

    return result

@router.get("/{id}", response_model=UserResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe ningún usuario con el id {id}")
    
    # Filtrar reviews por usuario
    user_videogames = []
    for vg in user.videogames:
        filtered_reviews = [r for r in vg.reviews if r.user_id == user.id]
        vg_copy = VideogameResponse.model_validate(vg)
        vg_copy.reviews = filtered_reviews
        user_videogames.append(vg_copy)

    user_copy = UserResponse.model_validate(user)
    user_copy.videogames = user_videogames

    return user_copy

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

# ==================================================
#        ENDPOINTS PARA BIBLIOTECA DE JUEGOS
# ==================================================

# Obtener todos los videojuegos que posee un usuario
@router.get("/{id}/games", response_model=list[VideogameResponse])
def get_user_games(id: int, db: Session = Depends(get_db)):
    user = db.get(UserORM, id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    return user.videogames


# Añadir un videojuego a la biblioteca del usuario
@router.post("/{id}/games/{game_id}", status_code=201)
def add_game_to_user(id: int, game_id: int, db: Session = Depends(get_db)):
    user = db.get(UserORM, id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    game = db.get(VideogameORM, game_id)
    if not game:
        raise HTTPException(404, "Videojuego no encontrado")

    if game in user.videogames:
        raise HTTPException(400, "El usuario ya posee este juego")

    user.videogames.append(game)
    db.commit()

    return {"message": "Videojuego añadido a la biblioteca"}


# Eliminar un videojuego de la biblioteca del usuario
@router.delete("/{id}/games/{game_id}", status_code=204)
def remove_game_from_user(id: int, game_id: int, db: Session = Depends(get_db)):
    user = db.get(UserORM, id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    game = db.get(VideogameORM, game_id)
    if not game:
        raise HTTPException(404, "Videojuego no encontrado")

    if game not in user.videogames:
        raise HTTPException(400, "El usuario no posee este juego")

    # Eliminar reviews del usuario en ese juego, para que no se queden huérfanas al eliminar un videjuego de tu biblioteca
    reviews_to_delete = [r for r in game.reviews if r.user_id == user.id]
    for r in reviews_to_delete:
        db.delete(r)
        
   # Eliminar el juego de la biblioteca del usuario     
    user.videogames.remove(game)
    db.commit()
    return None