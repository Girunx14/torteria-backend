# app/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import UserCreate, Token
from app.utils.security import hash_password, verify_password, create_access_token


def register(db: Session, data: UserCreate) -> User:
    # Verificar que no exista el username
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El usuario '{data.username}' ya existe",
        )

    # Verificar que no exista el email
    existing_email = db.query(User).filter(User.email == data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El email '{data.email}' ya está registrado",
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role or "staff",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, username: str, password: str) -> Token:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo, contacta al administrador",
        )

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )

    return Token(access_token=access_token, token_type="bearer")