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