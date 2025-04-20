from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.pqr import PQRCreate, PQRResponse
from database import get_db
from crud import pqr as crud_pqr

router = APIRouter(
    prefix="/pqr",
    tags=["PQR"]
)

@router.post("/", response_model=PQRResponse)
def create_pqr(pqr: PQRCreate, db: Session = Depends(get_db)):
    return crud_pqr.create_pqr(db, pqr)
