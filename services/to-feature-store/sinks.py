import hopsworks
import pandas as pd
from quixstreams.sinks.base import BatchingSink, SinkBackpressureError, SinkBatch


class SinkError(Exception):
    def __init__(self, error_message: str, topic: str, partition: int):
        super().__init__(error_message)
        self.topic = topic
        self.partition = partition


class HopsworksFeatureStoreSink(BatchingSink):
    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],
        feature_group_event_time: str,
    ):
        """
        Initialize a connection to the Hopsworks Feature Store
        """
        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version

        # Establish a connection to the Hopsworks Feature Store
        project = hopsworks.login(api_key_value=api_key, project=project_name)
        self._fs = project.get_feature_store()

        # Get or create the feature group
        self._fg = self._fs.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,
        )

        # Call constructor of the parent class to make sure the batches are initialized
        super().__init__()

    def write(self, batch: SinkBatch):
        # Transform the batch into a pandas DataFrame
        data = [item.value for item in batch]
        data = pd.DataFrame(data)

        # Insert the data into the feature group
        try:
            self._fg.insert(data)
        except TimeoutError as err:
            # In case of a timeout, tell the app wait for 30 seconds and try again
            raise SinkBackpressureError(
                error_message='The feature group is currently overloaded. Please try again in 30 seconds.',
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err
        except ConnectionError as err:
            # Handle network-related errors
            raise SinkBackpressureError(
                error_message='Connection to the feature store failed. Please try again in 60 seconds.',
                retry_after=60.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err
        except ValueError as err:
            # Handle data validation or format errors
            raise SinkError(
                error_message=f'Invalid data format: {str(err)}',
                topic=batch.topic,
                partition=batch.partition,
            ) from err
        except Exception as err:
            # Handle unexpected errors
            raise SinkError(
                error_message=f'Unexpected error during feature group insertion: {str(err)}',
                topic=batch.topic,
                partition=batch.partition,
            ) from err
