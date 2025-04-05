from sqlalchemy import (
    Boolean, Column, String, Text, DateTime, Integer, func
)

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    close_date = Column(DateTime, nullable=True)
