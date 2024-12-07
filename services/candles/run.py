from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger
from quixstreams import Application
from quixstreams.models import TimestampType


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload instead of Kafka's timestamp.
    """
    return value['timestamp_ms']


def init_candle(trade: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['volume'],
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair'],
    }


def update_candle(acc: Dict[str, Any], trade: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'close': trade['price'],
        'high': max(acc['high'], trade['price']),
        'low': min(acc['low'], trade['price']),
        'volume': acc['volume'] + trade['volume'],
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair'],
    }


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
    emit_incomplete_candles: bool,
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
        emit_incomplete_candles (bool): Emit incomplete candles or just the final one

    Returns:
        None
    """
    logger.info('Starting the candles service')
    logger.info(f'Kafka broker address: {kafka_broker_address}')
    logger.info(f'Kafka input topic: {kafka_input_topic}')
    logger.info(f'Kafka output topic: {kafka_output_topic}')
    logger.info(f'Kafka consumer group: {kafka_consumer_group}')
    logger.info(f'Candle seconds: {candle_seconds}')
    logger.info(f'Emit incomplete candles: {emit_incomplete_candles}')
    # Initialize the QuixStreams application
    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    # Define the input and output topics
    input_topic = app.topic(
        name=kafka_input_topic,
        value_serializer='json',
        timestamp_extractor=custom_ts_extractor,
    )
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Create a Streaming Dataframe
    sdf = app.dataframe(topic=input_topic)

    # Aggregation of trades into candles using tumbling windows
    sdf = (
        # Define a tumbling window of 60 seconds
        sdf.tumbling_window(timedelta(seconds=candle_seconds))
        # Apply the reducer to update the candle, or initialize it with the first trade
        .reduce(reducer=update_candle, initializer=init_candle)
    )

    if emit_incomplete_candles:
        # Emit all intermediate candles to make the system more responsive
        sdf = sdf.current()
    else:
        # Emit the final candle only
        sdf = sdf.final()

    # Extract the values from the dataframe
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    sdf['timestamp_ms'] = sdf['value']['timestamp_ms']
    sdf['pair'] = sdf['value']['pair']
    # Extract the window start and end timestamps
    sdf['window_start_ms'] = sdf['start']
    sdf['window_end_ms'] = sdf['end']

    # Keep only the columns we need
    sdf = sdf[
        [
            'pair',
            'timestamp_ms',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'window_start_ms',
            'window_end_ms',
        ]
    ]

    # For debugging
    # sdf = sdf.update(lambda value: breakpoint())

    # sdf = sdf.print()
    sdf = sdf.apply(lambda x: logger.info(f'Candle: {x}'))

    # Push the candles to the output topic
    sdf.to_topic(topic=output_topic)

    # Start the application
    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
        emit_incomplete_candles=config.emit_incomplete_candles,
    )
