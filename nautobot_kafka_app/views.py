from nautobot.apps.views import NautobotUIViewSet, ObjectView
from nautobot.dcim.models import Device

from nautobot_kafka_app import filters, forms, models, tables
from nautobot_kafka_app.api import serializers
from nautobot_kafka_app.models import KafkaMessage


class KafkaMessageUIViewSet(NautobotUIViewSet):
    """ViewSet for KafkaMessage views."""

    bulk_update_form_class = forms.KafkaMessageBulkEditForm
    filterset_class = filters.KafkaMessageFilterSet
    filterset_form_class = forms.KafkaMessageFilterForm
    form_class = forms.KafkaMessageForm
    lookup_field = "pk"
    queryset = models.KafkaMessage.objects.all()
    serializer_class = serializers.KafkaMessageSerializer
    table_class = tables.KafkaMessageTable


class KafkaMessageDeviceListView(ObjectView):
    """Device-scoped KafkaMessage list."""

    queryset = Device.objects.all()
    template_name = "nautobot_kafka_app/template.html"

    def get_extra_context(self, request, instance):
        table = tables.KafkaMessageTable(
            data=KafkaMessage.objects.filter(device=instance),
            user=request.user,
            orderable=False,
        )

        return {
            "table": table,
            "active_tab": "kafka-messages",
        }
