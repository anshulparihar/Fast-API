from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from .. import schemas,models,database,hashing
from ..repository import user
from typing import List

get_db = database.get_db

router = APIRouter(prefix="/user",tags=['User'])


#Creating User
@router.post('/',response_model=schemas.ShowUser,tags=["User"] )
def createUser(request: schemas.User,db : Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/{id}',response_model=schemas.ShowUser,tags=["User"])
def showUser(id:int, db : Session = Depends(get_db)):
    return user.getUser(id,db) 


