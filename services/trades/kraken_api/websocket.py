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
        
        if 'heartbeat' in data:
            logger.info("Heartbeat received")
            return []

        # Transform raw data
        try:
            parsed_data = json.loads(data)
            trades_data = parsed_data['data']

            return [
                Trade(
                    pair=trade['symbol'],
                    price=trade['price'],
                    volume=trade['qty'],
                    timestamp=trade['timestamp']
                ) for trade in trades_data
            ]
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return []
        except KeyError:
            logger.error(f"No 'data' field with trades in the message: {parsed_data}")
            return []

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

        # Skip initial messages for each pair
        for _ in self.pairs:
            _ = self._ws_client.recv()  # Subscription status
            _ = self._ws_client.recv()  # Initial snapshot
