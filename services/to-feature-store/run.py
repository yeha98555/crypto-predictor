from loguru import logger
from quixstreams import Application
from sinks import HopsworksFeatureStoreSink


def main(
    kafka_broker_address: str,
    kafka_consumer_group: str,
    kafka_input_topic: str,
    feature_group_name: str,
    feature_group_version: int,
    output_sink: HopsworksFeatureStoreSink,
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

    sdf = app.dataframe(input_topic)

    # Sink data to the feature store
    sdf.sink(output_sink)

    app.run()


if __name__ == '__main__':
    from config import config, hopsworks_credentials

    hopsworks_sink = HopsworksFeatureStoreSink(
        # Hopsworks credentials
        api_key=hopsworks_credentials.hopsworks_api_key,
        project_name=hopsworks_credentials.hopsworks_project_name,
        # Feature group config
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
        feature_group_primary_keys=config.feature_group_primary_keys,
        feature_group_event_time=config.feature_group_event_time,
    )

    main(
        config.kafka_broker_address,
        config.kafka_consumer_group,
        config.kafka_input_topic,
        config.feature_group_name,
        config.feature_group_version,
        output_sink=hopsworks_sink,
    )
