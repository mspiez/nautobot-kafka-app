from django import forms


from nautobot.apps.forms import (
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    TagsBulkEditFormMixin,
)

from nautobot_kafka_app import models


class KafkaMessageForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """KafkaMessage creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.KafkaMessage
        fields = [
            "device",
            "source",
            "event_type",
            "commit_id",
        ]


class KafkaMessageBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """KafkaMessage bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.KafkaMessage.objects.all(), widget=forms.MultipleHiddenInput
    )
    device = forms.CharField(required=False)
    source = forms.CharField(required=False)
    event_type = forms.CharField(required=False)
    commit_id = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""



class KafkaMessageFilterForm(NautobotFilterForm):
    """Filter form to filter searches."""

    model = models.KafkaMessage
    field_order = ["q", "device", "source", "event_type"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within device.",
    )
    device = forms.CharField(required=False, label="Device")
