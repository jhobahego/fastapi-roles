from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from config.deps import get_db

from crud.crud_user import user as crud_user
from schemas.User import UserCreate, User as UserSchema
from schemas.Role import Role
from models.User import User

router = APIRouter()


@router.get("/users", tags=["Users"], response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db), *, skip: int = 0, limit: int = 100):
    return db.query(User).options(joinedload(User.roles)).offset(skip).limit(limit).all()


@router.post("/users", tags=["Users"], response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud_user.create(db, user=user)
    except IntegrityError as e:
        error_message = e.args[0]

        field_error = error_message.split("'")[3]
        field_value = error_message.split("'")[1]
        db.rollback()
        raise HTTPException(status_code=400, detail=f"El {field_error}: {field_value} ya fue registrado")
    except Exception as e:
        # Si ocurre un error, hacer rollback de la transacción y devolver un error HTTP
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error al crear el usuario")


@router.get("/users/{id}", tags=["Users"], response_model=UserSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.roles)).filter(User.id == id).first()

    if not user:
        return HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


@router.get("/users/{user_id}/roles", tags=["Users"], response_model=list[Role])
def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.roles)).filter(User.id == user_id).first()
    if user:
        return user.roles
    return HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/users/{id}", tags=["Users"], status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud_user.remove(db=db, id=id)

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
