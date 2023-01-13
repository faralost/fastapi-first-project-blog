from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from blog import schemas
from blog.database import get_db
from blog.oauth2 import get_current_user
from blog.services.blog_services import get_all_blogs, create_blog, get_one_blog, update_one_blog, destroy_blog

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)


@router.get('/', response_model=dict[str, list[schemas.BlogDetail]])
def blogs_list(db: Session = Depends(get_db)):
    return get_all_blogs(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_blog(blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return create_blog(blog, db)


@router.get('/{blog_id}', response_model=dict[str, schemas.BlogDetail])
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    return get_one_blog(blog_id, db)


@router.put('/{blog_id}')
def update_blog(
        blog_id: int,
        blog: schemas.Blog,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    return update_one_blog(blog_id, blog, db)


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return destroy_blog(blog_id, db)
