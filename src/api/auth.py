from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db

from ..schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)

from ..services.auth_service import AuthService

from ..auth import (
    create_access_token,
    create_refresh_token,
    get_user_id_from_refresh_token,
)


router = APIRouter()

service = AuthService()


@router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = service.register_user(
        db,
        user_data.name,
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
        "email": user.email,
        "name": user.name
    }


@router.post(
    "/auth/login",
    response_model=LoginResponse
)
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

    refresh_token = create_refresh_token(user.id)

    return {
        "message": "Login successful",
        "name": user.name,
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post(
    "/auth/refresh",
    response_model=RefreshTokenResponse
)
def refresh_access_token(
    data: RefreshTokenRequest,
):
    user_id = get_user_id_from_refresh_token(
        data.refresh_token
    )

    access_token = create_access_token(user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
