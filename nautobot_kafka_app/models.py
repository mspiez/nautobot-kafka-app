from django.db import models
from nautobot.apps.models import PrimaryModel
from nautobot.dcim.models import Device
from django.urls import reverse


class KafkaMessage(PrimaryModel):
    device = models.ForeignKey(Device, blank=True, null=True, on_delete=models.SET_NULL)
    commit_id = models.BigIntegerField(unique=True)
    source = models.CharField(max_length=255, default="unknown")
    event_type = models.CharField(max_length=50, default="unknown")
    category = models.CharField(max_length=100, default="unknown")
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    raw_message = models.JSONField(blank=True, null=True)
    severity = models.CharField(max_length=100, null=True, blank=True, default="info")
    log_id = models.UUIDField(null=True, blank=True, db_index=True)

    class Meta:
        """Meta class."""

        ordering = ["device", "commit_id", "source", "event_type", "message"]

    def __str__(self):
        return f"KafkaMessage {self.commit_id} - {self.event_type}"

    @property
    def log_url(self):
        """Direct link to Nautobot's changelog view for this log_id (if available)."""
        if not self.log_id:
            return None
        return reverse("extras:objectchange", args=[self.log_id])
