"""
User Model

Represents clients and technician user accounts.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """User model for clients and technicians."""
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # Basic info
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=True,
    )
    password_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    
    # Profile
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # OAuth
    oauth_provider: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )  # 'google', 'apple', None
    oauth_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Verification
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Role
    role: Mapped[str] = mapped_column(
        String(20),
        default="client",
    )  # 'client', 'technician', 'admin'
    
    # Push notification
    fcm_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
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
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    technician_profile: Mapped[Optional["Technician"]] = relationship(
        "Technician",
        back_populates="user",
        uselist=False,
    )
    requests: Mapped[List["Request"]] = relationship(
        "Request",
        back_populates="client",
        foreign_keys="Request.client_id",
    )
    payments: Mapped[List["Payment"]] = relationship(
        "Payment",
        back_populates="client",
    )
    
    def __repr__(self) -> str:
        return f"<User {self.id} - {self.email or self.phone}>"
