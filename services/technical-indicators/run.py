from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    num_candles_in_state: int,
):
    """
    3 steps:
    1. Ingest candles from the Kafka input topic
    2. Calculate technical indicators
    3. Send the technical indicators to the Kafka output topic

    Args:
        kafka_broker_address (str): The address of the Kafka broker
        kafka_input_topic (str): The topic to ingest candles from
        kafka_output_topic (str): The topic to send technical indicators to
        kafka_consumer_group (str): The consumer group to use
        num_candles_in_state (int): The number of candles to keep in the state

    Returns:
        None
    """
    logger.info('Starting the technical-indicators service')
    logger.info(f'Kafka broker address: {kafka_broker_address}')
    logger.info(f'Kafka input topic: {kafka_input_topic}')
    logger.info(f'Kafka output topic: {kafka_output_topic}')
    logger.info(f'Kafka consumer group: {kafka_consumer_group}')
    logger.info(f'Number of candles in state: {num_candles_in_state}')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    # Define the input and output topics of our streaming application
    input_topic = app.topic(
        name=kafka_input_topic,
        value_serializer='json',
    )
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json',
    )

    sdf = app.dataframe(topic=input_topic)
    sdf = sdf.update(lambda value: logger.info(f'candle: {value}'))
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        num_candles_in_state=config.num_candles_in_state,
    )
