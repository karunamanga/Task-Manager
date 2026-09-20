from sqlalchemy.orm import Session

from ..models.user import User
from ..models.user_role import UserRole


class UserRepository:

    def get_user_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create_user(
        self,
        db: Session,
        name: str,
        email: str,
        password_hash: str,
        role_id: int,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
        )

        db.add(user)
        db.flush()

        user_role = UserRole(
            user_id=user.id,
            role_id=role_id,
        )
        db.add(user_role)
        db.commit()
        db.refresh(user)

        return user