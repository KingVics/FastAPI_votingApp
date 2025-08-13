
from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, database, schema, oauth2
from typing import  List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router =  APIRouter(
    prefix='/posts',
    tags=['Posts'],
    dependencies=[Depends(oauth2.get_current_user)]
)


@router.get('', response_model=List[schema.PostOut])
def get_post(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # post = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).limit(limit).offset(skip).all()
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    )  
    return result


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(payload: schema.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user) ):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (
    #     payload.title, payload.content, payload.published
    # ))
    # new_post = cursor.fetchone()
    # con.commit()
    
    new_post = models.Post(user_id=current_user.id, **payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schema.PostOut)
def post_detail(id: int, response: Response, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (
    #     str(id)
    # ))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter( models.Post.id == id).first()

    post, vote_count = (
        db.query(models.Post, func.count(models.Vote.post_id).label('vote'))  # match schema label
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    if post:
        return { "Post": post, "votes": vote_count}
    else:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING * """, (str(id)))
#    post = cursor.fetchone()
#    con.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post with {id} deleted successful"}
    
   

@router.put('/{id}', response_model=schema.PostCreate)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (
    #     post.title, post.content, post.published, str(id)
    # ))
    # update_post = cursor.fetchone()
    # con.commit()

    update_post = db.query(models.Post).filter(models.Post.id == id)

    post_data = update_post.first()
    
    print(f"post_data: {post_data}")
    
    if post_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    
    if post_data.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    update_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return  post
    

