from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status #status helps us to get the http status of different get, post type function

def getBlog(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request :schemas.Blog,db:Session):
    new_blog = models.Blog(title = request.title,body = request.body,user_id =1 )     #request.title because of its connection between request and schemas.py
    db.add(new_blog)    #adding new blog
    db.commit()         #commiting new blog
    db.refresh(new_blog)    #refreshing the blog
    return new_blog


def blogwithID(id,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no blog available of id:{id}")
    
    return blog


def delete(id,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no blog available of id:{id}")
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    message = {'Blog Deleted': f"Blog with id : {id} is been deleted"}
    return message
    

def update(id, request:schemas.Blog, db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    request = dict(request)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} not found')
    blog.update(request)
    db.commit()
    return "Updated"