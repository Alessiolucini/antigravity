"""
Payments API Router

Handles payment creation, escrow, capture, and payouts.
"""
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.request import Request, RequestStatus
from app.models.payment import Payment, PaymentStatus
from app.models.audit_log import AuditLog, AuditAction, EntityType
from app.api.v1.auth import get_current_active_user
from app.schemas.payment import (
    PaymentCreate,
    PaymentIntentResponse,
    PaymentResponse,
    QuoteResponse,
    QuoteRevision,
    QuoteApproval,
)


router = APIRouter()


@router.get("/quote/{request_id}", response_model=QuoteResponse)
async def get_quote(
    request_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get quote for a request."""
    result = await db.execute(
        select(Request).where(Request.id == request_id).options(selectinload(Request.quote))
    )
    request = result.scalar_one_or_none()
    if not request or not request.quote:
        raise HTTPException(status_code=404, detail="Richiesta o preventivo non trovato")
    if request.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accesso negato")
    return QuoteResponse.model_validate(request.quote)


@router.post("/quote/{request_id}/approve", response_model=QuoteResponse)
async def approve_quote(
    request_id: UUID,
    approval: QuoteApproval,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Client approves or rejects a quote."""
    result = await db.execute(
        select(Request).where(Request.id == request_id).options(selectinload(Request.quote))
    )
    request = result.scalar_one_or_none()
    if not request or not request.quote:
        raise HTTPException(status_code=404, detail="Non trovato")
    if request.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accesso negato")
    
    quote = request.quote
    if approval.approved:
        quote.client_approved = True
        quote.client_approved_at = datetime.now(timezone.utc)
        if request.status == RequestStatus.QUOTE_REVISION:
            request.status = RequestStatus.IN_PROGRESS
    else:
        quote.client_rejected = True
        quote.rejection_reason = approval.rejection_reason
        request.status = RequestStatus.CANCELLED
    
    await db.commit()
    await db.refresh(quote)
    return QuoteResponse.model_validate(quote)


@router.post("/create", response_model=PaymentIntentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create payment intent (holds funds in escrow)."""
    result = await db.execute(
        select(Request).where(Request.id == payment_data.request_id)
        .options(selectinload(Request.quote))
    )
    request = result.scalar_one_or_none()
    if not request or request.client_id != current_user.id:
        raise HTTPException(status_code=404, detail="Non trovato")
    if not request.quote or not request.quote.client_approved:
        raise HTTPException(status_code=400, detail="Preventivo non approvato")
    
    amount = request.quote.final_price or request.quote.max_price
    platform_fee = int(amount * (settings.PLATFORM_FEE_PERCENT / 100))
    
    payment = Payment(
        request_id=request.id,
        client_id=current_user.id,
        amount=amount,
        platform_fee=platform_fee,
        technician_payout=amount - platform_fee,
        payment_method=payment_data.payment_method,
        stripe_payment_intent_id=f"pi_mock_{request.id}",
        status=PaymentStatus.PENDING,
    )
    db.add(payment)
    await db.commit()
    
    return PaymentIntentResponse(client_secret=f"secret_{request.id}", amount=amount)


@router.post("/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
    payment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Confirm payment - moves to escrow."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment or payment.client_id != current_user.id:
        raise HTTPException(status_code=404, detail="Non trovato")
    payment.status = PaymentStatus.HELD
    payment.held_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(payment)
    return PaymentResponse.model_validate(payment)


@router.post("/{payment_id}/release", response_model=PaymentResponse)
async def release_payment(
    payment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Release payment to technician after completion."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment or payment.client_id != current_user.id:
        raise HTTPException(status_code=404, detail="Non trovato")
    payment.status = PaymentStatus.TRANSFERRED
    payment.transferred_at = datetime.now(timezone.utc)
    payment.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(payment.id)[:8]}"
    await db.commit()
    await db.refresh(payment)
    return PaymentResponse.model_validate(payment)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get payment details."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment or payment.client_id != current_user.id:
        raise HTTPException(status_code=404, detail="Non trovato")
    return PaymentResponse.model_validate(payment)
