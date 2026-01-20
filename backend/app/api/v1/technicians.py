"""
Technicians API Router

Handles technician profiles, job acceptance, and availability.
"""
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User
from app.models.technician import Technician
from app.models.request import Request, RequestStatus
from app.models.audit_log import AuditLog, AuditAction, EntityType
from app.api.v1.auth import get_current_active_user
from app.schemas.request import RequestResponse


router = APIRouter()


def generate_technician_code() -> str:
    """Generate unique internal code for technician."""
    random_part = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    return f"TECH-{random_part}"


# ============ Public endpoints ============

@router.get("/public/{technician_id}")
async def get_technician_public(
    technician_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get public technician profile (for clients)."""
    result = await db.execute(
        select(Technician)
        .where(Technician.id == technician_id)
        .options(selectinload(Technician.user))
    )
    technician = result.scalar_one_or_none()
    
    if not technician or not technician.is_active:
        raise HTTPException(status_code=404, detail="Tecnico non trovato")
    
    return {
        "id": technician.id,
        "internal_code": technician.internal_code,
        "name": technician.user.name,
        "avatar_url": technician.user.avatar_url,
        "specializations": technician.specializations,
        "rating": technician.rating,
        "total_reviews": technician.total_reviews,
        "completed_jobs": technician.completed_jobs,
        "bio": technician.bio,
        "is_verified": technician.is_verified,
    }


# ============ Technician-only endpoints ============

async def get_current_technician(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Technician:
    """Get current user's technician profile."""
    if not current_user.technician_profile:
        # Try to load it
        result = await db.execute(
            select(Technician).where(Technician.user_id == current_user.id)
        )
        technician = result.scalar_one_or_none()
        
        if not technician:
            raise HTTPException(
                status_code=403,
                detail="Devi essere un tecnico per accedere a questa risorsa",
            )
        return technician
    
    return current_user.technician_profile


@router.get("/me")
async def get_my_technician_profile(
    technician: Technician = Depends(get_current_technician),
    db: AsyncSession = Depends(get_db),
):
    """Get current technician's full profile."""
    # Reload with user relationship
    result = await db.execute(
        select(Technician)
        .where(Technician.id == technician.id)
        .options(selectinload(Technician.user))
    )
    technician = result.scalar_one()
    
    return {
        "id": technician.id,
        "internal_code": technician.internal_code,
        "user": {
            "id": technician.user.id,
            "name": technician.user.name,
            "email": technician.user.email,
            "phone": technician.user.phone,
            "avatar_url": technician.user.avatar_url,
        },
        "specializations": technician.specializations,
        "bio": technician.bio,
        "rating": technician.rating,
        "total_reviews": technician.total_reviews,
        "completed_jobs": technician.completed_jobs,
        "hourly_rate_cents": technician.hourly_rate_cents,
        "availability": technician.availability,
        "is_available_now": technician.is_available_now,
        "is_accepting_jobs": technician.is_accepting_jobs,
        "is_verified": technician.is_verified,
        "stripe_account_id": technician.stripe_account_id,
        "created_at": technician.created_at,
    }


@router.patch("/me/availability")
async def update_availability(
    is_available_now: Optional[bool] = None,
    is_accepting_jobs: Optional[bool] = None,
    availability: Optional[dict] = None,
    technician: Technician = Depends(get_current_technician),
    db: AsyncSession = Depends(get_db),
):
    """Update technician availability settings."""
    if is_available_now is not None:
        technician.is_available_now = is_available_now
    
    if is_accepting_jobs is not None:
        technician.is_accepting_jobs = is_accepting_jobs
    
    if availability is not None:
        technician.availability = availability
    
    await db.commit()
    
    return {
        "is_available_now": technician.is_available_now,
        "is_accepting_jobs": technician.is_accepting_jobs,
        "availability": technician.availability,
    }


@router.patch("/me/location")
async def update_location(
    latitude: float,
    longitude: float,
    address: Optional[str] = None,
    technician: Technician = Depends(get_current_technician),
    db: AsyncSession = Depends(get_db),
):
    """Update technician's current location."""
    technician.location = f"POINT({longitude} {latitude})"
    if address:
        technician.current_address = address
    
    await db.commit()
    
    return {"message": "Posizione aggiornata"}


@router.get("/me/jobs", response_model=list)
async def get_my_jobs(
    status_filter: Optional[RequestStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    technician: Technician = Depends(get_current_technician),
    db: AsyncSession = Depends(get_db),
):
    """Get technician's assigned jobs."""
    query = select(Request).where(Request.technician_id == technician.id)
    
    if status_filter:
        query = query.where(Request.status == status_filter)
    
    query = query.options(
        selectinload(Request.media),
        selectinload(Request.quote),
        selectinload(Request.client),
    ).order_by(Request.created_at.desc())
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    requests = result.scalars().all()
    
    return [RequestResponse.model_validate(r) for r in requests]


@router.get("/me/pending")
async def get_pending_requests(
    technician: Technician = Depends(get_current_technician),
    db: AsyncSession = Depends(get_db),
):
    """
    Get pending requests available for this technician.
    
    These are requests in DISPATCHING status where this technician
    was notified but hasn't responded yet.
    """
    # TODO: Implement dispatch tracking table
    # For now, return dispatching requests in technician's specializations
    
    query = select(Request).where(
        Request.status == RequestStatus.DISPATCHING,
        Request.technician_id.is_(None),
        Request.category.in_([s.lower() for s in technician.specializations]),
    ).options(
        selectinload(Request.media),
        selectinload(Request.quote),
    ).order_by(Request.created_at.desc()).limit(10)
    
    result = await db.execute(query)
    requests = result.scalars().all()
    
    # Don't show full address until accepted
    return [{
        "id": r.id,
        "reference_code": r.reference_code,
        "category": r.category.value,
        "title": r.title,
        "description": r.description,
        "severity": r.severity.value if r.severity else None,
        "ai_confidence": r.ai_confidence,
        "is_urgent": r.is_urgent,
        "quote": {
            "min_price": r.quote.min_price if r.quote else None,
            "max_price": r.quote.max_price if r.quote else None,
        } if r.quote else None,
        "created_at": r.created_at,
        # Partial address for privacy
        "area": r.address.split(",")[-2] if "," in r.address else r.address[:20],
    } for r in requests]


@router.post("/me/accept/{request_id}", response_model=RequestResponse)
async def accept_request(
    request_id: UUID,
    eta_minutes: int = Query(..., ge=5, le=180),
    technician: Technician = Depends(get_current_technician),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Accept a pending request.
    
    This assigns the technician and reveals the full address.
    """
    result = await db.execute(
        select(Request)
        .where(Request.id == request_id)
        .options(
            selectinload(Request.media),
            selectinload(Request.quote),
            selectinload(Request.client),
        )
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    
    if request.status != RequestStatus.DISPATCHING:
        raise HTTPException(status_code=400, detail="Richiesta non più disponibile")
    
    if request.technician_id:
        raise HTTPException(status_code=400, detail="Richiesta già assegnata")
    
    # Assign technician
    request.technician_id = technician.id
    request.status = RequestStatus.ACCEPTED
    request.accepted_at = datetime.now(timezone.utc)
    request.estimated_arrival = datetime.now(timezone.utc) + timedelta(minutes=eta_minutes)
    
    # Audit log
    audit = AuditLog(
        action=AuditAction.TECHNICIAN_ACCEPTED,
        entity_type=EntityType.REQUEST,
        entity_id=request.id,
        actor_id=current_user.id,
        new_value={"technician_id": str(technician.id), "eta_minutes": eta_minutes},
    )
    db.add(audit)
    
    await db.commit()
    await db.refresh(request)
    
    # TODO: Notify client with technician info and ETA
    
    return RequestResponse.model_validate(request)


@router.post("/me/start/{request_id}")
async def start_work(
    request_id: UUID,
    technician: Technician = Depends(get_current_technician),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark that work has started on a request."""
    result = await db.execute(
        select(Request).where(Request.id == request_id)
    )
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    
    if request.technician_id != technician.id:
        raise HTTPException(status_code=403, detail="Non sei assegnato a questa richiesta")
    
    if request.status not in [RequestStatus.ACCEPTED, RequestStatus.EN_ROUTE]:
        raise HTTPException(status_code=400, detail="Stato non valido per iniziare")
    
    request.status = RequestStatus.IN_PROGRESS
    
    # Audit
    audit = AuditLog(
        action=AuditAction.TECHNICIAN_ARRIVED,
        entity_type=EntityType.REQUEST,
        entity_id=request.id,
        actor_id=current_user.id,
    )
    db.add(audit)
    
    await db.commit()
    
    return {"message": "Lavoro iniziato"}

