from sqlalchemy import (Column, ForeignKey, Text,Integer)

from app.core.db import Base
from app.models.base import CharityDonationBase


class Donation(Base, CharityDonationBase):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
