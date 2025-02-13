from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from app.models import Wallet
from app.schemas import Operation


async def get_balance(db: AsyncSession, uuid: str):
    return await db.scalar(select(Wallet).where(Wallet.id == uuid))

async def wallet_operation(db: AsyncSession, uuid: str, operation: Operation):
    wallet = await db.scalar(select(Wallet).where(Wallet.id == uuid))
    if wallet:
        if operation.operationType == "DEPOSIT":
            new_balance = wallet.balance + operation.amount
        else:
            new_balance = wallet.balance - operation.amount
        if new_balance > 0:
            await db.execute(update(Wallet).where(Wallet.id == uuid).values(balance=new_balance))
            await db.commit()
        else:
            raise ValueError("Insufficient funds on balance")
    else:
        raise ValueError("Wallet not found")

async def create_wallet(db: AsyncSession):
    new_wallet = Wallet()
    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)
    print(type(new_wallet.id))
    return new_wallet