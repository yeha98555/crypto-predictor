# Mock the Kraken API
from pydantic import BaseModel
from datetime import datetime
from typing import List
import time


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

class KrakenMockAPI:
    def __init__(self, pair: str):
        self.pair = pair

    def get_trades(self) -> List[Trade]:
        mock_trades = [
            Trade(pair=self.pair, price=0.5147, volume=1136.19677815, timestamp=datetime(2023, 9, 25, 7, 49, 36, 925603), timestamp_ms=1727232576925603),
            Trade(pair=self.pair, price=0.5347, volume=1136.19677815, timestamp=datetime(2023, 9, 25, 7, 49, 36, 925605), timestamp_ms=1727232576925603),
        ]

        time.sleep(1)

        return mock_trades
