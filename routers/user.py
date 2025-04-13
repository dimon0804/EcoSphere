from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

# Секрет и алгоритм для JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # Извлекаем id пользователя
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Выполняем запрос к базе данных асинхронно
        result = await db.execute(select(User).filter(User.email == user_id))
        user = result.scalar_one_or_none()  # Применяем await для получения результата
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # user.created_at = user.created_at.isoformat()
        return user

    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter((User.email == user.email) | (User.username == user.username)))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким email или username уже существует")

        hashed_password = User.hash_password(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при регистрации пользователя: {str(e)}")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Выполняем запрос для получения пользователя
    result = await db.execute(select(User).filter(
    (User.email == form_data.username) | 
    (User.username == form_data.username)
    ))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    # Проверяем пароль с помощью метода verify_password
    if not User.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    # Генерация JWT токена
    access_token = create_access_token(
    data={"sub": user.email},
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_user_data(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/update", response_model=UserResponse)
async def update_user_data(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Обновляем поля, если они переданы
        if update_data.eco_wallet_balance is not None:
            current_user.eco_wallet_balance = update_data.eco_wallet_balance

        # Добавь другие поля, если нужно (аналогично)

        await db.commit()
        await db.refresh(current_user)
        return current_user

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обновлении данных: {str(e)}")