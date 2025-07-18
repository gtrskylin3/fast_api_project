from fastapi import FastAPI, Path
from typing import Annotated
import uvicorn
from items_views import router as items_router
from users.views import router as user_router
app = FastAPI()
app.include_router(items_router, tags=["Items"])
app.include_router(user_router)


@app.get("/hello/{name}")
def hello(name):
    return {'message': "hello"+" "+name}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)