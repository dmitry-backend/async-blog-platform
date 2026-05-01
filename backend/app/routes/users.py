from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.validators import validate_email, validate_password
from app.tasks.email_tasks import send_welcome_email
from app.crud import users as crud_users
from app.schemas import UserCreate, UserRead, UserLogin, Token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    if not validate_email(payload.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not validate_password(payload.password):
        raise HTTPException(status_code=400, detail="Weak password")
    if await crud_users.get_user_by_email(session, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await crud_users.create_user(session, payload.email, hash_password(payload.password))
    send_welcome_email.delay(user.email)
    return user

@router.post("/login", response_model=Token)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await crud_users.get_user_by_email(session, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
