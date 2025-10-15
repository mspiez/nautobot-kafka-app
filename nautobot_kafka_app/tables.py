"""Tables for nautobot_kafka_app."""

import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ButtonsColumn, ToggleColumn
from django.utils.html import format_html

from nautobot_kafka_app import models


class KafkaMessageTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    device = tables.Column(linkify=True)
    commit_id = tables.Column()
    source = tables.Column()
    event_type = tables.Column()
    message = tables.Column()
    actions = ButtonsColumn(
        models.KafkaMessage,
        pk_field="pk",
    )
    view_log = tables.Column(empty_values=(), orderable=False, verbose_name="View Log")

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.KafkaMessage
        fields = (
            "pk",
            "commit_id",
            "source",
            "device",
            "event_type",
            "category",
            "message",
            "timestamp",
            "severity",
            "view_log",
        )

    def render_view_log(self, record):
        """Render 'View Log' link if log_id exists."""
        if record.log_id:
            return format_html(
                '<a href="/extras/object-changes/{}/">View Log</a>', record.log_id
            )
        return "-"
