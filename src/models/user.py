from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        viewonly=True,
    )

    owned_tasks = relationship(
        "Task",
        foreign_keys="Task.owner_id",
        back_populates="owner",
    )

    assigned_tasks = relationship(
        "Task",
        foreign_keys="Task.assigned_to_id",
        back_populates="assigned_to",
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )