from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, database, schema
from sqlalchemy.orm import Session
from ..hash import Hash


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

  
@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(payload: schema.PostUser, db: Session = Depends(database.get_db)):
    #hash the user password
    new_password = Hash.get_password_hash(payload.password)
    payload.password = new_password
    
    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if new_user == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error has occurred")
    return new_user 


@router.get('/user/{id}', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")

    return user
