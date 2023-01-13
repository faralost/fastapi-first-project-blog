from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog import models, schemas


def get_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return {'data': blogs}


def create_blog(blog: schemas.Blog, db: Session):
    new_blog = models.Blog(title=blog.title, text=blog.text, author_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'blog': new_blog}


def get_one_blog(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    return {'blog': blog}


def update_one_blog(blog_id: int, blog: schemas.Blog, db: Session):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog_to_update.update(blog.dict())
    db.commit()
    return {'blog': blog}


def destroy_blog(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog.delete()
    db.commit()
    return
