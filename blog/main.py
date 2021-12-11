from fastapi import FastAPI,Depends,status  #status helps us to get the http status of different get, post type function
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


 #Creating new blog and storing it in the database
@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request : schemas.Blog, db : Session = Depends(get_db)):     #db is the database instance
   
    new_blog = models.Blog(title = request.title,body = request.body )     #request.title because of its connection between request and schemas.py
    db.add(new_blog)    #adding new blog
    db.commit()         #commiting new blog
    db.refresh(new_blog)    #refreshing the blog
    return new_blog

#getting all the blogs from the database
@app.get('/blog')
def getblog( db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#getting blog with id
@app.get('/blog/{id}')
def showblog(id,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    #blog = db.query(models.Blog).first()
    return blog 
