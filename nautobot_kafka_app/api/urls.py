"""Django API urlpatterns declaration for nautobot_kafka_app app."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_kafka_app.api import views

router = OrderedDefaultRouter()
router.register("kafkamessage", views.KafkaMessageViewSet)

app_name = "nautobot_kafka_app-api"
urlpatterns = router.urls
