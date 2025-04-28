from sqlalchemy import (Column, String, Text)

from app.core.db import Base
from app.models.base import CharityDonationBase

from app.services.constants import Limits


class CharityProject(Base, CharityDonationBase):
    name = Column(
        String(Limits.CHARITY_MODEL_NAME_LEN.value),
        unique=True,
        nullable=False
    )
    description = Column(Text, nullable=False)
