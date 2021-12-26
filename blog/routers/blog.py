from sys import prefix
from fastapi import APIRouter,Depends,status,HTTPException#status helps us to get the http status of different get, post type function
from sqlalchemy.orm import Session
from .. import schemas,models,database
from typing import List
from ..repository import blog
get_db = database.get_db

router = APIRouter(prefix="/blog",tags=['Blogs'])

#getting all the blogs from the database
@router.get('/',response_model=List[schemas.ShowBlog],tags=["Blogs"])
def getblog( db : Session = Depends(get_db)):
    return blog.getBlog(db)


 #Creating new blog and storing it in the database
@router.post('/',status_code=status.HTTP_201_CREATED,tags=["Blogs"])
def create(request : schemas.Blog, db : Session = Depends(get_db)):     #db is the database instance
    return blog.create(request,db)


#getting blog with id
@router.get('/{id}',response_model=schemas.ShowBlog, status_code= 200,tags=["Blogs"])
def showblog(id,db : Session = Depends(get_db)):
    return blog.blogwithID(id,db)

#deleting the blog
@router.delete('/{id}',status_code=status.HTTP_404_NOT_FOUND,tags=["Blogs"])
def deleteblog(id,db : Session = Depends(get_db)):
    return blog.delete(id,db)


#updating the blog
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def updateblog(id, request:schemas.Blog, db : Session = Depends(get_db)):
    return blog.update(id,request,db)
