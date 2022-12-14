from fastapi import APIRouter

router = APIRouter()

# get projects
@router.get("/")
def get():
    return { "message": "Hello wor/d" }