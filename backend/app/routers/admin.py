# backend/app/routers/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

# ← import from ../auth.py, not ./auth.py
from ..auth import User, get_current_user, get_db

admin_router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current: User = Depends(get_current_user)) -> User:
    if not current.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only",
        )
    return current


@admin_router.get("/users", response_model=list[User])
def list_users(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.exec(select(User)).all()


@admin_router.patch("/users/{user_id}/approve")
def approve_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": f"{user.email} approved"}


@admin_router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": f"{user.email} deleted"}
