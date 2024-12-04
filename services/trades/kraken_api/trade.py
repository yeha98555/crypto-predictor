from pydantic import BaseModel
from datetime import datetime

class Trade(BaseModel):
    """
    A trade from the Kraken API.
    
    "symbol": "MATIC/USD",
    "side": "buy",
    "price": 0.5147,
    "qty": 1136.19677815,
    "ord_type": "limit",
    "trade_id": 4665847,
    "timestamp": "2023-09-25T07:49:36.925603Z"
    """
    pair: str  # symbol
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int

    def to_dict(self) -> dict:
        return self.model_dump_json()