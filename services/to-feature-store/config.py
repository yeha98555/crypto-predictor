from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str
    feature_group_name: str
    feature_group_version: int


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='credentials.env', env_file_encoding='utf-8'
    )
    hopsworks_api_key: str


config = Config()
hopsworks_credentials = HopsworksCredentials()
