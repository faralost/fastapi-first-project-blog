from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from blog import schemas
from blog.database import get_db
from blog.oauth2 import get_current_user
from blog.services.user_services import get_all_users, create_user, get_one_user

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get('/', response_model=dict[str, list[schemas.UserDetailInBlog]])
def users_list(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=dict[str, schemas.UserDetail])
def add_user(user: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return create_user(user, db)


@router.get('/{user_id}', response_model=dict[str, schemas.UserDetail])
def user_detail(user_id: int, db: Session = Depends(get_db)):
    return get_one_user(user_id, db)
