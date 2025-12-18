# Copyright SmartHomeEnv

from .power_on import PowerOn
from .power_off import PowerOff
from .brightness_adjust import BrightnessAdjust
from .color_set import ColorSet
from .temperature_set import TemperatureSet
from .mode_set import ModeSet
from .volume_adjust import VolumeAdjust
from .channel_change import ChannelChange
from .lock_lock import LockLock
from .lock_unlock import LockUnlock
from .lock_status import LockStatus
from .open_open import OpenOpen
from .open_close import OpenClose
from .open_set_position import OpenSetPosition
# from .find_device_by_name import FindDeviceByName
from .get_device_details import GetDeviceDetails
from .get_group_devices import GetGroupDevices
from .get_user_inventory import GetUserInventory
# from .think import Think


ALL_TOOLS = [
    PowerOn,
    PowerOff,
    BrightnessAdjust,
    ColorSet,
    TemperatureSet,
    ModeSet,
    VolumeAdjust,
    ChannelChange,
    LockLock,
    LockUnlock,
    LockStatus,
    OpenOpen,
    OpenClose,
    OpenSetPosition,
    # FindDeviceByName,
    GetDeviceDetails,
    GetGroupDevices,
    GetUserInventory,
    # Think,
]
