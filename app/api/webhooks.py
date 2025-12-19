from fastapi import APIRouter
from ..database import SessionLocal
from ..models import Webhook

router = APIRouter(prefix="/webhooks")

@router.post("")
def create_webhook(url: str, event: str):
    db = SessionLocal()
    w = Webhook(url=url, event=event)
    db.add(w)
    db.commit()
    return w

