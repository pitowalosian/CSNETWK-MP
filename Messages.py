import time
import uuid

timeStamp = int(time.time())
message_id1 = uuid.uuid4().int >> 64  # Generate a unique message ID
message_id = f"{message_id1:016x}"  # Convert to hex and remove '0x' prefix

# === PROFILE MESSAGE FORMAT ===
def verboseProfMessage(display_name, ip_address, status):
    return f"""\nTYPE: PROFILE
USER_ID: {display_name}@{ip_address}
DISPLAY_NAME: {display_name}
STATUS: {status}
"""
def simpleProfMessage(display_name, status):
    return f"""\nTYPE: PROFILE
DISPLAY_NAME: {display_name}
STATUS: {status}
"""

# === POST MESSAGE FORMAT ===
def verbosePostMessage(display_name, ip_address, ttl, content):
    return f"""\nTYPE: POST
USER_ID: {display_name}@{ip_address}
CONTENT: {content}
TTL: {ttl}
MESSAGE_ID: {message_id}
TOKEN: {display_name}@{ip_address}|{timeStamp + ttl}|broadcast
"""
def simplePostMessage(display_name, content):
    message = f"""\nTYPE: POST
DISPLAY_NAME: {display_name}
CONTENT: {content}"""
#     if av_type and av_encoding and av_data:
#         message += f"""
# AVATAR_\nTYPE: {av_type}
# AVATAR_ENCODING: {av_encoding}
# AVATAR_DATA: {av_data}"""
    return message

# === DM MESSAGE FORMAT ===
def verboseDMMessage(sender, ip_address, userID, message, ttl):
    return f"""\nTYPE: DM
FROM: {sender}@{ip_address}
TO: {userID}
CONTENT: {message}
TIMESTAMP: {timeStamp}
MESSAGE_ID: {message_id}
TOKEN: {sender}@{ip_address}|{timeStamp + ttl}|chat
"""
def simpleDMMessage(sender, message):
    dm = f"""\nTYPE: DM
DISPLAY_NAME: {sender}
CONTENT: {message}
"""
#     if av_type and av_encoding and av_data:
#         dm += f"""
# AVATAR_\nTYPE: {av_type}
# AVATAR_ENCODING: {av_encoding}
# AVATAR_DATA: {av_data}"""
    return dm

# === PING MESSAGE FORMAT ===
def pingMessage(display_name, ip_address):
    return f"""\nTYPE: PING
USER_ID: {display_name}@{ip_address}
"""

# =k== ACK MESSAGE FORMAT ===
def ackMessage(message_id):
    return f"""\nTYPE: ACK
MESSAGE_ID: {message_id}
STATUS: RECEIVED
"""

# === FOLLOW MESSAGE FORMAT ===
def verboseFollowMessage(follower, userID, ip_address, ttl):
    token = timeStamp + ttl
    return f"""\nTYPE: FOLLOW
MESSAGE_ID: {message_id}
FROM: {follower}@{ip_address}
TO: {userID}
TIMESTAMP: {timeStamp}
TOKEN: {follower}@{ip_address}|{token}|follow
"""
def simpleFollowMessage(follower):
    return f"""User {follower} has followed you"""

# === UNFOLLOW MESSAGE FORMAT ===
def unfollowVerboseMessage(follower, userID, ip_address, ttl):
    return f"""\nTYPE: UNFOLLOW
MESSAGE_ID: {message_id}
FROM: {follower}@{ip_address}
TO: {userID}
TIMESTAMP: {timeStamp}
TOKEN: {follower}@{ip_address}|{timeStamp + ttl}|follow
"""
def unfollowSimpleMessage(follower):
    return f"""User {follower} has unfollowed you""
