"""Django urlpatterns declaration for nautobot_kafka_app app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_kafka_app import views


app_name = "nautobot_kafka_app"
router = NautobotUIViewSetRouter()

router.register("kafkamessage", views.KafkaMessageUIViewSet)

urlpatterns = [
    path(
        "docs/",
        RedirectView.as_view(url=static("nautobot_kafka_app/docs/index.html")),
        name="docs",
    ),
    path(
        "devices/<uuid:pk>",
        views.KafkaMessageDeviceListView.as_view(),
        name="device_kafkamessage_list",
    ),
]

urlpatterns += router.urls
