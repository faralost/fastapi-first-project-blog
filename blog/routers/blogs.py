from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import get_db

router = APIRouter()


@router.get('/blog', response_model=dict[str, list[schemas.BlogDetail]], tags=['Blog'])
def blogs_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {'data': blogs}


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, text=blog.text, author_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'blog': new_blog}


@router.get('/blog/{blog_id}', response_model=dict[str, schemas.BlogDetail], tags=['Blog'])
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    return {'blog': blog}


@router.put('/blog/{blog_id}', tags=['Blog'])
def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog_to_update.update(blog.dict())
    db.commit()
    return {'blog': blog}


@router.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog.delete()
    db.commit()
    return


