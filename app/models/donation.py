from sqlalchemy import (
    Boolean, Column, ForeignKey, Text, DateTime, Integer, func
)
from app.core.db import Base


class Donation(Base):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, server_default=func.now(), nullable=False)
    close_date = Column(DateTime, nullable=True)
