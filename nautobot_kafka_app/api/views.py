"""API views for nautobot_kafka_app."""

from nautobot.apps.api import NautobotModelViewSet

from nautobot_kafka_app import filters, models
from nautobot_kafka_app.api import serializers


class KafkaMessageViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """KafkaMessage viewset."""

    queryset = models.KafkaMessage.objects.all()
    serializer_class = serializers.KafkaMessageSerializer
    filterset_class = filters.KafkaMessageFilterSet
