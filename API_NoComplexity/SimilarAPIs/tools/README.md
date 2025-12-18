# Similar APIs Implementation

This directory contains implementations of "Similar APIs" for various domain functions that exhibited unclear functionality boundaries. Each implementation represents the "alternative" or "similar" API that could be confused with the original API, causing developer uncertainty.

## Implemented APIs (41/34)

### CulinaryControlEnv
1. `place_pickup_order.py` - Similar to `place_delivery_order`
2. `place_restaurant_order.py` - Similar to `place_delivery_order`
3. `place_delivery_order.py` - Similar to original function with similar name

### CommunicationController
4. `initiate_call_session.py` - Similar to `make_call`
5. `find_communication_device.py` - Similar to `find_call_device`
6. `search_contact_directory.py` - Similar to `find_contact`
7. `sync_messages.py` - Similar to `get_messages`
8. `send_notification.py` - Similar to `send_message`
9. `send_chat_message.py` - Similar to `send_message`

### MediaControlEnv
10. `get_content_details.py` - Similar to `get_media_details`
11. `play_stream.py` - Similar to `play`

### SmartHomeEnv
12. `lock_lock.py` - Similar to `lock_unlock`
13. `lock_toggle.py` - Similar to `lock_unlock`
14. `brightness_transition.py` - Similar to `brightness_adjust`
15. `channel_select.py` - Similar to `channel_change`
16. `find_device_by_id.py` - Similar to `find_device_by_name`
17. `search_devices.py` - Similar to `find_device_by_name`
18. `light_color_set.py` - Similar to `color_set`
19. `color_temperature_set.py` - Similar to `color_set`
20. `color_scene_set.py` - Similar to `color_set`
21. `device_status_get.py` - Similar to `get_device_details`
22. `get_device_collection.py` - Similar to `get_group_devices`
23. `get_device_inventory.py` - Similar to `get_user_inventory`
24. `hvac_mode_set.py` - Similar to `mode_set`
25. `toggle_blinds.py` - Similar to `open_close`
26. `open_window.py` - Similar to `open_open`
27. `open_adjust_position.py` - Similar to `open_set_position`
28. `device_deactivate.py` - Similar to `power_off`
29. `activate_device.py` - Similar to `power_on`
30. `temperature_adjust.py` - Similar to `temperature_set`
31. `temperature_schedule.py` - Similar to `temperature_set`
32. `analyze.py` - Similar to `think`
33. `audio_settings_adjust.py` - Similar to `volume_adjust`

### TimeNotificationEnv
34. `broadcast_alert.py` - Similar to `create_notification`
35. `create_timer.py` - Similar to `create_alarm`
36. `schedule_action.py` - Similar to `create_alarm`
37. `fetch_notification_status.py` - Similar to `get_notifications`
38. `get_alerts.py` - Similar to `get_alarms`
39. `get_calendar_events.py` - Similar to `get_reminders`
40. `create_calendar_event.py` - Similar to `create_reminder`
41. `set_app_notification_preferences.py` - Similar to `set_notification_preferences`

## Implementation Details

Each implemented file follows a standard structure:
1. Import necessary libraries
2. Define helper functions if needed
3. Create a Tool class that matches the API structure of the domain
4. Implement the `invoke` static method with appropriate parameters
5. Add proper validation, error handling, and functionality

These implementations demonstrate the realistic characteristics and potential confusion points that could arise between similar APIs in the same domain.

## Common Uncertainty Patterns

Through these implementations, we've demonstrated several common uncertainty patterns:
1. **Similar Naming** - Functions with similar names but different behaviors (e.g., `temperature_set` vs `temperature_adjust` vs `temperature_schedule`)
2. **Overlapping Functionality** - Functions that control similar aspects but in different ways (e.g., `volume_adjust` vs `audio_settings_adjust`)
3. **Different Abstraction Levels** - Functions that operate at different abstraction levels (e.g., `power_on` vs `activate_device`)
4. **Complementary Functions** - Functions that perform opposite operations but are named similarly (e.g., `open_open` vs `open_close`)
5. **Scope Differences** - Functions that operate on similar objects but with different scopes (e.g., `get_device_details` vs `device_status_get`)
6. **Domain Confusion** - Functions that have similar names across domains but with different behaviors (e.g., `create_notification` vs `broadcast_alert`)
7. **Temporal Differences** - Functions that operate with different time orientations (e.g., `create_alarm` that uses absolute times vs `create_timer` that uses durations)
8. **Granularity Differences** - Functions that operate at different levels of granularity (e.g., `set_notification_preferences` for system-wide settings vs `set_app_notification_preferences` for application-specific settings)
