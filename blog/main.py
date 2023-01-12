from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import engine, SessionLocal
from blog.hashing import hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, text=blog.text, author_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'blog': new_blog}


@app.get('/blog', response_model=dict[str, list[schemas.BlogDetail]], tags=['Blog'])
def blogs_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {'data': blogs}


@app.get('/blog/{blog_id}', response_model=dict[str, schemas.BlogDetail], tags=['Blog'])
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    return {'blog': blog}


@app.put('/blog/{blog_id}', tags=['Blog'])
def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog_to_update.update(blog.dict())
    db.commit()
    return {'blog': blog}


@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such blog.')
    blog.delete()
    db.commit()
    return


@app.post(
    '/user',
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, schemas.UserDetail],
    tags=['User']
)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'user': new_user}


@app.get('/user/{user_id}', response_model=dict[str, schemas.UserDetail], tags=['User'])
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such user.')
    return {'user': user}
