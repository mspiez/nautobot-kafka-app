from enum import StrEnum


class Constants:
    SOURCE = "nautobot"
    DEVICE_SCOPE = "device"
    SEVERITY = "info"
    KAFKA_TOPIC = "nautobot"
    KAFKA_BROKER = "KAFKA_BROKER"
    NAUTOBOT_EVENT_TYPE = "object_event"
    PAGINATION = 50
    UPDATE_EVENT = "update"
    APP_LABEL_DEVICE = "dcim"
    MODEL_DEVICE = "device"
    MODEL_INTERFACE = "interface"
    LOG_ID_FIELD = "log_id"


class EventActionEnums(StrEnum):
    CREATE = "create"
    DELETE = "delete"
    UPDATE = "update"


class TestConstants:
    STATUS_ACTIVE = "active"
    TEST_NAME = "test"
    DEVICE_1_ID = "eb640dce-5e44-4450-83b6-90e54c09e6f1"
    DEVICE_1_NAME = "router1"
    DEVICE_OBJECT_TYPE = "dcim.device"
    INTERFACE_1_ID = "eb640dce-5e44-4450-83b6-90e54c09e6f2"
    INTERFACE_1_NAME = "GigabitEthernet0/0/1"
    INTERFACE_OBJECT_TYPE = "dcim.interface"
    IP_ADDRESS_1 = "10.10.10.8/30"
    IP_ADDRESS_1_ID = "62d117c2-0909-42f7-bb21-b7e3a37faa28"
    IP_ADDRESS_OBJECT_TYPE = "ipam.ip_address"
