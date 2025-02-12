from sqlalchemy import Column, UUID, DECIMAL
from app.database import Base
import uuid


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(DECIMAL, index=True, nullable=False, default=0)
