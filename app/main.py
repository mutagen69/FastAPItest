from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models, database
from app.router import movies, users

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(movies.router)
app.include_router(users.router)


