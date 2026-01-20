"""
Requests API Router

Handles repair request CRUD, AI analysis, and status management.
"""
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.request import Request, Media, RequestStatus, MediaType
from app.models.quote import Quote
from app.models.audit_log import AuditLog, AuditAction, EntityType
from app.api.v1.auth import get_current_active_user
from app.schemas.request import (
    RequestCreate,
    RequestResponse,
    RequestListResponse,
    AIAnalysisResponse,
    CompletionSubmit,
    SignatureSubmit,
)
from app.services.ai_diagnostic import analyze_request
from app.services.dispatch import dispatch_technicians


router = APIRouter()


def generate_reference_code() -> str:
    """Generate unique reference code for request."""
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(4))
    return f"REQ-{date_part}-{random_part}"


@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request_data: RequestCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new repair request.
    
    This will:
    1. Create the request with media
    2. Trigger AI analysis
    3. Generate initial quote estimate
    4. Start technician dispatch
    """
    # Create request
    request = Request(
        reference_code=generate_reference_code(),
        client_id=current_user.id,
        category=request_data.category,
        title=request_data.title,
        description=request_data.description,
        guided_answers=request_data.guided_answers.model_dump(),
        address=request_data.address,
        address_details=request_data.address_details,
        location=f"POINT({request_data.longitude} {request_data.latitude})",
        is_urgent=request_data.is_urgent,
        preferred_time=request_data.preferred_time,
        status=RequestStatus.PENDING,
    )
    
    db.add(request)
    await db.flush()
    
    # Add media
    for media_data in request_data.media:
        media = Media(
            request_id=request.id,
            type=MediaType(media_data.type),
            url=media_data.url,
            thumbnail_url=media_data.thumbnail_url,
            duration_seconds=media_data.duration_seconds,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.MEDIA_RETENTION_DAYS),
        )
        db.add(media)
    
    await db.flush()
    
    # Audit log
    audit = AuditLog(
        action=AuditAction.REQUEST_CREATED,
        entity_type=EntityType.REQUEST,
        entity_id=request.id,
        actor_id=current_user.id,
        new_value={"category": request.category.value, "title": request.title},
    )
    db.add(audit)
    
    # Run AI analysis
    ai_result = await analyze_request(
        request_id=request.id,
        category=request.category,
        description=request.description,
        guided_answers=request.guided_answers,
        media_urls=[m.url for m in request_data.media],
    )
    
    # Update request with AI results
    request.severity = ai_result.severity
    request.ai_confidence = ai_result.confidence
    request.ai_diagnosis = {
        "probable_issue": ai_result.probable_issue,
        "safety_instructions": ai_result.safety_instructions,
        "estimated_duration_hours": ai_result.estimated_duration_hours,
    }
    request.safety_instructions_shown = True
    request.status = RequestStatus.ANALYZED
    
    # Create initial quote
    quote = Quote(
        request_id=request.id,
        initial_min_price=ai_result.price_range.min_price,
        initial_max_price=ai_result.price_range.max_price,
        min_price=ai_result.price_range.min_price,
        max_price=ai_result.price_range.max_price,
    )
    db.add(quote)
    
    await db.commit()
    
    # Dispatch technicians (async task in production)
    # For now, update status
    request.status = RequestStatus.DISPATCHING
    await db.commit()
    
    # Start dispatch in background
    await dispatch_technicians(db, request.id)
    
    # Reload with relationships
    result = await db.execute(
        select(Request)
        .where(Request.id == request.id)
        .options(
            selectinload(Request.media),
            selectinload(Request.quote),
            selectinload(Request.technician),
        )
    )
    request = result.scalar_one()
    
    return RequestResponse.model_validate(request)


@router.get("/", response_model=RequestListResponse)
async def list_requests(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[RequestStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's repair requests with pagination."""
    query = select(Request).where(Request.client_id == current_user.id)
    
    if status_filter:
        query = query.where(Request.status == status_filter)
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get page
    query = query.options(
        selectinload(Request.media),
        selectinload(Request.quote),
        selectinload(Request.technician),
    ).order_by(Request.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    requests = result.scalars().all()
    
    return RequestListResponse(
        items=[RequestResponse.model_validate(r) for r in requests],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
    request_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific request by ID."""
    result = await db.execute(
        select(Request)
        .where(Request.id == request_id)
        .options(
            selectinload(Request.media),
            selectinload(Request.quote),
            selectinload(Request.technician),
        )
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    
    # Check ownership (client or assigned technician)
    if request.client_id != current_user.id:
        if current_user.technician_profile:
            if request.technician_id != current_user.technician_profile.id:
                raise HTTPException(status_code=403, detail="Accesso negato")
        else:
            raise HTTPException(status_code=403, detail="Accesso negato")
    
    return RequestResponse.model_validate(request)


@router.post("/{request_id}/cancel")
async def cancel_request(
    request_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel a request (client only)."""
    result = await db.execute(
        select(Request).where(Request.id == request_id)
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    
    if request.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accesso negato")
    
    # Check if cancellation is allowed
    if request.status in [RequestStatus.COMPLETED, RequestStatus.PAID]:
        raise HTTPException(
            status_code=400,
            detail="Non puoi cancellare una richiesta completata",
        )
    
    # Apply penalty if technician already accepted/en route
    if request.status in [RequestStatus.ACCEPTED, RequestStatus.EN_ROUTE, RequestStatus.IN_PROGRESS]:
        # TODO: Apply 20% penalty (5% platform + 15% technician)
        pass
    
    request.status = RequestStatus.CANCELLED
    
    # Audit log
    audit = AuditLog(
        action=AuditAction.REQUEST_CANCELLED,
        entity_type=EntityType.REQUEST,
        entity_id=request.id,
        actor_id=current_user.id,
    )
    db.add(audit)
    
    await db.commit()
    
    return {"message": "Richiesta cancellata", "penalty_applied": False}


@router.post("/{request_id}/complete", response_model=RequestResponse)
async def submit_completion(
    request_id: UUID,
    completion: CompletionSubmit,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit work completion (technician).
    
    Includes up to 5 photos of completed work.
    """
    if not current_user.technician_profile:
        raise HTTPException(status_code=403, detail="Solo tecnici possono completare lavori")
    
    result = await db.execute(
        select(Request)
        .where(Request.id == request_id)
        .options(selectinload(Request.quote))
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    
    if request.technician_id != current_user.technician_profile.id:
        raise HTTPException(status_code=403, detail="Non sei assegnato a questa richiesta")
    
    if request.status != RequestStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="La richiesta non è in corso")
    
    # Update completion data
    request.completion_photos = completion.completion_photos
    request.status = RequestStatus.COMPLETED
    request.completed_at = datetime.now(timezone.utc)
    request.complaint_deadline = datetime.now(timezone.utc) + timedelta(days=7)
    
    # Audit log
    audit = AuditLog(
        action=AuditAction.REQUEST_COMPLETED,
        entity_type=EntityType.REQUEST,
        entity_id=request.id,
        actor_id=current_user.id,
    )
    db.add(audit)
    
    await db.commit()
    await db.refresh(request)
    
    return RequestResponse.model_validate(request)


@router.post("/{request_id}/sign", response_model=RequestResponse)
async def submit_signature(
    request_id: UUID,
    signature: SignatureSubmit,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit client signature to confirm work completion.
    
    This triggers payment capture.
    """
    result = await db.execute(
        select(Request)
        .where(Request.id == request_id)
        .options(
            selectinload(Request.media),
            selectinload(Request.quote),
            selectinload(Request.payment),
        )
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    
    if request.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accesso negato")
    
    if request.status != RequestStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Il lavoro non è ancora completato")
    
    # TODO: Upload signature image to S3
    # For now, store base64 data URL
    request.client_signature_url = signature.signature_data
    request.status = RequestStatus.PAID
    
    # TODO: Capture payment and transfer to technician
    
    await db.commit()
    await db.refresh(request)
    
    return RequestResponse.model_validate(request)
