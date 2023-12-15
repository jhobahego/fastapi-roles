from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse("/docs")
