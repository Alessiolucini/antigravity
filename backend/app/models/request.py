"""
Request Model

Represents a repair request from a client.
"""
import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from sqlalchemy import String, Boolean, DateTime, Text, Integer, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.technician import Technician
    from app.models.quote import Quote
    from app.models.payment import Payment


class RequestStatus(str, Enum):
    """Status flow for repair requests."""
    PENDING = "pending"              # Just created, awaiting AI analysis
    ANALYZED = "analyzed"            # AI has analyzed, awaiting dispatch
    DISPATCHING = "dispatching"      # Notifying technicians
    ACCEPTED = "accepted"            # Technician accepted
    EN_ROUTE = "en_route"            # Technician is on the way
    IN_PROGRESS = "in_progress"      # Work started
    QUOTE_REVISION = "quote_revision"  # Technician sent new quote
    COMPLETED = "completed"          # Work done, awaiting payment
    PAID = "paid"                    # Client paid
    CANCELLED = "cancelled"          # Cancelled by client/technician
    DISPUTED = "disputed"            # Under dispute


class Severity(str, Enum):
    """Problem severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Category(str, Enum):
    """Service categories."""
    PLUMBING = "plumbing"           # Idraulica
    ELECTRICAL = "electrical"       # Elettricità
    LOCKSMITH = "locksmith"         # Serrature/Fabbro
    HVAC = "hvac"                   # Caldaie/Climatizzazione
    APPLIANCES = "appliances"       # Elettrodomestici
    CARPENTRY = "carpentry"         # Falegnameria
    GENERAL = "general"             # Riparazioni generiche


class Request(Base):
    """Repair request model."""
    
    __tablename__ = "requests"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # Reference code for clients
    reference_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )  # e.g., "REQ-20260120-ABCD"
    
    # Client
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Assigned technician (nullable until accepted)
    technician_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("technicians.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Status
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(RequestStatus, name="request_status"),
        default=RequestStatus.PENDING,
        index=True,
    )
    
    # Category and description
    category: Mapped[Category] = mapped_column(
        SQLEnum(Category, name="request_category"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    
    # Guided questions answers
    guided_answers: Mapped[dict] = mapped_column(
        JSONB,
        default={},
    )
    # Example:
    # {
    #   "how_long": "2 days",
    #   "running_water": true,
    #   "sparks": false,
    #   "burning_smell": false,
    #   "availability": ["morning", "afternoon"]
    # }
    
    # Location
    location: Mapped[Optional[str]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326),
        nullable=True,
    )
    address: Mapped[str] = mapped_column(String(500))
    address_details: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Floor, apartment, etc.
    
    # AI Analysis results
    severity: Mapped[Optional[Severity]] = mapped_column(
        SQLEnum(Severity, name="severity_level"),
        nullable=True,
    )
    ai_confidence: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )  # 0-100 percentage
    ai_diagnosis: Mapped[dict] = mapped_column(
        JSONB,
        default={},
    )
    # Example:
    # {
    #   "probable_issue": "Tubo rotto sotto il lavandino",
    #   "confidence": 85,
    #   "safety_instructions": ["Chiudi l'acqua principale", "Non usare apparecchi elettrici vicino all'acqua"],
    #   "estimated_duration_hours": 2
    # }
    
    # Safety instructions shown immediately
    safety_instructions_shown: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Scheduling
    is_urgent: Mapped[bool] = mapped_column(Boolean, default=True)
    preferred_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # ETA (set when technician accepts)
    estimated_arrival: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Completion
    completion_photos: Mapped[List[str]] = mapped_column(
        JSONB,
        default=[],
    )  # Max 5 photos
    client_signature_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Complaint window (7 days after completion)
    complaint_deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    has_complaint: Mapped[bool] = mapped_column(Boolean, default=False)
    complaint_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
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
    accepted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    client: Mapped["User"] = relationship(
        "User",
        back_populates="requests",
        foreign_keys=[client_id],
    )
    technician: Mapped[Optional["Technician"]] = relationship(
        "Technician",
        back_populates="assigned_requests",
        foreign_keys=[technician_id],
    )
    media: Mapped[List["Media"]] = relationship(
        "Media",
        back_populates="request",
        cascade="all, delete-orphan",
    )
    quote: Mapped[Optional["Quote"]] = relationship(
        "Quote",
        back_populates="request",
        uselist=False,
    )
    payment: Mapped[Optional["Payment"]] = relationship(
        "Payment",
        back_populates="request",
        uselist=False,
    )
    
    def __repr__(self) -> str:
        return f"<Request {self.reference_code} - {self.status.value}>"


class MediaType(str, Enum):
    """Media types."""
    PHOTO = "photo"
    VIDEO = "video"


class Media(Base):
    """Media files attached to requests."""
    
    __tablename__ = "request_media"
    
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
        index=True,
    )
    
    # Media info
    type: Mapped[MediaType] = mapped_column(
        SQLEnum(MediaType, name="media_type"),
    )
    url: Mapped[str] = mapped_column(String(500))
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Metadata
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For videos
    
    # Auto-deletion (GDPR compliance)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )  # 10 days after created_at
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    # Relationships
    request: Mapped["Request"] = relationship(
        "Request",
        back_populates="media",
    )
    
    def __repr__(self) -> str:
        return f"<Media {self.id} - {self.type.value}>"
