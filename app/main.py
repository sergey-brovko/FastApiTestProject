from fastapi import FastAPI, HTTPException

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import Operation
from app import crud


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/wallets/{WALLET_UUID}")
async def say_balance(WALLET_UUID: str, db: AsyncSession = Depends(get_db)):
    wallet = await crud.get_balance(db, WALLET_UUID)
    if wallet:
        balance = wallet.balance
        return {"message": f"Your balance: {balance}"}
    else:
        raise HTTPException(status_code=404, detail="Wallet not found")

@app.post("/api/v1/wallets/{WALLET_UUID}/operation")
async def say_operation(WALLET_UUID: str, operations: Operation, db: AsyncSession = Depends(get_db)):
    try:
        await crud.wallet_operation(db, WALLET_UUID, operations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": f"Operation {operations.operationType.value}, amount: {operations.amount}"}

@app.post("/api/v1/new_wallet")
async def create_wallet(db: AsyncSession = Depends(get_db)):
    new_wallet = await crud.create_wallet(db)
    return {"NewWallet is created": new_wallet}
