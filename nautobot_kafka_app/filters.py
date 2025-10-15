"""Filtering for nautobot_kafka_app."""

import django_filters
from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet

from nautobot_kafka_app import models


class KafkaMessageFilterSet(NautobotFilterSet, NameSearchFilterSet):
    """Filter for KafkaMessage."""

    device_name = django_filters.CharFilter(
        field_name="device__name", lookup_expr="icontains", label="Device Name"
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.KafkaMessage

        fields = ["id", "device", "device_name", "source", "event_type"]
