from nautobot.apps.jobs import register_jobs
from nautobot.extras.jobs import JobHookReceiver
from nautobot_kafka_app.kafka.events import (
    build_kafka_event_from_model,
    EVENT_MODEL_REGISTRY,
    produce_message,
)
from nautobot_kafka_app.kafka.pydantic_models import BaseEventData
from nautobot.extras.models import ObjectChange


class KafkaProducerJob(JobHookReceiver):
    class Meta:
        name = "Kafka Producer Job"
        description = "Produces messages to Kafka from Nautobot."

    def receive_job_hook(self, change: ObjectChange, action: str, changed_object):
        self.logger.info("change: %s - %s - %s", change, action, changed_object)

        object_type = change.object_data_v2.get("object_type")
        model_cls = EVENT_MODEL_REGISTRY.get(object_type, BaseEventData)

        key, event = build_kafka_event_from_model(change, model_cls)

        self.logger.info(event.json())
        produce_message(event, key)


register_jobs(KafkaProducerJob)
