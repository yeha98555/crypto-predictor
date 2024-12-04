# Mock the Kraken API
from datetime import datetime
from typing import List
import time
from .trade import Trade


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
