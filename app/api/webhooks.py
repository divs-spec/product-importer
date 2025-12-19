# app/api/webhooks.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Webhook
from ..schemas import WebhookCreate, WebhookOut
from ..workers.webhooks import fire_webhook

router = APIRouter(prefix="/webhooks")

@router.post("", response_model=WebhookOut)
def create_webhook(data: WebhookCreate, db: Session = Depends(get_db)):
    w = Webhook(**data.dict())
    db.add(w)
    db.commit()
    db.refresh(w)
    return w

@router.post("/{id}/test")
def test_webhook(id: str, db: Session = Depends(get_db)):
    w = db.get(Webhook, id)
    fire_webhook.delay(w.url, {"test": True})
    return {"status": "sent"}
