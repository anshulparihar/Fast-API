from sys import prefix
from fastapi import APIRouter,Depends,status,HTTPException#status helps us to get the http status of different get, post type function
from sqlalchemy.orm import Session
from .. import schemas,models,database
from typing import List

get_db = database.get_db

router = APIRouter(prefix="/blog",tags=['Blogs'])

#getting all the blogs from the database
@router.get('/',response_model=List[schemas.ShowBlog],tags=["Blogs"])
def getblog( db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


 #Creating new blog and storing it in the database

@router.post('/',status_code=status.HTTP_201_CREATED,tags=["Blogs"])
def create(request : schemas.Blog, db : Session = Depends(get_db)):     #db is the database instance
   
    new_blog = models.Blog(title = request.title,body = request.body,user_id =1 )     #request.title because of its connection between request and schemas.py
    db.add(new_blog)    #adding new blog
    db.commit()         #commiting new blog
    db.refresh(new_blog)    #refreshing the blog
    return new_blog


@router.get('/',response_model=List[schemas.ShowBlog],tags=["Blogs"])
def getblog( db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#getting blog with id
@router.get('/{id}',response_model=schemas.ShowBlog, status_code= 200,tags=["Blogs"])
def showblog(id,db : Session = Depends(get_db)):
    print(List[schemas.ShowBlog])
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no blog available of id:{id}")
    return blog 

#deleting the blog
@router.delete('/{id}',status_code=status.HTTP_404_NOT_FOUND,tags=["Blogs"])
def deleteblog(id,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no blog available of id:{id}")
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return {'Blog Deleted': f"Blog with id : {id} is been deleted"}


#updating the blog
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def updateblog(id, request:schemas.Blog, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    request = dict(request)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} not found')
    blog.update(request)
    db.commit()
    return "UPDATED"
