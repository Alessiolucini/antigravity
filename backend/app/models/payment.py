"""
Payment Model

Escrow payments and technician payouts.
"""
import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlalchemy import String, DateTime, Integer, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.request import Request


class PaymentStatus(str, Enum):
    """Payment status flow."""
    PENDING = "pending"              # Payment initiated
    HELD = "held"                    # Funds held in escrow
    CAPTURED = "captured"            # Work done, funds captured
    TRANSFERRED = "transferred"      # Payout sent to technician
    REFUNDED = "refunded"            # Full refund to client
    PARTIAL_REFUND = "partial_refund"  # Penalty applied, partial refund
    FAILED = "failed"                # Payment failed


class PaymentMethod(str, Enum):
    """Supported payment methods."""
    CARD = "card"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    PAYPAL = "paypal"


class Payment(Base):
    """Payment model with escrow support."""
    
    __tablename__ = "payments"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # FK to request
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("requests.id", ondelete="CASCADE"),
        unique=True,
    )
    
    # FK to client
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Amount (in cents)
    amount: Mapped[int] = mapped_column(Integer)  # Total amount
    
    # Fee breakdown
    platform_fee: Mapped[int] = mapped_column(Integer)  # 10% for the platform
    technician_payout: Mapped[int] = mapped_column(Integer)  # 90% for technician
    
    # Status
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus, name="payment_status"),
        default=PaymentStatus.PENDING,
        index=True,
    )
    
    # Payment method
    payment_method: Mapped[PaymentMethod] = mapped_column(
        SQLEnum(PaymentMethod, name="payment_method"),
    )
    
    # Stripe
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )
    stripe_transfer_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Penalty (if client cancels after technician arrives)
    penalty_amount: Mapped[int] = mapped_column(Integer, default=0)
    penalty_to_platform: Mapped[int] = mapped_column(Integer, default=0)  # 5%
    penalty_to_technician: Mapped[int] = mapped_column(Integer, default=0)  # 15%
    
    # Invoice
    invoice_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    invoice_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    invoice_generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    held_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    captured_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    transferred_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    request: Mapped["Request"] = relationship(
        "Request",
        back_populates="payment",
    )
    client: Mapped["User"] = relationship(
        "User",
        back_populates="payments",
    )
    
    def __repr__(self) -> str:
        return f"<Payment {self.id} - €{self.amount/100:.2f} - {self.status.value}>"
