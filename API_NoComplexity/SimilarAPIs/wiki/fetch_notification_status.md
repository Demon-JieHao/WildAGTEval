## Fetch Notification Status

Fetch delivery status and interaction metrics for notifications sent to users. Returns aggregated metrics and detailed status information for each notification.

### Key Features

- Developers would be confused between the get_notifications function and this fetch_notification_status 
function that exists in the same notification ecosystem.
- While both functions retrieve notification-related 
data, they serve fundamentally different purposes.
- get_notifications returns the actual notification objects 
with their content, while this fetch_notification_status function provides metadata about notification 
delivery status, read receipts, and user interaction metrics.
- The similar naming and overlapping parameter 
sets create significant confusion about which function to use when developers need specific notification-related 
information.

### Error Cases

- **No user logged in**
- **Invalid date format**

