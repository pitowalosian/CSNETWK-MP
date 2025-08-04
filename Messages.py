import time
import uuid

timeStamp = int(time.time())
message_id = uuid.uuid4().hex[:8]
# === PROFILE MESSAGE FORMAT ===
def verboseProfMessage(display_name, ip_address, status, av_type, av_encoding, av_data):
    return f"""TYPE: PROFILE
USER_ID: {display_name}@{ip_address}
DISPLAY_NAME: {display_name}
STATUS: {status}
AVATAR_TYPE: {av_type}
AVATAR_ENCODING: {av_encoding}
AVATAR_DATA: {av_data}
"""

def simpleProfMessage(display_name, status):
    return f"""
USER_ID: {display_name}
STATUS: {status}
"""

# === POST MESSAGE FORMAT ===

# === DM MESSAGE FORMAT ===
def verboseDMMessage(sender, ip_address, userID, message):
    return f"""TYPE: DM
    FROM: {sender}@{ip_address}
    TO: {userID}
    CONTENT: {message}
    TIMESTAMP: {timeStamp}
    MESSAGE_ID: {message_id}
    TOKEN: {sender}@{ip_address}|{message_id}|chat
"""
def simpleDMMessage(sender, message):
    return f"""
    DISPLAY_NAME: {sender}
    CONTENT: {message}
    """

