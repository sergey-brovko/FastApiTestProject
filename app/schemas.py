from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum


class OperationEnum(str, Enum):
    deposit = 'DEPOSIT'
    withdraw = 'WITHDRAW'

class Operation(BaseModel):
    operationType: OperationEnum
    amount: Decimal = Field(decimal_places=2, gt=0)

