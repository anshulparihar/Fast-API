from fastapi import FastAPI,Depends
# from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import schemas,models
from .database import engine,SessionLocal
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog')
def create(request : schemas.Blog, db : Session = Depends(get_db)):
    #Creating new blog
    new_blog = models.Blog(title = request.title,body = request.body )     #request.title because of its connection between request and schemas.py
    db.add(new_blog)    #adding new blog
    db.commit()         #commiting new blog
    db.refresh(new_blog)    #refreshing the blog
    return new_blog