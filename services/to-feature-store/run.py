from loguru import logger
from quixstreams import Application
from quixstreams.sinks.core.csv import CSVSink


def main(
    kafka_broker_address: str,
    kafka_consumer_group: str,
    kafka_input_topic: str,
    feature_group_name: str,
    feature_group_version: int,
):
    """
    2 things:
    1. Read messages from Kafka topic
    2. Push messages to Feature Store
    """
    logger.info('Hello from to-feature-store!')
    logger.info(f'Kafka broker address: {kafka_broker_address}')
    logger.info(f'Kafka consumer group: {kafka_consumer_group}')
    logger.info(f'Kafka input topic: {kafka_input_topic}')
    logger.info(f'Feature group name: {feature_group_name}')
    logger.info(f'Feature group version: {feature_group_version}')

    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    input_topic = app.topic(kafka_input_topic, value_deserializer='json')

    # Push messages to Feature Store
    csv_sink = CSVSink(path='file.csv')

    sdf = app.dataframe(input_topic)
    sdf.sink(csv_sink)

    app.run()


if __name__ == '__main__':
    from config import config

    main(
        config.kafka_broker_address,
        config.kafka_consumer_group,
        config.kafka_input_topic,
        config.feature_group_name,
        config.feature_group_version,
    )
