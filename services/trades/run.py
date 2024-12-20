import signal
import sys
from typing import Union

from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def signal_handler(sig, frame):
    logger.info('Received shutdown signal. Exiting gracefully...')
    sys.exit(0)


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: Union[KrakenMockAPI, KrakenWebsocketAPI],
):
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

    logger.info('Starting the trades service')
    print(f'Kafka broker address: {kafka_broker_address}')
    print(f'Kafka topic: {kafka_topic}')

    # Initialize the QuixStreams application
    # This class handles all the low-level details of connecting to Kafka
    app = Application(broker_address=kafka_broker_address)

    # Define a topic where we will push the trades
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # Register the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                try:
                    # Serialize the trade as bytes
                    message = topic.serialize(key=trade.pair, value=trade.to_dict())
                    # Push the serialized message to Kafka
                    producer.produce(
                        topic=topic.name, value=message.value, key=message.key
                    )
                except Exception as e:
                    logger.error(f'Failed to produce message to Redpanda: {e}')

                logger.info(f'Pushed trade to Kafka: {trade}')


if __name__ == '__main__':
    from config import config

    # Initialize the Kraken API
    kraken_api = KrakenWebsocketAPI(pairs=config.pairs)
    # kraken_api = KrakenMockAPI(pair=config.pairs[0])  # Mock API for testing

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )
