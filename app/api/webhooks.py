# app/api/webhooks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Webhook
from ..schemas import WebhookCreate, WebhookOut

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("", response_model=WebhookOut)
def create_webhook(
    data: WebhookCreate,
    db: Session = Depends(get_db)
):
    webhook = Webhook(**data.dict())
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


@router.post("/{id}/test")
def test_webhook(
    id: str,
    db: Session = Depends(get_db)
):
    webhook = db.get(Webhook, id)

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    if not webhook.enabled:
        raise HTTPException(status_code=400, detail="Webhook is disabled")

    # 🔥 Dispatch async webhook test
    fire_webhook.delay(
        webhook.url,
        {
            "event": "webhook.test",
            "webhook_id": webhook.id
        }
    )

    return {
        "status": "dispatched",
        "message": "Webhook test request sent asynchronously"
    }
