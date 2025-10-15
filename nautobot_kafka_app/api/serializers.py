"""API serializers for nautobot_kafka_app."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from nautobot_kafka_app import models


class KafkaMessageSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """KafkaMessage Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.KafkaMessage

        fields = [
            "source",
            "event_type",
            "commit_id",
            "device",
            "message",
        ]

