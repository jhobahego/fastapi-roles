from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session, joinedload

from crud.base import CRUDBase
from models.Role import Role
from models.User import User
from schemas.User import UserCreate, UserUpdate, User as UserSchema
from schemas.Role import Role as RoleSchema, RolName
from config.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserSchema]:
        return db.query(User).options(User.roles).filter(User.email == email).first()

    def create(self, db: Session, *, user: UserCreate) -> UserSchema:
        created_user = User(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
        )

        permissions = ["CHANGE_CREDENTIALS, READ"]
        if user.rol:
            rol_name = user.rol.name
            if rol_name == "MANAGER":
                permissions.extend(["CREATE", "MODIFY", "DELETE"])

            role = Role(name=rol_name, permissions=permissions)
            created_user.roles = [role]
            db.add_all([created_user, role])
            db.commit()

        db.refresh(created_user)
        created_user = db.query(User). \
            options(joinedload(User.roles)). \
            filter(User.id == created_user.id). \
            first()

        return created_user

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        role: RoleSchema = user.roles[0]

        return role.name == RolName.MANAGER


user = CRUDUser(User)
