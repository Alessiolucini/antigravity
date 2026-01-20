"""
Audit Log Model

GDPR-compliant audit trail for all sensitive operations.
"""
import uuid
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy import String, DateTime, Text, func, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditAction(str, Enum):
    """Auditable actions."""
    # User actions
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    PASSWORD_CHANGED = "password_changed"
    
    # Request actions
    REQUEST_CREATED = "request_created"
    REQUEST_UPDATED = "request_updated"
    REQUEST_CANCELLED = "request_cancelled"
    REQUEST_COMPLETED = "request_completed"
    
    # Technician actions
    TECHNICIAN_ASSIGNED = "technician_assigned"
    TECHNICIAN_ACCEPTED = "technician_accepted"
    TECHNICIAN_REJECTED = "technician_rejected"
    TECHNICIAN_ARRIVED = "technician_arrived"
    
    # Quote actions
    QUOTE_CREATED = "quote_created"
    QUOTE_REVISED = "quote_revised"
    QUOTE_APPROVED = "quote_approved"
    QUOTE_REJECTED = "quote_rejected"
    
    # Payment actions
    PAYMENT_INITIATED = "payment_initiated"
    PAYMENT_HELD = "payment_held"
    PAYMENT_CAPTURED = "payment_captured"
    PAYMENT_REFUNDED = "payment_refunded"
    PAYMENT_TRANSFERRED = "payment_transferred"
    
    # Media actions
    MEDIA_UPLOADED = "media_uploaded"
    MEDIA_DELETED = "media_deleted"
    MEDIA_AUTO_EXPIRED = "media_auto_expired"
    
    # Admin actions
    ADMIN_USER_DISABLED = "admin_user_disabled"
    ADMIN_TECHNICIAN_VERIFIED = "admin_technician_verified"
    ADMIN_DISPUTE_RESOLVED = "admin_dispute_resolved"


class EntityType(str, Enum):
    """Entity types for audit log."""
    USER = "user"
    TECHNICIAN = "technician"
    REQUEST = "request"
    QUOTE = "quote"
    PAYMENT = "payment"
    MEDIA = "media"


class AuditLog(Base):
    """Immutable audit log for compliance and debugging."""
    
    __tablename__ = "audit_logs"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # Entity reference
    entity_type: Mapped[EntityType] = mapped_column(
        SQLEnum(EntityType, name="entity_type"),
        index=True,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
    )
    
    # Action
    action: Mapped[AuditAction] = mapped_column(
        SQLEnum(AuditAction, name="audit_action"),
        index=True,
    )
    
    # Actor (who performed the action)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )  # Null for system actions
    actor_type: Mapped[str] = mapped_column(
        String(20),
        default="user",
    )  # 'user', 'system', 'admin'
    
    # IP and user agent for security
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Changes
    old_value: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Additional context
    metadata: Mapped[dict] = mapped_column(JSONB, default={})
    
    # Timestamp (immutable)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )
    
    def __repr__(self) -> str:
        return f"<AuditLog {self.action.value} on {self.entity_type.value}:{self.entity_id}>"
