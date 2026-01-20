"""
Request Schemas

Pydantic models for repair request operations.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from app.models.request import RequestStatus, Severity, Category


class GuidedAnswers(BaseModel):
    """Guided questions answers for request creation."""
    how_long: Optional[str] = Field(None, description="Da quanto tempo c'è il problema?")
    running_water: Optional[bool] = Field(None, description="C'è acqua corrente coinvolta?")
    sparks: Optional[bool] = Field(None, description="Hai visto scintille?")
    burning_smell: Optional[bool] = Field(None, description="Senti odore di bruciato?")
    gas_smell: Optional[bool] = Field(None, description="Senti odore di gas?")
    availability: List[str] = Field(
        default=[],
        description="Fasce orarie di disponibilità",
    )  # ['morning', 'afternoon', 'evening', 'night']
    
    @field_validator('availability')
    @classmethod
    def validate_availability(cls, v: List[str]) -> List[str]:
        valid_slots = {'morning', 'afternoon', 'evening', 'night', 'anytime'}
        for slot in v:
            if slot not in valid_slots:
                raise ValueError(f'Fascia oraria non valida: {slot}')
        return v


class MediaUpload(BaseModel):
    """Schema for media upload info."""
    type: str  # 'photo' or 'video'
    url: str
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None  # For videos


class RequestCreate(BaseModel):
    """Schema for creating a repair request."""
    category: Category
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10, max_length=2000)
    
    # Location
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: str = Field(..., min_length=5, max_length=500)
    address_details: Optional[str] = Field(None, max_length=255)
    
    # Media (uploaded separately, passed as URLs)
    media: List[MediaUpload] = Field(default=[], max_length=6)  # Max 5 photos + 1 video
    
    # Guided answers
    guided_answers: GuidedAnswers
    
    # Scheduling
    is_urgent: bool = True
    preferred_time: Optional[datetime] = None
    
    @field_validator('media')
    @classmethod
    def validate_media(cls, v: List[MediaUpload]) -> List[MediaUpload]:
        photos = [m for m in v if m.type == 'photo']
        videos = [m for m in v if m.type == 'video']
        
        if len(photos) > 5:
            raise ValueError('Massimo 5 foto consentite')
        if len(videos) > 1:
            raise ValueError('Massimo 1 video consentito')
        if videos and videos[0].duration_seconds and videos[0].duration_seconds > 10:
            raise ValueError('Video massimo 10 secondi')
        
        return v


class AIAnalysisResponse(BaseModel):
    """AI analysis result."""
    severity: Severity
    confidence: int = Field(..., ge=0, le=100)
    probable_issue: str
    safety_instructions: List[str]
    estimated_duration_hours: float
    price_range: "PriceRange"


class PriceRange(BaseModel):
    """Price estimate range."""
    min_price: int  # In cents
    max_price: int  # In cents
    disclaimer: str = "Il preventivo definitivo sarà confermato dopo verifica del tecnico"
    
    @property
    def min_price_eur(self) -> float:
        return self.min_price / 100
    
    @property
    def max_price_eur(self) -> float:
        return self.max_price / 100


class MediaResponse(BaseModel):
    """Media response schema."""
    id: UUID
    type: str
    url: str
    thumbnail_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TechnicianBrief(BaseModel):
    """Brief technician info for request response."""
    id: UUID
    internal_code: str
    name: str
    rating: float
    completed_jobs: int
    avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class RequestResponse(BaseModel):
    """Full request response."""
    id: UUID
    reference_code: str
    status: RequestStatus
    category: Category
    title: str
    description: str
    
    # Location (partial for privacy)
    address: str
    
    # AI analysis
    severity: Optional[Severity] = None
    ai_confidence: Optional[int] = None
    ai_diagnosis: dict = {}
    
    # Quote (if exists)
    quote: Optional["QuoteBrief"] = None
    
    # Technician (if assigned)
    technician: Optional[TechnicianBrief] = None
    estimated_arrival: Optional[datetime] = None
    
    # Media
    media: List[MediaResponse] = []
    
    # Timestamps
    created_at: datetime
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Complaint
    complaint_deadline: Optional[datetime] = None
    has_complaint: bool = False
    
    class Config:
        from_attributes = True


class QuoteBrief(BaseModel):
    """Brief quote info for request response."""
    id: UUID
    min_price: int
    max_price: int
    final_price: Optional[int] = None
    client_approved: bool
    revision_count: int
    
    class Config:
        from_attributes = True


class RequestListResponse(BaseModel):
    """Paginated list of requests."""
    items: List[RequestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class RequestStatusUpdate(BaseModel):
    """For updating request status (technician/admin)."""
    status: RequestStatus
    notes: Optional[str] = None


class CompletionSubmit(BaseModel):
    """For submitting work completion."""
    completion_photos: List[str] = Field(..., max_length=5)
    notes: Optional[str] = None


class SignatureSubmit(BaseModel):
    """For submitting client signature."""
    signature_data: str  # Base64 encoded signature image


# Update forward references
AIAnalysisResponse.model_rebuild()
RequestResponse.model_rebuild()
