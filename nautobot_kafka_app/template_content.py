from django.urls import reverse
from nautobot.apps.ui import TemplateExtension


class DeviceKafkaMessagesTab(TemplateExtension):
    model = "dcim.device"

    def detail_tabs(self):
        return [
            {
                "title": "Kafka Messages",
                "url": reverse(
                    "plugins:nautobot_kafka_app:device_kafkamessage_list",
                    kwargs={"pk": self.context["object"].pk},
                ),
            }
        ]


template_extensions = [DeviceKafkaMessagesTab]
