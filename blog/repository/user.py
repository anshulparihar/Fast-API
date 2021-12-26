from sqlalchemy.orm import Session
from .. import models,schemas,hashing
from typing import List
from fastapi import HTTPException,status

def create(request: schemas.User,db : Session):
    new_user = models.User(name = request.name,email = request.email,password = hashing.Hash.bcrypt(request.password))     #request.title because of its connection between request and schemas.py
    db.add(new_user)    #adding new user
    db.commit()         #commiting new user
    db.refresh(new_user)    #refreshing the database
    #return (f'{request.name} Created')
    return new_user

def getUser(id:int, db : Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no user available of id:{id}")
    return user