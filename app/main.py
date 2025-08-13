from fastapi import FastAPI
from . import models, database
from .router import posts, users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

print(settings.database_username)

# models.Base.metadata.create_all(database.engine)


app =  FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def index():
    return 'hello world'
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(vote.router)





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)