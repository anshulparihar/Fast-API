from datetime import timedelta
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session

from blog.routers.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .. import schemas,database,models,hashing
from . import token

get_db = database.get_db
router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(request:schemas.Login,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")


#verifying password
    if not hashing.Hash.verify(request.password,user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    
#generate JWT token

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}