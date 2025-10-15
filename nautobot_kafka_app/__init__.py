from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotKafkaAppConfig(NautobotAppConfig):
    """App configuration for the nautobot_kafka_app."""

    name = "nautobot_kafka_app"
    verbose_name = "Nautobot Kafka App"
    version = "0.1.0"
    author = "Michal Spiez"
    description = "Nautobot Kafka App."
    base_url = "nautobot-kafka-app"
    required_settings = []
    default_settings = {}
    caching_config = {}


config = NautobotKafkaAppConfig
