"""
Technician Model

Extended profile for technician users.
"""
import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, Float, Integer, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.request import Request


class Technician(Base):
    """Technician profile with specializations and availability."""
    
    __tablename__ = "technicians"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # FK to User
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )
    
    # Internal code visible to clients (e.g., "TECH-001234")
    internal_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )
    
    # Specializations
    specializations: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=[],
    )  # ['idraulica', 'elettricità', 'serrature', 'caldaie', 'elettrodomestici']
    
    # Bio and description
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Rating and stats
    rating: Mapped[float] = mapped_column(Float, default=5.0)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    completed_jobs: Mapped[int] = mapped_column(Integer, default=0)
    
    # Pricing (hourly rate in cents)
    hourly_rate_cents: Mapped[int] = mapped_column(Integer, default=5000)  # €50 default
    
    # Location (PostGIS geography for distance queries)
    # Note: Requires PostGIS extension
    location: Mapped[Optional[str]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326),
        nullable=True,
    )
    
    # Last known address (for display)
    current_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Availability
    availability: Mapped[dict] = mapped_column(
        JSONB,
        default={},
    )  # {"mon": ["09:00-18:00"], "tue": ["09:00-18:00"], ...}
    
    is_available_now: Mapped[bool] = mapped_column(Boolean, default=True)
    is_accepting_jobs: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Verification
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    id_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    insurance_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Documents
    id_document_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    insurance_document_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Stripe Connect account for payouts
    stripe_account_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
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
    user: Mapped["User"] = relationship(
        "User",
        back_populates="technician_profile",
    )
    assigned_requests: Mapped[List["Request"]] = relationship(
        "Request",
        back_populates="technician",
        foreign_keys="Request.technician_id",
    )
    
    def __repr__(self) -> str:
        return f"<Technician {self.internal_code} - {', '.join(self.specializations)}>"
