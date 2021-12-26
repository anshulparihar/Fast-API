from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from .. import schemas,models,database,hashing

from typing import List

get_db = database.get_db

router = APIRouter(prefix="/user",tags=['User'])


#Creating User
@router.post('/',response_model=schemas.ShowUser,tags=["User"] )
def createUser(request: schemas.User,db : Session = Depends(get_db)):
    # hashedPassword = pwd_context.hash(request.password)
    new_user = models.User(name = request.name,email = request.email,password = hashing.Hash.bcrypt(request.password))     #request.title because of its connection between request and schemas.py
    db.add(new_user)    #adding new user
    db.commit()         #commiting new user
    db.refresh(new_user)    #refreshing the database
    #return (f'{request.name} Created')
    return new_user

@router.get('/{id}',response_model=schemas.ShowUser,tags=["User"])
def showUser(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no user available of id:{id}")
    return user 


