from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, schema, models, oauth2
from ..hash import Hash
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated



router =  APIRouter(
    tags=['Auth']
)

@router.post('/login', response_model=schema.Token)
def login(payload:  Annotated[OAuth2PasswordRequestForm, Depends()], db: Session =  Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    if not Hash.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = oauth2.create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
