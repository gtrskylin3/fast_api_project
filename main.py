from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from typing import Annotated
import uvicorn
from api_v1 import router as router_v1
from items_views import router as items_router
from users.views import router as user_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    yield



app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Укажите домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router, tags=["Items"])
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "hello"}

@app.get("/hello/{name}")
def hello(name):
    return {'message': "hello"+" "+name}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)