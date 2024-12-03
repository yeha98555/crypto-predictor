from loguru import logger
from src.kraken_api import KrakenMockAPI
from quixstreams import Application


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
    
    # Mock the Kraken API
    kraken_api = KrakenMockAPI(pair="BTC/USD")

    # Initialize the QuixStreams application
    # This class handles all the low-level details of connecting to Kafka
    app = Application(broker_address=kafka_broker_address)
    
    # Define a topic where we will push the trades
    topic = app.topic(name=kafka_topic, value_serializer="json")

    with app.get_producer() as producer:
        while True: 
            trades = kraken_api.get_trades()

            for trade in trades:
                # Serialize the trade as bytes
                message = topic.serialize(key=trade.pair, value=trade.to_dict())
                # Push the serialized message to Kafka
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f"Pushed trade to Kafka: {trade}")


if __name__ == "__main__":
    from config import config
    
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic
    )
