"""
Quote Model

Price quotes and revisions for repair requests.
"""
import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, Text, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.request import Request


class Quote(Base):
    """Price quote model with revision support."""
    
    __tablename__ = "quotes"
    
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
    
    # Initial estimate (from AI, in cents)
    initial_min_price: Mapped[int] = mapped_column(Integer)  # e.g., 8000 = €80
    initial_max_price: Mapped[int] = mapped_column(Integer)  # e.g., 15000 = €150
    
    # Current estimate (may be revised)
    min_price: Mapped[int] = mapped_column(Integer)
    max_price: Mapped[int] = mapped_column(Integer)
    
    # Final price (set by technician after inspection)
    final_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Price breakdown
    labor_cost: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    materials_cost: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Notes
    estimate_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Disclaimer shown to client
    disclaimer_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    # "Il prezzo definitivo sarà confermato dopo verifica del tecnico"
    
    # Revisions
    revision_count: Mapped[int] = mapped_column(Integer, default=0)
    last_revision_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    revision_media: Mapped[List[dict]] = mapped_column(
        JSONB,
        default=[],
    )  # Photos documenting why price increased
    # Example: [{"url": "...", "caption": "Danni nascosti trovati"}]
    
    # If revision > 40%, requires phone confirmation
    requires_phone_confirmation: Mapped[bool] = mapped_column(Boolean, default=False)
    phone_confirmation_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmation_operator_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    
    # Client approval
    client_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    client_approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Rejection
    client_rejected: Mapped[bool] = mapped_column(Boolean, default=False)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Cancellation penalty (if client rejects after technician arrives)
    penalty_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    penalty_amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # In cents
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    # Relationships
    request: Mapped["Request"] = relationship(
        "Request",
        back_populates="quote",
    )
    
    @property
    def revision_percentage(self) -> Optional[float]:
        """Calculate percentage increase from initial estimate."""
        if self.final_price and self.initial_max_price:
            if self.final_price > self.initial_max_price:
                return ((self.final_price - self.initial_max_price) / self.initial_max_price) * 100
        return None
    
    def __repr__(self) -> str:
        return f"<Quote {self.id} - €{self.min_price/100:.2f}-{self.max_price/100:.2f}>"
