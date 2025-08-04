import time
import uuid

timeStamp = int(time.time())
message_id1 = uuid.uuid4().int >> 64  # Generate a unique message ID
message_id = f"{message_id1:016x}"  # Convert to hex and remove '0x' prefix

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
def verbosePostMessage(display_name, ip_address, ttl, content, av_type, av_encoding, av_data):
    return f"""TYPE: POST
USER_ID: {display_name}@{ip_address}
CONTENT: {content}
TTL: {ttl}
MESSAGE_ID: {message_id}
TOKEN: {display_name}@{ip_address}|{timeStamp + ttl}|broadcast
"""
def simplePostMessage(display_name, content, av_type, av_encoding, av_data):
    message = f"""TYPE: POST
DISPLAY_NAME: {display_name}
CONTENT: {content}"""
    if av_type and av_encoding and av_data:
        message += f"""
AVATAR_TYPE: {av_type}
AVATAR_ENCODING: {av_encoding}
AVATAR_DATA: {av_data}"""
    return message

# === DM MESSAGE FORMAT ===
def verboseDMMessage(sender, ip_address, userID, message, ttl):
    return f"""TYPE: DM
FROM: {sender}@{ip_address}
TO: {userID}
CONTENT: {message}
TIMESTAMP: {timeStamp}
MESSAGE_ID: {message_id}
TOKEN: {sender}@{ip_address}|{message_id + ttl}|chat
"""
def simpleDMMessage(sender, message, av_type, av_encoding, av_data):
    dm = f"""
DISPLAY_NAME: {sender}
CONTENT: {message}
"""
    if av_type and av_encoding and av_data:
        dm += f"""
AVATAR_TYPE: {av_type}
AVATAR_ENCODING: {av_encoding}
AVATAR_DATA: {av_data}"""
    return dm

# === PING MESSAGE FORMAT ===
def pingMessage(display_name, ip_address):
    return f"""TYPE: PING
USER_ID: {display_name}@{ip_address}
"""

# === ACK MESSAGE FORMAT ===
def ackMessage(message_id, status):
    return f"""TYPE: ACK
MESSAGE_ID: {message_id}
STATUS: {status}
"""

# === FOLLOW MESSAGE FORMAT ===
def followVerboseMessage(follower, userID, ip_address, ttl):
    return f"""TYPE: FOLLOW
MESSAGE_ID: {message_id}
FROM: {follower}@{ip_address}
TO: {userID}
TIMESTAMP: {timeStamp}
TOKEN: {follower}@{ip_address}|{timeStamp + ttl}|follow
"""
def followSimpleMessage(follower):
    return f"""User {follower} has followed you"""

# === UNFOLLOW MESSAGE FORMAT ===
def unfollowMessage(follower, userID, ip_address, ttl):
    return f"""TYPE: UNFOLLOW
MESSAGE_ID: {message_id}
FROM: {follower}@{ip_address}
TO: {userID}
TIMESTAMP: {timeStamp}
TOKEN: {follower}@{ip_address}|{timeStamp + ttl}|follow
"""
def unfollowSimpleMessage(follower):
    return f"""User {follower} has unfollowed you"""
