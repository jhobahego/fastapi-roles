from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config.db import Base, engine
from routes import users, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return RedirectResponse("/docs")
