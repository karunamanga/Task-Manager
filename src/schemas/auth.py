from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=6)


class RegisterResponse(BaseModel):
    message: str
    user_id: int
    email: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    message: str
    name: str
    user_id: int
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str

