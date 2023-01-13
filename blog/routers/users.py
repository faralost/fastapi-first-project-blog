from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import get_db
from blog.hashing import hash_password

router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=dict[str, schemas.UserDetail], tags=['User'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'user': new_user}


@router.get('/user/{user_id}', response_model=dict[str, schemas.UserDetail], tags=['User'])
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such user.')
    return {'user': user}
