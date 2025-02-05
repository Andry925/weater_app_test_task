from fastapi import FastAPI

from routers import weather
from config import settings

app = FastAPI()


@app.get("/healthy")
async def healthy():
    return {"healthy": True}


app.include_router(weather.router)
