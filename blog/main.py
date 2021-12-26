from fastapi import FastAPI,Depends,status,Response,HTTPException  #status helps us to get the http status of different get, post type function
# from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import schemas,models
from .database import engine,SessionLocal
from .hashing import Hash
from typing import List,Dict
from pydantic import BaseModel, ValidationError, validator
# from passlib.context import CryptContext
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


 #Creating new blog and storing it in the database
@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=["Blogs"])
def create(request : schemas.Blog, db : Session = Depends(get_db)):     #db is the database instance
   
    new_blog = models.Blog(title = request.title,body = request.body,user_id =1 )     #request.title because of its connection between request and schemas.py
    db.add(new_blog)    #adding new blog
    db.commit()         #commiting new blog
    db.refresh(new_blog)    #refreshing the blog
    return new_blog

#getting all the blogs from the database
@app.get('/blog',response_model=List[schemas.ShowBlog],tags=["Blogs"])
def getblog( db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#getting blog with id

@app.get('/blog/{id}',response_model=schemas.ShowBlog, status_code= 200,tags=["Blogs"])

def showblog(id,db : Session = Depends(get_db)):
    print(List[schemas.ShowBlog])
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    #blog = db.query(models.Blog).first()
    #if we have an ID not available and we need to print the message we can do this my two methods
    #1. using Response
    '''if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"details" : f"There is not blog available of id:{id}"}'''
    #2. Using HTTPException
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no blog available of id:{id}")
    return blog 


#deleting the blog
@app.delete('/blog/{id}',status_code=status.HTTP_404_NOT_FOUND,tags=["Blogs"])
def deleteblog(id,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no blog available of id:{id}")
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return {'Blog Deleted': f"Blog with id : {id} is been deleted"}


#updating the blog
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def updateblog(id, request:schemas.Blog, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    request = dict(request)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} not found')
    blog.update(request)
    db.commit()
    return "UPDATED"

#Hashing password for the user
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Creating User
@app.post('/user',response_model=schemas.ShowUser,tags=["User"] )
def createUser(request: schemas.User,db : Session = Depends(get_db)):
    # hashedPassword = pwd_context.hash(request.password)
    new_user = models.User(name = request.name,email = request.email,password = Hash.bcrypt(request.password) )     #request.title because of its connection between request and schemas.py
    db.add(new_user)    #adding new user
    db.commit()         #commiting new user
    db.refresh(new_user)    #refreshing the database
    #return (f'{request.name} Created')
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=["User"])
def showUser(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no user available of id:{id}")
    return user 


