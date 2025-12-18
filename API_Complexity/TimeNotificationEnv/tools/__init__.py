# Import all tools

from TimeNotificationEnv.tools.create_alarm import CreateAlarm
from TimeNotificationEnv.tools.get_alarms import GetAlarms
from TimeNotificationEnv.tools.delete_alarm import DeleteAlarm
from TimeNotificationEnv.tools.create_reminder import CreateReminder
from TimeNotificationEnv.tools.get_reminders import GetReminders
from TimeNotificationEnv.tools.create_notification import CreateNotification
from TimeNotificationEnv.tools.get_notifications import GetNotifications
from TimeNotificationEnv.tools.set_notification_preferences import SetNotificationPreferences

# List of all tools for automatic registration
ALL_TOOLS = [
    CreateAlarm,
    GetAlarms,
    DeleteAlarm,
    CreateReminder,
    GetReminders,
    CreateNotification,
    GetNotifications,
    SetNotificationPreferences
]
