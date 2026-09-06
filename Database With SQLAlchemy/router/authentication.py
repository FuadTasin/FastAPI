from fastapi import FastAPI,APIRouter
from pydantic import BaseModel

router=APIRouter()

@router.get('/auth')
def authentication():
    return "Added the route successfully."
