from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from blog.routers import token
from blog.routers.oauth2 import get_current_user
from .. import schemas,database
from typing import List
from ..repository import blog
from . import oauth2
get_db = database.get_db


router = APIRouter(prefix="/blog",tags=['Blogs'])

#getting all the blogs from the database
@router.get('/',response_model=List[schemas.ShowBlog],tags=["Blogs"])
def getblog( db : Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.getBlog(db)


 #Creating new blog and storing it in the database
@router.post('/',status_code=status.HTTP_201_CREATED,tags=["Blogs"])
def create(request : schemas.Blog, db : Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):     #db is the database instance
    return blog.create(request,db)


#getting blog with id
@router.get('/{id}',response_model=schemas.ShowBlog, status_code= 200,tags=["Blogs"])
def showblog(id,db : Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.blogwithID(id,db)

#deleting the blog
@router.delete('/{id}',status_code=status.HTTP_404_NOT_FOUND,tags=["Blogs"])
def deleteblog(id,db : Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id,db)


#updating the blog
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def updateblog(id, request:schemas.Blog, db : Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db)
