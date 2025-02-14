from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from app.models import Wallet
from app.schemas import Operation


async def get_balance(db: AsyncSession, uuid: str):
    return await db.scalar(select(Wallet).where(Wallet.id == uuid))

async def wallet_operation(new_balance: Decimal, db: AsyncSession, uuid: str, operation: Operation):
    await db.execute(update(Wallet).where(Wallet.id == uuid).values(balance=new_balance))
    await db.commit()

async def create_wallet(db: AsyncSession):
    new_wallet = Wallet()
    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)
    print(type(new_wallet.id))
    return new_wallet