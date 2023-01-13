from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.config import ACCESS_TOKEN_EXPIRE_MINUTES
from blog.database import get_db
from blog.hashing import verify_password
from blog.token import create_access_token

router = APIRouter(
    tags=['Auth']
)


@router.post('/login')
def login(user: schemas.Login, db: Session = Depends(get_db)):
    a_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not a_user or not verify_password(a_user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
