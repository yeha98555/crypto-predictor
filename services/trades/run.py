from loguru import logger
from src.kraken_api import KrakenMockAPI
import time


def main(kafka_broker_address: str, kafka_topic: str):
    """
    It does 2 things:
    1. Reads trades from the Kraken API.
    2. Push them to a Kafka topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_topic (str): The topic to push the trades to.

    Returns:
        None
    """

    logger.info("Starting the trades service")
    print(f"Kafka broker address: {kafka_broker_address}")
    print(f"Kafka topic: {kafka_topic}")
    
    kraken_api = KrakenMockAPI(pair="BTC/USD")

    while True: 
        trades = kraken_api.get_trades()

        for trade in trades:
            # TODO: Push to a Kafka topic

            logger.info(f"Pushed trade to Kafka: {trade}")
        
        time.sleep(1)

if __name__ == "__main__":
    from config import config
    
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic
    )
