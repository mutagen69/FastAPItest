from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter

from app import models, schemas, database, utils, oauth2


router = APIRouter(
    prefix="",
    tags=['Users']
)

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Регистрация пользователя
    """
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    user_db = db.query(models.User).where(models.User.username==user.username).first()
    if not user_db is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь уже существует")
        
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def login(user_cerd: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Авторизация пользователя
    """
    user = db.query(models.User).filter(models.User.username == user_cerd.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно полномочий")
    if not utils.verify(user_cerd.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно полномочий")
    
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token" : access_token, "token_type": "bearer"}


@router.post('/profile', response_model=schemas.UserResponse)
def get_user(current_user: int = Depends(oauth2.get_current_user)):
    """
    Получение пользователя
    """
    return current_user