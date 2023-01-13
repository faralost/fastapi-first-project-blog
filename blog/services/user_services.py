from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog import models, schemas
from blog.hashing import hash_password


def get_all_users(db: Session):
    users = db.query(models.User).all()
    return {'data': users}


def create_user(user: schemas.User, db):
    new_user = models.User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'user': new_user}


def get_one_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such user.')
    return {'user': user}
