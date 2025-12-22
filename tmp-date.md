APIs with Date-Related Parameters/Logic
1. CulinaryControlEnv (High Impact)
API	Date Fields	Issue
create_meal_plan	start_date, end_date (YYYY-MM-DD)	Data uses 2025-07-17 as start dates
schedule_meal	day (YYYY-MM-DD)	Data schedules meals for 2025-07-22, 2025-07-23, etc.
2. TimeNotificationEnv (High Impact)
API	Date Fields	Issue
create_reminder	date (YYYY-MM-DD), time (HH:MM:SS)	Data creates reminders for 2025-07-24, 2025-07-25
get_reminders	date_from, date_to filters	Timestamps in context use 2025-07-17T14:10:...
create_alarm	time (HH:MM:SS), days	Timestamps use July 2025
get_alarms	Returns timestamps	Timestamps in context use 2025-07-01T..., 2025-07-17T...
get_notifications	Returns timestamps	Timestamps use 2025-07-15T22:20:...
3. CommunicationController (Medium Impact)
API	Date Fields	Issue
get_call_history	time_range (ISO 8601 duration)	May compare against frozen time
get_messages	Returns message timestamps	Message timestamps may not match
4. TransactionEnv (Low-Medium Impact)
API	Date Fields	Issue
get_order_history	Order creation dates	Order timestamps
track_order	Estimated delivery dates	Delivery date calculations
