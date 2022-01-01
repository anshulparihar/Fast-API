from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .. import schemas,database
from ..repository import user

get_db = database.get_db

router = APIRouter(prefix="/user",tags=['User'])


#Creating User
@router.post('/',response_model=schemas.ShowUser,tags=["User"] )
def createUser(request: schemas.User,db : Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/{id}',response_model=schemas.ShowUser,tags=["User"])
def showUser(id:int, db : Session = Depends(get_db)):
    return user.getUser(id,db) 


