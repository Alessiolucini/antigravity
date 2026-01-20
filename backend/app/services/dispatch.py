"""
Dispatch Service

Intelligent technician dispatch based on specialization, distance, and availability.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.technician import Technician
from app.models.request import Request


async def dispatch_technicians(db: AsyncSession, request_id: UUID) -> list:
    """
    Find and notify the best technicians for a request.
    
    Selection criteria (in order):
    1. Specialization match
    2. Currently available
    3. Distance (closest first)
    4. Rating
    5. Response time history
    
    Notifies up to MAX_TECHNICIANS_TO_NOTIFY technicians.
    """
    # Get the request
    result = await db.execute(
        select(Request).where(Request.id == request_id)
    )
    request = result.scalar_one_or_none()
    if not request:
        return []
    
    category = request.category.value
    
    # Query technicians
    # In production, use PostGIS ST_Distance for real distance calculation
    query = select(Technician).where(
        Technician.is_active == True,
        Technician.is_available_now == True,
        Technician.is_accepting_jobs == True,
        Technician.is_verified == True,
    ).order_by(
        Technician.rating.desc(),
        Technician.completed_jobs.desc(),
    ).limit(settings.MAX_TECHNICIANS_TO_NOTIFY)
    
    result = await db.execute(query.options(selectinload(Technician.user)))
    technicians = result.scalars().all()
    
    # Filter by specialization (case insensitive)
    matching = [t for t in technicians if category.lower() in [s.lower() for s in t.specializations]]
    
    # If not enough specialists, include general technicians
    if len(matching) < settings.MAX_TECHNICIANS_TO_NOTIFY:
        general = [t for t in technicians if t not in matching]
        matching.extend(general[:settings.MAX_TECHNICIANS_TO_NOTIFY - len(matching)])
    
    # Notify technicians (in production: push, SMS, WhatsApp)
    for tech in matching[:settings.MAX_TECHNICIANS_TO_NOTIFY]:
        await notify_technician(tech, request)
    
    return [{"id": t.id, "internal_code": t.internal_code} for t in matching]


async def notify_technician(technician: Technician, request: Request):
    """Send notification to technician about new job."""
    # In production, implement:
    # 1. Push notification via Firebase
    # 2. SMS via Twilio
    # 3. WhatsApp via Business API
    
    # For now, just log
    print(f"[DISPATCH] Notifying {technician.internal_code} about request {request.reference_code}")
