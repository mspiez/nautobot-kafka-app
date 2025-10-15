
from nautobot_kafka_app.kafka.pydantic_models import (
    DeviceEvent,
    InterfaceEvent,
    IPAddressEvent,
)
from nautobot.core.testing import TestCase
from nautobot_kafka_app.tests.payloads import (
    DeviceEventEnum,
    InterfaceEventEnum,
    IpAddressEventEnum,
)
from nautobot_kafka_app.constants import EventActionEnums, TestConstants
from nautobot.dcim.models import (
    Device,
    DeviceType,
    LocationType,
    Manufacturer,
    Location,
    Platform,
)
from nautobot.extras.models import Role, Status
from django.contrib.contenttypes.models import ContentType


class PydanticModelsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PydanticModelsTestCase, cls).setUpClass()
        active_status = Status.objects.get(name=TestConstants.STATUS_ACTIVE)
        device_ct = ContentType.objects.get_for_model(Device)

        lc, _ = LocationType.objects.get_or_create(name=TestConstants.TEST_NAME)
        lc.content_types.add(device_ct)

        manufacturer = Manufacturer.objects.create(name=TestConstants.TEST_NAME)
        platform = Platform.objects.create(
            manufacturer=manufacturer,
            name=TestConstants.TEST_NAME,
        )
        role, _ = Role.objects.get_or_create(name=TestConstants.TEST_NAME)
        role.content_types.set([device_ct])

        device_type = DeviceType.objects.create(
            model=TestConstants.TEST_NAME, manufacturer=manufacturer
        )
        site, _ = Location.objects.get_or_create(
            name=TestConstants.TEST_NAME, status=active_status, location_type=lc
        )
        Device.objects.create(
            id=TestConstants.DEVICE_1_ID,
            name=TestConstants.DEVICE_1_NAME,
            device_type=device_type,
            platform=platform,
            status=active_status,
            role=role,
            location=site,
        )

    def test_device_create_event(self):
        change = DeviceEventEnum.CREATE.value
        device_event = DeviceEvent(**change.object_data_v2, event_type=change.action)

        assert device_event.name == TestConstants.DEVICE_1_NAME
        assert device_event.device_name == TestConstants.DEVICE_1_NAME
        assert device_event.key == TestConstants.DEVICE_1_NAME
        assert device_event.event_type == EventActionEnums.CREATE
        assert device_event.object_type == TestConstants.DEVICE_OBJECT_TYPE

    def test_device_update_event(self):
        change = DeviceEventEnum.UPDATE.value
        device_event = DeviceEvent(**change.object_data_v2, event_type=change.action)

        assert device_event.name == TestConstants.DEVICE_1_NAME
        assert device_event.device_name == TestConstants.DEVICE_1_NAME
        assert device_event.key == TestConstants.DEVICE_1_NAME
        assert device_event.event_type == EventActionEnums.UPDATE
        assert device_event.object_type == TestConstants.DEVICE_OBJECT_TYPE

    def test_device_delete_event(self):
        change = DeviceEventEnum.DELETE.value
        device_event = DeviceEvent(**change.object_data_v2, event_type=change.action)

        assert device_event.name == TestConstants.DEVICE_1_NAME
        assert device_event.device_name == TestConstants.DEVICE_1_NAME
        assert device_event.key == TestConstants.DEVICE_1_NAME
        assert device_event.event_type == EventActionEnums.DELETE
        assert device_event.object_type == TestConstants.DEVICE_OBJECT_TYPE

    def test_interface_create_event(self):
        change = InterfaceEventEnum.CREATE.value
        interface_event = InterfaceEvent(
            **change.object_data_v2, event_type=change.action
        )

        assert interface_event.name == TestConstants.INTERFACE_1_NAME
        assert interface_event.device.name == TestConstants.DEVICE_1_NAME
        assert interface_event.device_name == TestConstants.DEVICE_1_NAME
        assert interface_event.key == TestConstants.DEVICE_1_NAME
        assert interface_event.event_type == EventActionEnums.CREATE
        assert interface_event.object_type == TestConstants.INTERFACE_OBJECT_TYPE

    def test_interface_update_event(self):
        change = InterfaceEventEnum.UPDATE.value
        interface_event = InterfaceEvent(
            **change.object_data_v2, event_type=change.action
        )

        assert interface_event.name == TestConstants.INTERFACE_1_NAME
        assert interface_event.device.name == TestConstants.DEVICE_1_NAME
        assert interface_event.device_name == TestConstants.DEVICE_1_NAME
        assert interface_event.key == TestConstants.DEVICE_1_NAME
        assert interface_event.event_type == EventActionEnums.UPDATE
        assert interface_event.object_type == TestConstants.INTERFACE_OBJECT_TYPE

    def test_interface_delete_event(self):
        change = InterfaceEventEnum.DELETE.value
        interface_event = InterfaceEvent(
            **change.object_data_v2, event_type=change.action
        )

        assert interface_event.name == TestConstants.INTERFACE_1_NAME
        assert interface_event.device.name == TestConstants.DEVICE_1_NAME
        assert interface_event.device_name == TestConstants.DEVICE_1_NAME
        assert interface_event.key == TestConstants.DEVICE_1_NAME
        assert interface_event.event_type == EventActionEnums.DELETE
        assert interface_event.object_type == TestConstants.INTERFACE_OBJECT_TYPE

    def test_ip_address_create_event(self):
        change = IpAddressEventEnum.CREATE.value
        ip_address_event = IPAddressEvent(
            **change.object_data_v2, event_type=change.action
        )

        assert ip_address_event.address == TestConstants.IP_ADDRESS_1
        assert ip_address_event.key == TestConstants.IP_ADDRESS_1
        assert ip_address_event.event_type == EventActionEnums.CREATE
        assert ip_address_event.object_type == TestConstants.IP_ADDRESS_OBJECT_TYPE

    def test_ip_address_update_event_with_interface(self):
        change = IpAddressEventEnum.UPDATE_WITH_INTERFACE.value
        ip_address_event = IPAddressEvent(
            **change.object_data_v2, event_type=change.action
        )

        assert ip_address_event.address == TestConstants.IP_ADDRESS_1
        assert ip_address_event.event_type == EventActionEnums.UPDATE
        assert ip_address_event.object_type == TestConstants.IP_ADDRESS_OBJECT_TYPE
        assert ip_address_event.device_name == TestConstants.DEVICE_1_NAME
        assert ip_address_event.key == TestConstants.DEVICE_1_NAME

    def test_ip_address_delete_event_with_interface(self):
        change = IpAddressEventEnum.DELETE_WITH_INTERFACE.value
        ip_address_event = IPAddressEvent(
            **change.object_data_v2, event_type=change.action
        )

        assert ip_address_event.address == TestConstants.IP_ADDRESS_1
        assert ip_address_event.event_type == EventActionEnums.DELETE
        assert ip_address_event.object_type == TestConstants.IP_ADDRESS_OBJECT_TYPE
        assert ip_address_event.device_name == TestConstants.DEVICE_1_NAME
        assert ip_address_event.key == TestConstants.DEVICE_1_NAME
