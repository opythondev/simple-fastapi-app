from fastapi import FastAPI

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "David"},
    {"id": 3, "role": "trader", "name": "John"},
]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "ammount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "ammount": 2.12},
]

app = FastAPI(title="Trading App")


@app.get("/users/{user_id}")
async def get_users(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]
