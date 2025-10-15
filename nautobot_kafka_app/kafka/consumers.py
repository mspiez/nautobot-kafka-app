import os
import json
import logging
from confluent_kafka import Consumer, TopicPartition
from nautobot.apps.jobs import register_jobs
from nautobot.extras import jobs
from nautobot_kafka_app.models import KafkaMessage
from nautobot_kafka_app.kafka.pydantic_models import ParsedKafkaMessage
from nautobot_kafka_app.constants import Constants


KAFKA_BROKER = os.environ.get(Constants.KAFKA_BROKER)
KAFKA_TOPIC = Constants.KAFKA_TOPIC


def get_last_commit_id() -> int:
    last_commit = KafkaMessage.objects.order_by("-commit_id").first()
    return last_commit.commit_id if last_commit else 0


def insert_message(commit_id: int, payload: dict) -> None:
    try:
        parsed_msg = ParsedKafkaMessage(commit_id=commit_id, **payload)
        KafkaMessage.objects.create(**parsed_msg.to_django_kwargs())
        logging.info(
            f"Inserted message with commit_id {commit_id} for device={parsed_msg.device}"
        )
    except Exception as e:
        logging.error(f"Failed to insert message: {e}, payload={payload}")


class KafkaConsumerJob(jobs.Job):
    class Meta:
        name = "Kafka Consumer Job"
        description = "Consumes messages from Kafka and stores them in the database."

    def run(self):
        self.consume_messages()

    def consume_messages(self) -> None:
        last_commit_id = get_last_commit_id()
        consumer = Consumer(
            {
                "bootstrap.servers": KAFKA_BROKER,
                "group.id": "test",
                "enable.auto.commit": False,
            }
        )

        if last_commit_id:
            last_commit_id += 1

        consumer.assign([TopicPartition(KAFKA_TOPIC, 0, last_commit_id)])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                self.logger.info("Message: None")
                break
            if msg.error():
                self.logger.error(f"Kafka error: {msg.error()}")
                break

            commit_id = msg.offset()
            try:
                payload = json.loads(msg.value().decode("utf-8"))
                insert_message(commit_id, payload)
                self.logger.info(f"Message inserted: {payload}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to decode JSON: {e}, raw={msg.value()}")

        consumer.close()


register_jobs(KafkaConsumerJob)
