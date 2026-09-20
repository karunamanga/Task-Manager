from sqlalchemy.orm import Session

from ..models.user import User


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
            role_id=role_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user