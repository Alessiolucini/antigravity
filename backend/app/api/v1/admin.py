"""
Admin API Router

Admin panel endpoints for managing users, technicians, and requests.
"""
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.technician import Technician
from app.models.request import Request, RequestStatus
from app.models.payment import Payment
from app.models.audit_log import AuditLog
from app.api.v1.auth import get_current_active_user


router = APIRouter()


async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Ensure user is admin."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accesso admin richiesto")
    return current_user


@router.get("/dashboard")
async def admin_dashboard(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Get admin dashboard metrics."""
    # Users count
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar()
    
    # Technicians count
    techs_result = await db.execute(select(func.count(Technician.id)))
    total_technicians = techs_result.scalar()
    
    # Requests by status
    requests_result = await db.execute(
        select(Request.status, func.count(Request.id)).group_by(Request.status)
    )
    requests_by_status = {r[0].value: r[1] for r in requests_result.all()}
    
    # Today's metrics
    today = datetime.now(timezone.utc).date()
    today_requests = await db.execute(
        select(func.count(Request.id)).where(func.date(Request.created_at) == today)
    )
    
    return {
        "total_users": total_users,
        "total_technicians": total_technicians,
        "requests_by_status": requests_by_status,
        "requests_today": today_requests.scalar(),
    }


@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role_filter: Optional[str] = None,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all users with pagination."""
    query = select(User)
    if role_filter:
        query = query.where(User.role == role_filter)
    query = query.order_by(User.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in result.scalars()]


@router.patch("/users/{user_id}/disable")
async def disable_user(
    user_id: UUID,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Disable a user account."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    user.is_active = False
    await db.commit()
    return {"message": "Utente disabilitato"}


@router.get("/technicians")
async def list_technicians(
    page: int = Query(1, ge=1),
    verified_only: bool = False,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List technicians for admin review."""
    query = select(Technician)
    if verified_only:
        query = query.where(Technician.is_verified == True)
    result = await db.execute(query.limit(50))
    return [{"id": t.id, "internal_code": t.internal_code, "is_verified": t.is_verified} for t in result.scalars()]


@router.patch("/technicians/{tech_id}/verify")
async def verify_technician(
    tech_id: UUID,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Verify a technician's credentials."""
    result = await db.execute(select(Technician).where(Technician.id == tech_id))
    tech = result.scalar_one_or_none()
    if not tech:
        raise HTTPException(status_code=404, detail="Tecnico non trovato")
    tech.is_verified = True
    await db.commit()
    return {"message": "Tecnico verificato"}


@router.get("/audit-logs")
async def list_audit_logs(
    page: int = Query(1, ge=1),
    entity_type: Optional[str] = None,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List audit logs for compliance."""
    query = select(AuditLog).order_by(AuditLog.created_at.desc())
    query = query.offset((page - 1) * 50).limit(50)
    result = await db.execute(query)
    return [{"id": l.id, "action": l.action.value, "entity_type": l.entity_type.value, "created_at": l.created_at} for l in result.scalars()]
