from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.user_service import UserService
from app.api.v1.auth.models import User as UserModel

router = APIRouter()

@router.get("", response_model=List[dict])
def list_users(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """
    Public paginated list of users.
    Returns a list of dicts with minimal fields (id, email).
    """
    users = UserService.list_users(db, page=page, per_page=per_page)
    return users

@router.get("/{user_id}", response_model=dict)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Public profile with acquired cosmetics.
    """
    try:
        profile = UserService.get_user_profile(db, user_id)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))