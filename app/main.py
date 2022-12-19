from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from app.db import models
from app.db.database import engine
from app.routers import projects, users, updates, points, auth
from fastapi.responses import RedirectResponse

from app.utils import get_current_user

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI()


# protected routes
app.include_router(
    projects.router, prefix="/projects", dependencies=[Depends(get_current_user)]
),
app.include_router(
    users.router, prefix="/users", dependencies=[Depends(get_current_user)]
)
app.include_router(
    updates.router, prefix="/updates", dependencies=[Depends(get_current_user)]
)
app.include_router(
    points.router, prefix="/points", dependencies=[Depends(get_current_user)]
)

# unprotected routes
app.include_router(auth.router)


@app.get("/")
async def root():
    return RedirectResponse("/docs")
