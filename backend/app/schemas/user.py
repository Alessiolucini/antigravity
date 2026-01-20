"""
User Schemas

Pydantic models for user-related API operations.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserBase(BaseModel):
    """Base user schema."""
    name: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration."""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    
    # OAuth fields (optional)
    oauth_provider: Optional[str] = None  # 'google', 'apple'
    oauth_token: Optional[str] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        # Italian phone format validation
        phone_pattern = r'^(\+39)?[0-9]{9,10}$'
        cleaned = re.sub(r'[\s\-]', '', v)
        if not re.match(phone_pattern, cleaned):
            raise ValueError('Formato telefono non valido. Usa formato italiano (+39XXXXXXXXXX)')
        return cleaned
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.search(r'[A-Z]', v):
            raise ValueError('La password deve contenere almeno una lettera maiuscola')
        if not re.search(r'[0-9]', v):
            raise ValueError('La password deve contenere almeno un numero')
        return v
    
    def model_post_init(self, __context):
        # At least one of email or phone must be provided for standard registration
        if not self.oauth_provider and not self.email and not self.phone:
            raise ValueError('Email o telefono richiesto')


class UserLogin(BaseModel):
    """Schema for user login."""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=1)
    
    def model_post_init(self, __context):
        if not self.email and not self.phone:
            raise ValueError('Email o telefono richiesto')


class PhoneVerification(BaseModel):
    """Schema for phone verification."""
    phone: str
    code: str = Field(..., min_length=6, max_length=6)


class UserResponse(BaseModel):
    """User response schema."""
    id: UUID
    email: Optional[str] = None
    phone: Optional[str] = None
    name: str
    avatar_url: Optional[str] = None
    role: str
    is_email_verified: bool
    is_phone_verified: bool
    created_at: datetime
    
    # Technician profile (if exists)
    technician_profile: Optional["TechnicianBrief"] = None
    
    class Config:
        from_attributes = True


class TechnicianBrief(BaseModel):
    """Brief technician info for user response."""
    id: UUID
    internal_code: str
    specializations: list[str]
    rating: float
    completed_jobs: int
    is_active: bool
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request."""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8)


# Update forward references
UserResponse.model_rebuild()
