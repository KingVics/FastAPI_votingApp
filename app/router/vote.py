from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from .. import schema, database, oauth2, models

router =  APIRouter(
    prefix='/vote',
    tags=['Vote'],
    dependencies=[Depends(oauth2.get_current_user)]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(payload: schema.VoteBase, db: Session =  Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == payload.post_id, 
    models.Vote.user_id == current_user.id)

    found_query = vote_query.first()

    if payload.dir == 1:
        if found_query:
            raise(HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id}"
                f" has already voted for post {payload.post_id}"))
        new_vote = models.Vote(post_id = payload.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}