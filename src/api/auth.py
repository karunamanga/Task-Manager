from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db

from ..schemas.auth import RegisterRequest, LoginRequest
from ..services.auth_service import AuthService

from ..auth import create_access_token

router = APIRouter()

service = AuthService()


@router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = service.register_user(
        db,
        user_data.email,
        user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email
    }
@router.post("/auth/login")
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = service.login_user(
        db,
        user_data.email,
        user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }