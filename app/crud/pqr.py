from sqlalchemy.orm import Session
from app.models.pqr import PQR
from app.schemas.pqr import PQRCreate

def create_pqr(db: Session, pqr_data: PQRCreate) -> PQR:
    new_pqr = PQR(
        user_id=pqr_data.user_id,
        type=pqr_data.type,
        subject=pqr_data.subject,
        message=pqr_data.message
    )
    db.add(new_pqr)
    db.commit()
    db.refresh(new_pqr)
    return new_pqr
