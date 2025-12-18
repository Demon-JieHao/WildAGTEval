# Import all tools

from CommunicationController.tools.find_contact import FindContact
from CommunicationController.tools.make_call import MakeCall
from CommunicationController.tools.end_call import EndCall
from CommunicationController.tools.send_message import SendMessage
from CommunicationController.tools.get_messages import GetMessages
from CommunicationController.tools.get_call_history import GetCallHistory
from CommunicationController.tools.find_call_device import FindCallDevice

# List of all tools for automatic registration
ALL_TOOLS = [
    FindContact,
    MakeCall,
    EndCall,
    SendMessage,
    GetMessages,
    GetCallHistory,
    FindCallDevice
]
