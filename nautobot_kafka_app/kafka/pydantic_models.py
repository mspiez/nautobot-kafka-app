from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from nautobot.dcim.models import Device


class EventData(BaseModel):
    type: str = Field(
        ..., description="Event type, e.g. state_change, alert, object_change"
    )
    category: str = Field(..., description="Event category, e.g. telemetry:bgp_session")
    message: str = Field(..., description="Human readable message")


class KafkaEvent(BaseModel):
    source: str = Field(..., description="Origin: telemetry, nautobot, alertmanager")
    device: Optional[str] = Field(None, description="Device name")
    event: EventData
    timestamp: datetime = Field(..., description="Event timestamp in ISO8601 format")
    severity: Optional[str] = Field(
        "info", description="Optional. Severity of event: info, warning, critical"
    )
    log_id: Optional[str] = Field(
        None, description="UUID of corresponding ObjectChange entry (if applicable)"
    )


class ParsedKafkaMessage(BaseModel):
    commit_id: int
    source: str
    device: Optional[str]
    event: EventData
    timestamp: datetime
    severity: str
    log_id: Optional[UUID] = None

    def to_django_kwargs(self) -> dict:
        device_obj = (
            Device.objects.filter(name=self.device).first() if self.device else None
        )
        return {
            "commit_id": self.commit_id,
            "source": self.source,
            "device": device_obj,
            "event_type": self.event.type,
            "category": self.event.category,
            "message": self.event.message,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "log_id": self.log_id,
        }


class BaseEventData(BaseModel):
    id: str
    object_type: str | None = None
    event_type: str


class DeviceEvent(BaseEventData):
    name: Optional[str] = None

    @property
    def key(self) -> str:
        return self.name

    @property
    def device_name(self) -> str:
        return self.name

    def __str__(self):
        return self.name


class DeviceBase(BaseModel):
    id: str
    name: Optional[str] = None


class InterfaceEvent(BaseEventData):
    name: str
    device: DeviceBase

    @property
    def key(self) -> str:
        return self.device.name

    @property
    def device_name(self) -> str:
        return self.device.name

    def __str__(self):
        return f"{self.device.name} | {self.name}"


class InterfaceBase(BaseModel):
    name: str
    device: DeviceBase


class IPAddressEvent(BaseEventData):
    address: str
    interfaces: Optional[List[InterfaceBase]] = None

    @property
    def device_name(self) -> Optional[str]:
        if self.interfaces and self.interfaces[0].device:
            if getattr(self.interfaces[0].device, "name", None):
                return self.interfaces[0].device.name
            try:
                device = Device.objects.get(id=self.interfaces[0].device.id)
                return device.name
            except Device.DoesNotExist:
                return None
        return None

    @property
    def interface_name(self) -> Optional[str]:
        if self.interfaces:
            return self.interfaces[0].name
        return None

    @property
    def key(self) -> str:
        return self.device_name if self.device_name else self.address

    def __str__(self):
        if self.interfaces:
            return f"{self.address} | {self.device_name} | {self.interface_name}"
        return self.address

