# Copyright SimilarAPIs

from .broadcast_alert import BroadcastAlert
from .color_scene_set import ColorSceneSet
from .color_temperature_set import ColorTemperatureSet
from .create_calendar_event import CreateCalendarEvent
from .create_timer import CreateTimer
from .device_deactivate import DeviceDeactivate
from .fetch_notification_status import FetchNotificationStatus
from .find_communication_device import FindCommunicationDevice
from .get_calendar_events import GetCalendarEvents
from .get_content_details import GetContentDetails
from .get_device_inventory import GetDeviceInventory
from .hvac_mode_set import HVACModeSet
from .initiate_call_session import CallSessionManager
from .place_pickup_order import PlacePickupOrder
from .place_restaurant_order import PlaceRestaurantOrder
from .schedule_action import ScheduleAction
from .search_contact_directory import SearchContactDirectory
from .send_chat_message import SendChatMessage
from .sync_messages import SyncMessages
from .temperature_schedule import TemperatureSchedule


ALL_TOOLS = [
    BroadcastAlert,
    ColorSceneSet,
    ColorTemperatureSet,
    CreateCalendarEvent,
    CreateTimer,
    DeviceDeactivate,
    FetchNotificationStatus,
    FindCommunicationDevice,
    GetCalendarEvents,
    GetContentDetails,
    GetDeviceInventory,
    HVACModeSet,
    CallSessionManager,
    PlacePickupOrder,
    PlaceRestaurantOrder,
    ScheduleAction,
    SearchContactDirectory,
    SendChatMessage,
    SyncMessages,
    TemperatureSchedule,
]
