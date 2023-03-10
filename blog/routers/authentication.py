from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import get_db
from blog.hashing import verify_password
from blog.token import create_access_token

router = APIRouter(
    tags=['Auth']
)


@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    a_user = db.query(models.User).filter(models.User.email == user.username).first()
    if not a_user or not verify_password(a_user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
