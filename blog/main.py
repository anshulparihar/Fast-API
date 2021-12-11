from fastapi import FastAPI,Depends,status,Response,HTTPException  #status helps us to get the http status of different get, post type function
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
@app.get('/blog/{id}',status_code= 200)
def showblog(id, response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    #blog = db.query(models.Blog).first()
    #if we have an ID not available and we need to print the message we can do this my two methods
    #1. using Response
    '''if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details" : f"There is not blog available of id:{id}"}'''
    #2. Using HTTPException
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is not blog available of id:{id}")
    return blog 


#deleting the blog
@app.delete('/blog/{id}',status_code=status.HTTP_404_NOT_FOUND)
def deleteblog(id,db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return {'Blog Deleted': f"Blog with id : {id} is been deleted"}