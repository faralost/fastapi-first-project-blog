from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, text=blog.text)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'blog': new_blog}


@app.get('/blog')
def blogs_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {'data': blogs}


@app.get('/blog/{blog_id}')
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    return {'blog': blog}


@app.put('/blog/{blog_id}')
def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog_to_update.update(blog.dict())
    db.commit()
    return {'blog': blog}


@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog.delete()
    db.commit()
    return
