import json
from typing import List
from loguru import logger
from websocket import create_connection

from .trade import Trade


class KrakenWebsocketAPI:
    # Websocket URL
    URL = "wss://ws.kraken.com/v2"

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # Create a websocket connection
        self._ws_client = create_connection(self.URL)

        # Subscribe to the trades
        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        Fetch the trades from the Kraken Websocket APIs and returns them as a list of Trade objects.

        Returns:
            List[Trade]: A list of Trade objects.
        """
        data = self._ws_client.recv()

        # Transform raw data into a JSON object
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return []

        # Extract the trades data
        try:
            trades_data = data['data']
        except KeyError:
            logger.error(f"No 'data' field with trades in the message: {data}")
            return []

        trades = [
            Trade(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp']
            ) for trade in trades_data
        ]

        return trades

    def _subscribe(self):
        # Send a subscribe message to the websocket
        self._ws_client.send(json.dumps({
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": self.pairs,
                "snapshot": True
            }
        }))

        # Skip the initial messages
        for pair in self.pairs:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()
