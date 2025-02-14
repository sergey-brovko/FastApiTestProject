from fastapi import FastAPI, HTTPException

from fastapi.params import Depends
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import Operation
from app import crud

from redis.asyncio import Redis
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключение к Redis при старте
    app.redis = Redis(
        host="redis",
        port=6379,
        db=0,
        decode_responses=True
    )
    yield
    # Закрытие соединения при остановке
    await app.redis.close()

app = FastAPI(lifespan=lifespan)

async def get_redis() -> Redis:
    return app.redis



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/wallets/{WALLET_UUID}")
async def say_balance(WALLET_UUID: str, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    wallet_cache = await redis.get(WALLET_UUID)
    if wallet_cache:
        return {"message": f"Your balance: {wallet_cache}"}
    wallet = await crud.get_balance(db, WALLET_UUID)
    if wallet:
        balance = wallet.balance
        await redis.setex(WALLET_UUID, 60, f"{wallet.balance}")
        return {"message": f"Your balance: {balance}"}
    else:
        raise HTTPException(status_code=404, detail="Wallet not found")

@app.post("/api/v1/wallets/{WALLET_UUID}/operation")
async def say_operation(WALLET_UUID: str, operation: Operation, db: AsyncSession = Depends(get_db),
                        redis: Redis = Depends(get_redis)):
    wallet_cache = await redis.get(WALLET_UUID)
    if wallet_cache:
        balance = Decimal(wallet_cache)
    else:
        wallet = await crud.get_balance(db, WALLET_UUID)
        if wallet:
            balance = wallet.balance
        else:
            raise HTTPException(status_code=404, detail="Wallet not found")
    new_balance = balance + operation.amount if operation.operationType == "DEPOSIT" else balance - operation.amount
    if new_balance > 0.0:
        try:
            await redis.setex(WALLET_UUID, 60, f"{new_balance}")
            await crud.wallet_operation(new_balance, db, WALLET_UUID, operation)
        except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
        else:
            return {"message": f"Operation {operation.operationType.value}, amount: {operation.amount}"}
    else:
        raise HTTPException(status_code=404, detail="Insufficient funds on balance")



@app.post("/api/v1/new_wallet")
async def create_wallet(db: AsyncSession = Depends(get_db)):
    new_wallet = await crud.create_wallet(db)
    return {"NewWallet is created": new_wallet}
