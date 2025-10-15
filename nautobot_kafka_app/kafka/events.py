import logging
import os
from typing import Dict, Type
from confluent_kafka import Producer
from nautobot_kafka_app.constants import Constants
from nautobot_kafka_app.kafka.pydantic_models import (
    BaseEventData,
    KafkaEvent,
    EventData,
    DeviceEvent,
    InterfaceEvent,
    IPAddressEvent,
)
from nautobot.extras.models import ObjectChange

KAFKA_BROKER = os.environ.get(Constants.KAFKA_BROKER)
EVENT_MODEL_REGISTRY: Dict[str, Type[BaseEventData]] = {
    "dcim.device": DeviceEvent,
    "dcim.interface": InterfaceEvent,
    "ipam.ipaddress": IPAddressEvent,
}


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")


def produce_message(event: KafkaEvent, key: str) -> None:
    conf = {
        "bootstrap.servers": KAFKA_BROKER,
        "enable.idempotence": True,
    }
    producer = Producer(conf)

    try:
        producer.produce(
            topic=Constants.KAFKA_TOPIC,
            key=key.encode("utf-8"),
            value=event.json(),
            callback=delivery_report,
        )
        producer.flush()
    except Exception as e:
        logger.error(f"Failed to produce message for device {key}: {e}")


def build_kafka_event_from_model(
    change: ObjectChange,
    model_cls: Type[BaseEventData],
    source: str = Constants.SOURCE,
    severity: str = Constants.SEVERITY,
) -> tuple[str, KafkaEvent]:
    """
    Generic event generator for Pydantic models subclass of BaseEventData.
    """
    obj = model_cls(**change.object_data_v2, event_type=change.action)

    event = KafkaEvent(
        source=source,
        device=obj.device_name,
        event=EventData(
            type=obj.event_type,
            category=obj.object_type,
            message=f"{change.action} | {obj}",
        ),
        timestamp=change.time,
        severity=severity,
        log_id=str(change.id),
    )

    return obj.key, event
