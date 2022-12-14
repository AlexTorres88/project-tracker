from fastapi import FastAPI
from routers import projects

app = FastAPI()

app.include_router(projects.router, prefix='/projects')


@app.get("/")
async def root():
    return {"message": "Hello World"}