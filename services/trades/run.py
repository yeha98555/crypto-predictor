from loguru import logger
from src.kraken_api import KrakenMockAPI
import time


def main():
    """
    It does 2 things:
    1. Reads trades from the Kraken API.
    2. Push them to a Kafka topic.

    Args:
        None

    Returns:
        None
    """

    logger.info("Starting the trades service")
    
    kraken_api = KrakenMockAPI(pair="BTC/USD")

    while True: 
        trades = kraken_api.get_trades()

        for trade in trades:
            # TODO: Push to a Kafka topic

            logger.info(f"Pushed trade to Kafka: {trade}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
