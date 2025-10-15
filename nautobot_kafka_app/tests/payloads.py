from dataclasses import dataclass
from enum import Enum
from nautobot_kafka_app.constants import TestConstants, EventActionEnums


@dataclass(frozen=True)
class FakeChange:
    action: str
    object_data_v2: dict


class DeviceEventEnum(Enum):
    CREATE = FakeChange(
        action=EventActionEnums.CREATE,
        object_data_v2={
            "id": TestConstants.DEVICE_1_ID,
            "name": TestConstants.DEVICE_1_NAME,
            "object_type": TestConstants.DEVICE_OBJECT_TYPE,
        },
    )
    UPDATE = FakeChange(
        action=EventActionEnums.UPDATE,
        object_data_v2={
            "id": TestConstants.DEVICE_1_ID,
            "name": TestConstants.DEVICE_1_NAME,
            "object_type": TestConstants.DEVICE_OBJECT_TYPE,
        },
    )
    DELETE = FakeChange(
        action=EventActionEnums.DELETE,
        object_data_v2={
            "id": TestConstants.DEVICE_1_ID,
            "name": TestConstants.DEVICE_1_NAME,
            "object_type": TestConstants.DEVICE_OBJECT_TYPE,
        },
    )


class InterfaceEventEnum(Enum):
    CREATE = FakeChange(
        action=EventActionEnums.CREATE,
        object_data_v2={
            "id": TestConstants.INTERFACE_1_ID,
            "name": TestConstants.INTERFACE_1_NAME,
            "object_type": TestConstants.INTERFACE_OBJECT_TYPE,
            "device": {
                "id": TestConstants.DEVICE_1_ID,
                "name": TestConstants.DEVICE_1_NAME,
            },
        },
    )
    UPDATE = FakeChange(
        action=EventActionEnums.UPDATE,
        object_data_v2={
            "id": TestConstants.INTERFACE_1_ID,
            "name": TestConstants.INTERFACE_1_NAME,
            "object_type": TestConstants.INTERFACE_OBJECT_TYPE,
            "device": {
                "id": TestConstants.DEVICE_1_ID,
                "name": TestConstants.DEVICE_1_NAME,
            },
        },
    )
    DELETE = FakeChange(
        action=EventActionEnums.DELETE,
        object_data_v2={
            "id": TestConstants.INTERFACE_1_ID,
            "name": TestConstants.INTERFACE_1_NAME,
            "object_type": TestConstants.INTERFACE_OBJECT_TYPE,
            "device": {
                "id": TestConstants.DEVICE_1_ID,
                "name": TestConstants.DEVICE_1_NAME,
            },
        },
    )


class IpAddressEventEnum(Enum):
    CREATE = FakeChange(
        action=EventActionEnums.CREATE,
        object_data_v2={
            "id": TestConstants.IP_ADDRESS_1_ID,
            "address": TestConstants.IP_ADDRESS_1,
            "object_type": TestConstants.IP_ADDRESS_OBJECT_TYPE,
        },
    )
    UPDATE_WITH_INTERFACE = FakeChange(
        action=EventActionEnums.UPDATE,
        object_data_v2={
            "id": TestConstants.IP_ADDRESS_1_ID,
            "address": TestConstants.IP_ADDRESS_1,
            "object_type": TestConstants.IP_ADDRESS_OBJECT_TYPE,
            "interfaces": [
                {
                    "id": TestConstants.INTERFACE_1_ID,
                    "name": TestConstants.INTERFACE_1_NAME,
                    "device": {
                        "id": TestConstants.DEVICE_1_ID,
                        "object_type": TestConstants.DEVICE_OBJECT_TYPE,
                    },
                }
            ],
        },
    )
    DELETE_WITH_INTERFACE = FakeChange(
        action=EventActionEnums.DELETE,
        object_data_v2={
            "id": TestConstants.IP_ADDRESS_1_ID,
            "address": TestConstants.IP_ADDRESS_1,
            "object_type": TestConstants.IP_ADDRESS_OBJECT_TYPE,
            "interfaces": [
                {
                    "id": TestConstants.INTERFACE_1_ID,
                    "name": TestConstants.INTERFACE_1_NAME,
                    "device": {
                        "id": TestConstants.DEVICE_1_ID,
                        "object_type": TestConstants.DEVICE_OBJECT_TYPE,
                    },
                }
            ],
        },
    )
