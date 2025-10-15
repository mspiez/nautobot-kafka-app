"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:nautobot_kafka_app:kafkamessage_list",
        name="Nautobot Kafka App",
        permissions=["nautobot_kafka_app.view_kafkamessage"],
        buttons=(
            NavMenuAddButton(
                link="plugins:nautobot_kafka_app:kafkamessage_add",
                permissions=["nautobot_kafka_app.add_kafkamessage"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Nautobot Kafka App", items=tuple(items)),),
    ),
)
