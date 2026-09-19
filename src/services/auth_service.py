from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from ..models.user import User
from ..repositories.user_repository import UserRepository


class AuthService:

    def __init__(self):
        self.repository = UserRepository()
        self.password_hash = PasswordHash.recommended()

    def register_user(
        self,
        db: Session,
        name: str,
        email: str,
        password: str,
    ) -> User | None:
        existing_user = self.repository.get_user_by_email(
            db,
            email,
        )

        if existing_user:
            return None

        hashed_password = self.password_hash.hash(password)

        return self.repository.create_user(
            db,
            name,
            email,
            hashed_password,
        )

    def login_user(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> User | None:
        user = self.repository.get_user_by_email(
            db,
            email,
        )

        if user is None:
            return None

        is_valid = self.password_hash.verify(
            password,
            user.password_hash,
        )

        if not is_valid:
            return None

        return user