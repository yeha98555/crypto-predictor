from datetime import datetime

from pydantic import BaseModel, Field, computed_field


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
    timestamp: str = Field(
        ...,
        pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$',
    )

    @computed_field
    def timestamp_ms(self) -> int:
        """Compute timestamp in milliseconds."""
        dt = datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
        return int(dt.timestamp() * 1000)

    def to_dict(self) -> dict:
        return self.model_dump()
