from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config.db import Base, engine
from routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)


@app.get("/")
async def root():
    return RedirectResponse("/docs")
