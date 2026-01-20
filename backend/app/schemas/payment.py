"""
Payment Schemas

Pydantic models for payment and quote operations.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.payment import PaymentStatus, PaymentMethod


class QuoteResponse(BaseModel):
    """Quote response schema."""
    id: UUID
    request_id: UUID
    
    # Prices
    initial_min_price: int
    initial_max_price: int
    min_price: int
    max_price: int
    final_price: Optional[int] = None
    
    # Breakdown
    labor_cost: Optional[int] = None
    materials_cost: Optional[int] = None
    
    # Notes
    estimate_notes: Optional[str] = None
    disclaimer_accepted: bool
    
    # Revision info
    revision_count: int
    last_revision_reason: Optional[str] = None
    revision_media: List[dict] = []
    requires_phone_confirmation: bool
    phone_confirmation_completed: bool
    
    # Status
    client_approved: bool
    client_approved_at: Optional[datetime] = None
    client_rejected: bool
    
    # Penalty
    penalty_applied: bool
    penalty_amount: Optional[int] = None
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QuoteRevision(BaseModel):
    """Schema for technician submitting a quote revision."""
    new_min_price: int = Field(..., gt=0)
    new_max_price: int = Field(..., gt=0)
    final_price: Optional[int] = Field(None, gt=0)
    reason: str = Field(..., min_length=10, max_length=1000)
    revision_media: List[dict] = []  # [{"url": "...", "caption": "..."}]
    
    # Breakdown
    labor_cost: Optional[int] = None
    materials_cost: Optional[int] = None


class QuoteApproval(BaseModel):
    """Schema for client approving/rejecting quote."""
    approved: bool
    rejection_reason: Optional[str] = None


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""
    request_id: UUID
    payment_method: PaymentMethod
    
    # For card payments
    payment_method_id: Optional[str] = None  # Stripe PaymentMethod ID


class PaymentIntentResponse(BaseModel):
    """Stripe PaymentIntent response for client."""
    client_secret: str
    amount: int
    currency: str = "eur"


class PaymentResponse(BaseModel):
    """Payment response schema."""
    id: UUID
    request_id: UUID
    
    # Amount
    amount: int
    platform_fee: int
    technician_payout: int
    
    # Status
    status: PaymentStatus
    payment_method: PaymentMethod
    
    # Penalty
    penalty_amount: int
    
    # Invoice
    invoice_number: Optional[str] = None
    invoice_url: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    held_at: Optional[datetime] = None
    captured_at: Optional[datetime] = None
    transferred_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PaymentCapture(BaseModel):
    """For manually capturing held payment (admin only)."""
    notes: Optional[str] = None


class RefundRequest(BaseModel):
    """For requesting a refund."""
    reason: str = Field(..., min_length=10, max_length=1000)
    refund_type: str = Field(..., pattern="^(full|partial)$")
    partial_amount: Optional[int] = None  # If partial refund


class TechnicianEarnings(BaseModel):
    """Technician earnings summary."""
    total_earned: int  # In cents
    pending_payout: int
    completed_jobs: int
    period_start: datetime
    period_end: datetime
    
    # Breakdown by status
    earnings_by_month: List[dict] = []  # [{"month": "2026-01", "amount": 150000}]


class DisputeCreate(BaseModel):
    """For creating a payment dispute."""
    request_id: UUID
    reason: str = Field(..., min_length=20, max_length=2000)
    evidence_urls: List[str] = []
    requested_resolution: str  # 'refund', 'partial_refund', 'redo_work'
