from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from ..database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
         index=True,
    )