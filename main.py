from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field
from enum import Enum

fake_users = [
    {"id": 1, "role": "admin", "name": ["Bob"]},
    {"id": 2, "role": "investor", "name": "David"},
    {"id": 3, "role": "trader", "name": "John"},
    {
        "id": 4,
        "role": "trader",
        "name": "Andrea",
        "degree": [
            {"id": 1, "created_at": "2023-01-01T00:00:00", "type_degree": "expert"}
        ],
    },
]


fake_trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123,
        "ammount": 2.12,
    },
    {
        "id": 2,
        "user_id": 1,
        "currency": "BTC",
        "side": "sell",
        "price": 125,
        "ammount": 2.12,
    },
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    ammount: float


app = FastAPI(title="Trading App")


@app.exception_handler(ValidationError)
async def validation_error_handker(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(exc.errors()),
    )


@app.get("/users/{user_id}", response_model=List[User])
async def get_users(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@app.post("/trades")
async def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
