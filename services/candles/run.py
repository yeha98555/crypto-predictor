from loguru import logger


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
):
    """
    3 steps:
    1. Ingest trades from Kafka
    2. Generate candles using tumbling window and
    3. Output candles to Kafka

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic
        kafka_output_topic (str): Kafka output topic
        kafka_consumer_group (str): Kafka consumer group
        candle_seconds (int): Candle seconds

    Returns:
        None
    """
    logger.info('Starting the candles service')
    logger.info(f'Kafka broker address: {kafka_broker_address}')
    logger.info(f'Kafka input topic: {kafka_input_topic}')
    logger.info(f'Kafka output topic: {kafka_output_topic}')
    logger.info(f'Kafka consumer group: {kafka_consumer_group}')
    logger.info(f'Candle seconds: {candle_seconds}')


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
    )
